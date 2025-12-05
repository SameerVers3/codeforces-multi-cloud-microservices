# Architecture Documentation

## System Overview

The Multi-Cloud Codeforces Platform is a distributed competitive programming platform built with microservices architecture and deployed across AWS, Azure, and GCP.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Next.js)                     │
│                         [GCP]                               │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐            ┌──────────▼──────────┐
│  Auth Service  │            │  Contest Service   │
│    [Azure]     │            │     [Azure]         │
└───────┬────────┘            └──────────┬──────────┘
        │                               │
        └───────────────┬───────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐            ┌──────────▼──────────┐
│ Submission Svc │            │  Execution Service  │
│     [AWS]      │───────────▶│       [AWS]         │
└───────┬────────┘            └──────────┬──────────┘
        │                               │
        └───────────────┬───────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐            ┌──────────▼──────────┐
│ Scoring Svc    │            │ Leaderboard Service │
│     [GCP]      │───────────▶│       [GCP]         │
└───────┬────────┘            └──────────┬──────────┘
        │                               │
        └───────────────┬───────────────┘
                        │
                ┌───────▼────────┐
                │   PostgreSQL   │
                │    [Azure]     │
                └────────────────┘
```

## Service Distribution

### AWS (High Compute)
- **Execution Service**: Docker-based C++ code execution
- **Submission Service**: Code submission handling and queue management

### Azure (Managed Services)
- **Auth Service**: User authentication and authorization
- **Contest Service**: Contest and problem management
- **PostgreSQL Database**: Primary data store

### GCP (Global Distribution)
- **Scoring Service**: Score calculation
- **Leaderboard Service**: Real-time leaderboard with WebSockets
- **Frontend**: Next.js application

## Data Flow

1. User submits code via Frontend
2. Submission Service validates and queues submission
3. Execution Service processes code in Docker sandbox
4. Results sent to Scoring Service
5. Scoring Service calculates score and updates leaderboard
6. Leaderboard Service broadcasts updates via WebSocket

## Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Next.js 14+ (App Router)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Message Queue**: RabbitMQ
- **Orchestration**: Kubernetes (EKS, AKS, GKE)
- **Infrastructure**: Terraform
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack / Loki
- **Tracing**: Jaeger

## Security

- JWT-based authentication
- Role-based access control (RBAC)
- Docker sandboxing for code execution
- TLS/SSL encryption
- Secrets management via cloud providers
- Network policies and security groups

## Scalability

- Horizontal scaling via Kubernetes
- Load balancing across cloud providers
- Failover mechanisms
- Auto-scaling based on metrics
- Caching layer with Redis

## Observability

- Prometheus metrics collection
- Grafana dashboards
- Distributed tracing with Jaeger
- Centralized logging
- Health check endpoints

