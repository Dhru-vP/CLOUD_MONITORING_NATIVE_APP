# 🌩️ Cloud-Native Monitoring App on Kubernetes

A real-time system resource monitoring application built with Flask and Python, containerized with Docker, and deployed on AWS EKS using Kubernetes.

## 📘 Overview

This project implements a resource monitoring web application that collects real-time CPU and memory statistics and visualizes them on a web dashboard. Built with modern cloud technologies, it demonstrates containerization, orchestration, and AWS cloud deployment.

## 🧰 Tech Stack

- **Frontend**: HTML, CSS
- **Backend**: Python, Flask, Flask-SocketIO
- **Containerization**: Docker
- **Cloud Platform**: AWS (ECR, EKS)
- **Orchestration**: Kubernetes
- **Automation**: Boto3, Kubernetes Python Client

## 🗂️ Project Structure

```
CLOUD_NATIVE_MONITORING_APP/
├── templates/              # HTML UI templates
│   └── index.html
├── app.py                  # Flask application
├── ecr.py                  # AWS ECR automation script
├── eks.py                  # AWS EKS automation script
├── Dockerfile              # Docker configuration
└── requirements.txt        # Python dependencies
```

## ✨ Features

- Real-time CPU & memory usage monitoring
- WebSocket-based data streaming
- Containerized deployment
- Secure and scalable hosting via AWS EKS
- Automated cloud provisioning

## ✅ Prerequisites

- AWS Account with programmatic access
- Python 3 installed
- Docker installed
- kubectl installed
- Code editor (VSCode recommended)

## 🚀 Deployment Guide

### Part 1: Local Deployment

1. **Clone the repository**
   ```bash
   git clone <repository_url>
   cd <project_folder>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```
   Access the dashboard at http://localhost:5000/

### Part 2: Docker Containerization

1. **Build the Docker image**
   ```bash
   docker build -t monitoring-app .
   ```

2. **Run the Docker container**
   ```bash
   docker run -p 5000:5000 monitoring-app
   ```
   Access at http://localhost:5000/

### Part 3: AWS ECR Deployment

1. **Create ECR repository**
   ```python
   # Using ecr.py script
   import boto3
   
   ecr_client = boto3.client('ecr')
   repository_name = 'monitoring-app-repo'
   response = ecr_client.create_repository(repositoryName=repository_name)
   repository_uri = response['repository']['repositoryUri']
   print(f"Repository URI: {repository_uri}")
   ```

2. **Push to ECR**
   ```bash
   # Authenticate Docker to ECR
   aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <repository_uri>
   
   # Tag and push
   docker tag monitoring-app:latest <repository_uri>:latest
   docker push <repository_uri>:latest
   ```

### Part 4: Kubernetes Deployment on EKS

1. **Create EKS cluster**
   ```bash
   # Use AWS Console or eks.py script to create cluster and node group
   ```

2. **Deploy the application**
   ```python
   # Using the Kubernetes Python client
   from kubernetes import client, config
   
   config.load_kube_config()
   api_client = client.ApiClient()
   
   # Create deployment
   deployment = client.V1Deployment(
       metadata=client.V1ObjectMeta(name="monitoring-app"),
       spec=client.V1DeploymentSpec(
           replicas=1,
           selector=client.V1LabelSelector(match_labels={"app": "monitoring-app"}),
           template=client.V1PodTemplateSpec(
               metadata=client.V1ObjectMeta(labels={"app": "monitoring-app"}),
               spec=client.V1PodSpec(containers=[
                   client.V1Container(
                       name="monitoring-container",
                       image="<repository_uri>:latest",
                       ports=[client.V1ContainerPort(container_port=5000)]
                   )
               ])
           )
       )
   )
   
   apps_v1 = client.AppsV1Api(api_client)
   apps_v1.create_namespaced_deployment(namespace="default", body=deployment)
   
   # Create service
   service = client.V1Service(
       metadata=client.V1ObjectMeta(name="monitoring-service"),
       spec=client.V1ServiceSpec(
           selector={"app": "monitoring-app"},
           ports=[client.V1ServicePort(port=5000, target_port=5000)],
           type="LoadBalancer"
       )
   )
   
   core_v1 = client.CoreV1Api(api_client)
   core_v1.create_namespaced_service(namespace="default", body=service)
   ```

3. **Verify the deployment**
   ```bash
   kubectl get deployment -n default
   kubectl get service -n default
   kubectl get pods -n default
   ```

4. **Access the application**
   ```bash
   # For testing, you can use port-forwarding
   kubectl port-forward service/monitoring-service 5000:5000
   
   # For production, access via the LoadBalancer URL
   kubectl get service monitoring-service -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
   ```

## 📄 License

This project is licensed under the MIT License.