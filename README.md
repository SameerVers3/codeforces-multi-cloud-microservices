# Multi-Cloud Codeforces Platform

A comprehensive multi-cloud DevOps pipeline for a Codeforces-like competitive programming platform with microservices architecture, deployed across AWS, Azure, and GCP.

## Architecture

### Microservices
- **Auth Service** - User authentication, JWT tokens, role management
- **Contest Service** - Contest CRUD, registration management
- **Submission Service** - Code submission handling, queue management
- **Execution Service** - C++ code execution engine with Docker sandboxing
- **Scoring Service** - Score calculation and leaderboard computation
- **Leaderboard Service** - Real-time leaderboard updates via WebSockets
- **Frontend** - Next.js user interface with real-time updates

### Multi-Cloud Distribution
- **AWS**: Execution Service, Submission Service (high compute needs)
- **Azure**: Auth Service, Contest Service, Database (managed services)
- **GCP**: Scoring Service, Leaderboard Service, Frontend (CDN/global distribution)

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Next.js 14+ (App Router)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Message Queue**: RabbitMQ
- **Orchestration**: Kubernetes (EKS, AKS, GKE)
- **IaC**: Terraform
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack / Loki
- **Tracing**: Jaeger

## Status: ✅ 100% COMPLETE

All components have been fully implemented:
- ✅ All 6 microservices with complete functionality
- ✅ Full frontend with authentication, code editor, leaderboard
- ✅ Multi-cloud infrastructure (AWS, Azure, GCP)
- ✅ Complete Kubernetes setup with Helm charts
- ✅ Full observability stack (Prometheus, Grafana, Loki, Jaeger)
- ✅ Security hardening (network policies, RBAC, TLS)
- ✅ Failover mechanisms (circuit breakers, health checks)
- ✅ API Gateway configuration
- ✅ CI/CD pipeline
- ✅ Testing framework
- ✅ Comprehensive documentation

## Quick Start

### Local Development

```bash
# Start all services with Docker Compose
docker-compose up -d

# Run database migrations
psql -h localhost -U codeforces -d codeforces_db -f services/shared/database/schema.sql

# Access services:
# - Frontend: http://localhost:3000
# - Auth Service: http://localhost:8001
# - Contest Service: http://localhost:8002
# - Submission Service: http://localhost:8003
# - Execution Service: http://localhost:8004
# - Scoring Service: http://localhost:8005
# - Leaderboard Service: http://localhost:8006
```

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- Terraform
- kubectl
- Helm

## Project Structure

```
project/
├── infrastructure/     # Terraform, Kubernetes configs
├── services/          # Microservices
├── frontend/          # Next.js application
├── ci-cd/            # CI/CD pipelines
├── monitoring/       # Observability configs
└── docs/             # Documentation
```

## Development

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed development guide.

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for multi-cloud deployment instructions.

## License

MIT

