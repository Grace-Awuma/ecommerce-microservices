# E-Commerce Microservices on Azure

A production-grade microservices architecture built with Python FastAPI, deployed on Azure Kubernetes Service (AKS) using Terraform for infrastructure provisioning and GitHub Actions + Jenkins for CI/CD automation.

---

## Architecture Overview

```
                         ┌─────────────────────────────────────┐
                         │         Azure Kubernetes Service      │
                         │                                       │
  Client Request ──────► │  ┌─────────────┐  ┌──────────────┐  │
                         │  │   Product   │  │    Order     │  │
                         │  │   Service   │  │   Service    │  │
                         │  │  :8000      │  │   :8001      │  │
                         │  └──────┬──────┘  └──────┬───────┘  │
                         │         │                 │          │
                         │  ┌──────▼──────┐  ┌──────▼───────┐  │
                         │  │  Product DB │  │   Order DB   │  │
                         │  │ PostgreSQL  │  │  PostgreSQL  │  │
                         │  └─────────────┘  └──────────────┘  │
                         │                                       │
                         │         ┌──────────────┐             │
                         │         │   Payment    │             │
                         │         │   Service    │             │
                         │         │   :8002      │             │
                         │         └──────┬───────┘             │
                         │                │                     │
                         │         ┌──────▼───────┐             │
                         │         │  Payment DB  │             │
                         │         │  PostgreSQL  │             │
                         │         └──────────────┘             │
                         └─────────────────────────────────────┘
```

---

## Tech Stack

| Category | Technology |
|---|---|
| **Language** | Python 3.12 |
| **Framework** | FastAPI |
| **Database** | Azure Database for PostgreSQL Flexible Server |
| **Containerization** | Docker |
| **Orchestration** | Kubernetes (AKS) |
| **Container Registry** | Azure Container Registry (ACR) |
| **Infrastructure as Code** | Terraform |
| **CI/CD** | GitHub Actions + Jenkins |
| **Secrets Management** | Azure Key Vault |
| **Cloud Provider** | Microsoft Azure |

---

## Services

### Product Service (Port 8000)
Manages the product catalog and stock levels.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/products` | List all products |
| POST | `/products` | Create a product |
| GET | `/products/{id}` | Get product by ID |
| PATCH | `/products/{id}/stock` | Update stock |
| DELETE | `/products/{id}` | Delete product |

### Order Service (Port 8001)
Orchestrates the order flow — validates stock, reserves inventory and triggers payment.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/orders` | Create an order |
| GET | `/orders` | List all orders |
| GET | `/orders/{id}` | Get order by ID |

### Payment Service (Port 8002)
Handles payment processing and transaction records.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/payments` | Process a payment |
| GET | `/payments/{id}` | Get payment by ID |
| GET | `/payments/order/{id}` | Get payment by order ID |

---

## Infrastructure (Terraform)

All Azure infrastructure is provisioned as code using Terraform:

```
infra/
├── main.tf          # AKS, ACR, PostgreSQL, Key Vault
├── variables.tf     # Input variables
├── outputs.tf       # Output values
├── providers.tf     # Azure provider config
├── bootstrap.sh     # One-time backend setup
└── environments/
    ├── dev.tfvars
    └── prod.tfvars
```

**Resources provisioned:**
- Azure Resource Group
- Azure Kubernetes Service (AKS) — Standard_B2s_v2, 1 node
- Azure Container Registry (ACR) — Basic tier
- Azure Database for PostgreSQL Flexible Server × 3 — B_Standard_B1ms
- Azure Key Vault — stores database credentials
- Role assignments — AKS → ACR pull permission

---

## CI/CD Pipeline

### GitHub Actions

```
git push to main
      │
      ▼
build-and-push.yml
  ├── Login to Azure
  ├── Login to ACR
  ├── Build product-service image
  ├── Build order-service image
  ├── Build payment-service image
  └── Push all images to ACR
      │
      ▼ (on success)
deploy.yml
  ├── Login to Azure
  ├── Get AKS credentials
  ├── Rollout restart all deployments
  └── Verify pods are running
