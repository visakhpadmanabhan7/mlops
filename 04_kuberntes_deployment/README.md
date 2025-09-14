 Kubernetes (K8s) Basics

1. What is Kubernetes?
	•	Kubernetes = container orchestration platform.
	•	Think of it like an operating system for your containers.
	•	Instead of manually starting Docker containers, networking them, and restarting them when they fail → Kubernetes does all that automatically.

2. Why do we need Kubernetes?

Without Kubernetes:
	•	You run Docker containers manually: docker run -p 8000:8000 my-app.
	•	If the container crashes, you must restart it.
	•	If traffic spikes, you must manually run more containers.
	•	Networking between containers (APIs, DBs) = messy.
	•	Deploying to multiple machines = painful.

With Kubernetes:
	•	It keeps your app alive (auto-restarts containers if they fail).
	•	It scales up/down containers based on traffic.
	•	It has a service mesh (built-in networking & service discovery).
	•	It manages secrets, configs, storage.
	•	It runs across clusters of servers → looks like one machine.

| Component       | What it is                         | Why it’s needed                                   | Analogy                |
|-----------------|------------------------------------|--------------------------------------------------|------------------------|
| **Cluster**     | Whole Kubernetes system            | Runs and manages all workloads                   | The whole city         |
| **Node**        | A worker machine (VM/server)       | Provides compute/storage for Pods                 | A building             |
| **Pod**         | Smallest deployable unit           | Runs containers with networking/storage           | An apartment           |
| **Deployment**  | Controller for Pods                | Ensures desired replicas, self-healing, updates   | Blueprint for buildings|
| **Service**     | Stable network endpoint            | Load balances Pods, hides Pod IP changes          | Public entrance        |
| **Ingress**     | HTTP/HTTPS routing                 | Pretty URLs, external access to Services          | City gate & street signs|
| **ConfigMap**   | App config storage                 | Keeps configs separate from code                  | Instruction manual     |
| **Secret**      | Encrypted config storage           | Safely stores passwords, API keys                 | Safe with keys         |
| **Namespace**   | Logical grouping                   | Isolates dev/staging/prod resources               | District in the city   |


brew install --cask docker && brew install kubectl minikube

🔑 The Order of Kubernetes Components
	1.	Cluster
	•	First you need a cluster (the whole environment).
	•	If you’re using Minikube locally:
    . minikube start
	2.	Nodes
	•	A cluster is made of nodes (machines).
	•	When you create a cluster, Kubernetes already provisions nodes for you.
	•	In Minikube, it’s just 1 node (your laptop inside Docker/VM).
	•	On AWS/GCP/Azure, you can have many worker nodes.
	•	You don’t usually create nodes manually — Kubernetes/cloud does it.
    . kubectl get nodes

We’ll create two YAML files:
	1.	deployment.yaml → tells Kubernetes how to run Pods.
	2.	service.yaml → exposes your Pods so you can reach them.


 Summary (deployment.yaml )
	•	apiVersion + kind: tells Kubernetes “this is a Deployment.”
	•	metadata: gives it a name + labels.
	•	replicas: how many Pods (copies) to run.
	•	selector: tells Deployment which Pods belong to it.
	•	template: defines what each Pod looks like.
	•	containers: runs your Docker image.
	•	probes: health checks to restart or stop routing traffic if unresponsive.

 Summary (service.yaml )

    Line-by-line
	•	kind: Service → We’re creating a Service resource.
	•	metadata.name → Name = fastapi-service.
	•	selector.app=fastapi-app → This Service connects to all Pods with that label.
	•	ports.port=8000 → The Service will listen on port 8000.
	•	ports.targetPort=8000 → Traffic goes into the Pod’s container port 8000.
	•	type: NodePort → Makes it reachable outside the cluster on a high random port.

	You have a Deployment with 2 replicas (Pods).
	•	The Service (fastapi-service) load balances between them.
	•	Without Service → you’d have to manually find Pod IPs each time (painful).
	•	With Service → you always use fastapi-service:8000 inside the cluster, or a node/URL externally.

Cluster (Minikube)
 └── Node: minikube (your laptop/VM)
      └── Deployment: fastapi-deployment
           └── Pods:
               - Pod1 (FastAPI + model)
               - Pod2 (FastAPI + model)


# 🚀 FastAPI on Kubernetes (Minikube)

This demo shows how to deploy a FastAPI ML app on Kubernetes using **Deployment**, **Service**, and **Ingress**.

---

## 🛠️ Prerequisites
- Docker
- Minikube
- kubectl

---

## 📦 Step 1. Start Cluster
```bash
# Start local Kubernetes cluster
minikube start --driver=docker

# Verify cluster
kubectl cluster-info
kubectl get nodes
```

# Deploy FastAPI App
# Apply Deployment (runs 2 replicas of FastAPI container)
kubectl apply -f deployment.yaml

# Check Deployment & Pods
kubectl get deployments
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>

# Expose with Service

# Apply Service
kubectl apply -f service.yaml

# Check Services
kubectl get services

# Open Service in browser (NodePort URL)
minikube service fastapi-service --url

# (Alternative) Port-forward Service to localhost
kubectl port-forward service/fastapi-service 8080:8000

#Enable Ingress

# Enable ingress controller in Minikube
minikube addons enable ingress

# Apply Ingress resource
kubectl apply -f ingress.yaml

# Check Ingress
kubectl get ingress
kubectl describe ingress fastapi-ingress

# Get Minikube IP
minikube ip

#Test API

# Health check
curl http://fastapi.local/

# Prediction
curl -X POST http://fastapi.local/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[5.1,3.5,1.4,0.2]}'