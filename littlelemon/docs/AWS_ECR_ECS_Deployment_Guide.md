# 🚀 Deploy Docker Container on AWS with ECR + ECS (Fargate)

This guide explains how to deploy a Docker container to AWS using:

- **ECR** (Elastic Container Registry) to store Docker images
- **ECS** (Elastic Container Service) with **Fargate** to run containers
- Optional: **Load Balancer + HTTPS with ACM certificate**

---

## 🧱 Prerequisites

- AWS CLI installed and configured (`aws configure`)
- Docker installed locally
- An AWS IAM user with permissions for ECR, ECS, EC2, ACM, and IAM
- VPC and public subnets already created (or use default VPC)

---

## 1️⃣ Create an ECR Repository

### ✅ Using GUI:
1. Open AWS Console → ECR → "Create repository"
2. Name it (e.g., `my-app`)
3. Keep settings default (private repo)
4. Click **"Create repository"**

### 💻 Using AWS CLI:
```bash
aws ecr create-repository --repository-name my-app


2️⃣ Build and Push Docker Image to ECR
🛠️ Build and Tag Locally:
docker build -t my-app .

🔁 Tag for ECR:
aws_account_id=<your-account-id>
region=<your-region>
repo_uri="$aws_account_id.dkr.ecr.$region.amazonaws.com/my-app"
docker tag my-app:latest $repo_uri:latest

🔐 Authenticate and Push:
aws ecr get-login-password --region $region | docker login --username AWS --password-stdin $repo_uri
docker push $repo_uri:latest

3️⃣ Create ECS Cluster (Fargate)
✅ Using GUI:
Go to ECS → Clusters → "Create Cluster"
Choose "Networking only (Fargate)"
Name it my-cluster
Click "Create"

4️⃣ Register Task Definition
✅ Using GUI:
Go to ECS → Task Definitions → "Create new Task Definition"
Launch type: Fargate
Task name: my-app-task
Task role: ecsTaskExecutionRole (create if missing)
Set CPU: 256 and Memory: 512
Add Container:
Name: my-app
Image: ECR URI (<repo-uri>:latest)
Port mapping: 80
Click "Add", then "Create"

5️⃣ Run ECS Service
✅ Using GUI:
Go to your ECS Cluster → Services → "Create"
Launch type: Fargate
Task Definition: my-app-task
Service Name: my-app-service
Desired tasks: 1
Click "Next"

6️⃣ Configure Networking
Select VPC and public subnets
Enable "Auto-assign public IP"
Select/Create a security group that allows port 80 (HTTP)
Click "Next", then "Create Service"

7️⃣ Access Your Application
Go to ECS → Cluster → Tasks
Click the running task
Under Networking, find the public IP

Visit:
http://<your-task-public-ip>
🔒 [Optional] HTTPS via Load Balancer + ACM
🛠️ Create ACM Certificate
Go to ACM → "Request a certificate"
Choose public certificate, add your domain (e.g., example.com)
Validate via DNS or email
Once issued, proceed

🌐 Create Load Balancer (ALB)
Go to EC2 → Load Balancers → "Create Load Balancer"
Choose Application Load Balancer
Name it (e.g., my-app-alb)

Scheme: internet-facing

Listeners:
HTTP (80)
Add HTTPS (443) with your ACM certificate
Choose public subnets and security groups (allow 80 & 443)

🎯 Create Target Group
Target type: IP
Protocol: HTTP, port: 80
Register your running ECS tasks by IP

🔗 Update ECS Service
Go to ECS Cluster → Service → "Update"
Set Load Balancer to the new ALB and target group
Redeploy the service

✅ Done!
Your Docker container is now deployed and running on AWS ECS (Fargate), secured via HTTPS and fully managed. 🚀

🧠 Pro Tips
Use Secrets Manager or SSM Parameter Store for sensitive environment variables
Use Application Auto Scaling to manage service capacity
Add CloudWatch logs to monitor container output