```

### CI Checks (Pull Requests)

```
pull_request to main
      │
      ▼
ci.yml
  ├── Lint Python code (flake8)
  ├── Validate Docker builds
  └── Validate Azure credentials
```

### Jenkins (Jenkinsfile)

An equivalent Jenkins pipeline is defined in `jenkins/Jenkinsfile` for enterprise environments that require self-hosted CI/CD:

```
Stages:
  1. Checkout
  2. Login to Azure
  3. Build Docker Images
  4. Push to ACR
  5. Deploy to AKS
  6. Verify Deployment
```

---

## Local Development

### Prerequisites
- Docker Desktop
- Python 3.12
- Azure CLI
- kubectl
- Terraform

### Run locally with Docker Compose

```bash
# Clone the repo
git clone https://github.com/Grace-Awuma/ecommerce-microservices.git
cd ecommerce-microservices

# Start all services with PostgreSQL databases
docker-compose up --build
```

**Service URLs:**
- Product Service: http://localhost:8000/docs
- Order Service: http://localhost:8001/docs
- Payment Service: http://localhost:8002/docs

### Test the full flow

```bash
# 1. Create a product
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "description": "Dev machine", "price": 999.99, "stock": 10}'

# 2. Place an order (use product ID from step 1)
curl -X POST http://localhost:8001/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_email": "user@example.com", "items": [{"product_id": "<ID>", "quantity": 1}]}'

# 3. Check payment
curl http://localhost:8002/payments/order/<order_id>
```

---

## Deployment to Azure

### 1. Set up infrastructure

```bash
cd infra
bash bootstrap.sh
export TF_VAR_db_password="your-password"
terraform init
terraform plan -var-file=environments/dev.tfvars
terraform apply -var-file=environments/dev.tfvars
```

### 2. Push images to ACR

```bash
az acr login --name gracecommerceacr
docker-compose build
docker tag ecommerce-microservices-product-service gracecommerceacr.azurecr.io/product-service:latest
docker push gracecommerceacr.azurecr.io/product-service:latest
# repeat for order-service and payment-service
```

### 3. Deploy to AKS

```bash
az aks get-credentials --resource-group ecommerce-rg --name ecommerce-aks
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/db-config.yaml
kubectl apply -f k8s/ -R
```

### 4. Verify

```bash
kubectl get pods -n ecommerce
kubectl port-forward service/product-service 8000:8000 -n ecommerce
```

---

## Project Structure

```
ecommerce-microservices/
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI checks on PRs
│       ├── build-and-push.yml  # Build and push to ACR
│       └── deploy.yml          # Deploy to AKS
├── infra/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── providers.tf
│   ├── bootstrap.sh
│   └── environments/
├── k8s/
│   ├── namespace.yaml
│   ├── ingress.yaml
│   ├── product-service/
│   ├── order-service/
│   └── payment-service/
├── product-service/
├── order-service/
├── payment-service/
├── jenkins/
│   └── Jenkinsfile
└── docker-compose.yml
```

---

## Key Design Decisions

**Database per service** — Each microservice owns its own PostgreSQL database. No shared databases, enforcing loose coupling.

**Managed databases** — Used Azure Database for PostgreSQL Flexible Server instead of running PostgreSQL inside Kubernetes pods — more reliable and closer to production patterns.

**Secret management** — Database credentials stored in Azure Key Vault, injected into pods via Kubernetes secrets. Never hardcoded in code or manifests.

**Infrastructure as Code** — 100% of Azure infrastructure defined in Terraform with remote state stored in Azure Blob Storage.

**Dual CI/CD** — GitHub Actions for managed pipeline (build + deploy), Jenkins pipeline defined for enterprise self-hosted environments.

---

## Author

**Grace Aku Nutifafa Awuma**
- LinkedIn: [linkedin.com/in/graceawuma](https://linkedin.com/in/graceawuma)
- GitHub: [github.com/Grace-Awuma](https://github.com/Grace-Awuma)