# 🚀 Deploy FastAPI Model to AWS ECS (with CI/CD)

This repository demonstrates how to train a model, package it with FastAPI in Docker, and deploy it to **AWS ECS Fargate** using **GitHub Actions CI/CD**.

---

## 🔹 1. AWS One-Time Setup

Before running the pipeline, you must create resources in AWS.

### Install AWS CLI (Mac)
```bash
brew install awscli
aws --version
```

### Configure AWS CLI
```bash
aws configure
```
Provide:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION` (e.g., `eu-central-1`)

### Create ECR Repository
```bash
aws ecr create-repository   --repository-name mlops-model   --image-scanning-configuration scanOnPush=true   --region eu-central-1
```

### Create ECS Cluster
```bash
aws ecs create-cluster   --cluster-name mlops-cluster   --region eu-central-1
```

### Create IAM Execution Role
Create trust policy:
```bash
cat > ecs-trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "ecs-tasks.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
```

Create role:
```bash
aws iam create-role   --role-name ecsTaskExecutionRole   --assume-role-policy-document file://ecs-trust-policy.json
```

Attach permissions:
```bash
aws iam attach-role-policy   --role-name ecsTaskExecutionRole   --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

### Register ECS Task Definition
`ecs-task-def.json`:
```json
{
  "family": "mlops-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::094905625251:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "mlops-container",
      "image": "094905625251.dkr.ecr.eu-central-1.amazonaws.com/mlops-model:latest",
      "essential": true,
      "portMappings": [
        { "containerPort": 8000, "protocol": "tcp" }
      ]
    }
  ]
}
```

Register task definition:
```bash
aws ecs register-task-definition   --cli-input-json file://ecs-task-def.json
```

### Create ECS Service with Public IP
Find VPC + Subnets:
```bash
aws ec2 describe-vpcs --query "Vpcs[].VpcId" --region eu-central-1
aws ec2 describe-subnets --filters "Name=vpc-id,Values=<your-vpc-id>"   --query "Subnets[].SubnetId" --region eu-central-1
```

Create service:
```bash
aws ecs create-service   --cluster mlops-cluster   --service-name mlops-service   --task-definition mlops-task   --desired-count 1   --launch-type FARGATE   --network-configuration "awsvpcConfiguration={subnets=[subnet-aaa,subnet-bbb],assignPublicIp=ENABLED}"   --region eu-central-1
```

---

## 🔹 2. GitHub Secrets Setup

In your repo → **Settings → Secrets and variables → Actions → New repository secret**:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION` (e.g., `eu-central-1`)

---

## 🔹 3. GitHub Actions CI/CD Workflow

Save as `.github/workflows/aws_pipeline.yml`:

```yaml
name: AWS CI/CD Pipeline

on:
  push:
    branches: [ "aws_deploy" ]   # ✅ Run everything only on aws_deploy branch

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - run: |
          python -m pip install --upgrade pip
          pip install -r 01_cicd_pipeline/requirements.txt
          pip install pytest flake8
      - run: flake8 . --select=E9,F63,F7,F82 --show-source --statistics
      - run: pytest -v tests/

  train:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - run: |
          python -m pip install --upgrade pip
          pip install -r 01_cicd_pipeline/requirements.txt
      - run: python 01_cicd_pipeline/train.py
      - uses: actions/upload-artifact@v4
        with:
          name: trained-model
          path: artifacts/model.pkl

  smoke-test:
    runs-on: ubuntu-latest
    needs: train
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: trained-model
          path: 02_docker_fastapi/
      - run: docker build -t mlops-model:test 02_docker_fastapi
      - run: docker run -d -p 8000:8000 --name test_container mlops-model:test
      - run: |
          sleep 5
          curl -X POST "http://localhost:8000/predict"             -H "Content-Type: application/json"             -d '{"features":[5.1,3.5,1.4,0.2]}'
      - run: docker rm -f test_container

  deploy_aws:
    runs-on: ubuntu-latest
    needs: smoke-test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: trained-model
          path: 02_docker_fastapi/
      - run: docker build -t mlops-model:latest 02_docker_fastapi

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Push image to ECR
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: mlops-model
        run: |
          docker tag mlops-model:latest $ECR_REGISTRY/$ECR_REPOSITORY:latest
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest

      - name: Update ECS Service
        run: |
          aws ecs update-service             --cluster mlops-cluster             --service mlops-service             --force-new-deployment

      - name: Wait for task to start
        run: sleep 60

      - name: Get Public IP
        run: |
          TASK_ARN=$(aws ecs list-tasks             --cluster mlops-cluster             --service-name mlops-service             --query "taskArns[0]" --output text)

          PUBLIC_IP=$(aws ecs describe-tasks             --cluster mlops-cluster             --tasks $TASK_ARN             --query "tasks[0].attachments[0].details[?name=='publicIPv4Address'].value"             --output text)

          echo "✅ ECS Task Public IP: $PUBLIC_IP"
          echo "🌍 Test your API at: http://$PUBLIC_IP:8000/predict"
```

---

## 🔹 4. Testing the API

After deployment, check the GitHub Actions logs — you’ll see output like:

```
✅ ECS Task Public IP: 18.212.45.67
🌍 Test your API at: http://18.212.45.67:8000/predict
```

Test with curl:
```bash
curl -X POST "http://18.212.45.67:8000/predict"   -H "Content-Type: application/json"   -d '{"features":[5.1,3.5,1.4,0.2]}'
```

Or use Postman. ✅
