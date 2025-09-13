# 🤖 MLOps Robotics Prep

This repo is a learning project to practice **MLOps workflows** for robotics AI.  
It demonstrates how to build, test, train, and deploy ML models with **GitHub Actions**, **Docker**, and **FastAPI**.

---

## 🚀 Features

- **CI (Continuous Integration)**
  - Linting with `flake8` (basic syntax & error checks)
  - Unit tests with `pytest` (training & inference validation)
  - Model training with scikit-learn
  - Artifact storage (`model.pkl`)

- **CD (Continuous Delivery)**
  - Dockerize ML model with FastAPI
  - Push container image to **Docker Hub**
  - Image ready for deployment to Kubernetes / cloud services

---

## 📂 Repo Structure

mlops-robotics-prep/
│
├── 01_cicd_pipeline/          # CI/CD basics
│   ├── train.py               # Train simple sklearn model
│   ├── requirements.txt       # Training deps
│
├── 02_docker_fastapi/         # FastAPI + Docker model server
│   ├── app.py                 # FastAPI app to serve predictions
│   ├── requirements.txt       # Serving deps
│   └── Dockerfile             # Docker build instructions
│
├── tests/                     # Unit tests
│   ├── test_training.py       # Verify training produces model.pkl
│   └── test_inference.py      # Verify model can predict
│
└── .github/workflows/
└── ci_cd.yml              # Unified CI/CD workflow

---

## ⚙️ CI/CD Pipeline

### 🔹 Workflow Overview
1. **Build Job**
   - Install dependencies
   - Run `flake8` linting
   - Run `pytest` tests

2. **Train Job**
   - Train model (`train.py`)
   - Save artifact → `artifacts/model.pkl`

3. **Deploy Job (only on `main`)**
   - Download model artifact
   - Build Docker image with FastAPI
   - Push to Docker Hub

---

## 🧪 Run Locally

### Train the model
```bash
pip install -r 01_cicd_pipeline/requirements.txt
python 01_cicd_pipeline/train.py
```
## Run tests
pytest -v tests/

## Build Docker image
docker build -t my-ml-model:latest 02_docker_fastapi

## Run container
Run container

## Test API
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"features":[5.1,3.5,1.4,0.2]}'