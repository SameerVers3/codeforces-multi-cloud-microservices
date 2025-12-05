# Development Guide

## Local Development Setup

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL client tools

### Starting Services Locally

1. **Start infrastructure services**:
```bash
docker-compose up -d postgres redis rabbitmq
```

2. **Run database migrations**:
```bash
# Apply schema
psql -h localhost -U codeforces -d codeforces_db -f services/shared/database/schema.sql
```

3. **Start backend services**:
```bash
# Auth Service
cd services/auth-service
pip install -r requirements.txt
uvicorn app.main:app --port 8001

# Contest Service
cd services/contest-service
pip install -r requirements.txt
uvicorn app.main:app --port 8002

# Submission Service
cd services/submission-service
pip install -r requirements.txt
uvicorn app.main:app --port 8003

# Execution Service
cd services/execution-service
pip install -r requirements.txt
uvicorn app.main:app --port 8004

# Scoring Service
cd services/scoring-service
pip install -r requirements.txt
uvicorn app.main:app --port 8005

# Leaderboard Service
cd services/leaderboard-service
pip install -r requirements.txt
uvicorn app.main:app --port 8006
```

4. **Start frontend**:
```bash
cd frontend/nextjs-app
npm install
npm run dev
```

### Using Docker Compose

```bash
docker-compose up -d
```

This starts all services in containers.

## API Endpoints

### Auth Service (Port 8001)
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get current user
- `GET /api/v1/users/` - List users (staff only)

### Contest Service (Port 8002)
- `GET /api/v1/contests/` - List contests
- `POST /api/v1/contests/` - Create contest (staff only)
- `GET /api/v1/contests/{id}` - Get contest
- `POST /api/v1/registrations/contest/{id}/register` - Register for contest

### Submission Service (Port 8003)
- `POST /api/v1/submissions/` - Submit code
- `GET /api/v1/submissions/` - List submissions
- `GET /api/v1/submissions/{id}` - Get submission details

### Leaderboard Service (Port 8006)
- `GET /api/v1/leaderboard/contest/{id}` - Get leaderboard
- `WS /ws/leaderboard/{id}` - WebSocket for real-time updates

## Testing

### Running Tests

```bash
# Unit tests for a service
cd services/auth-service
pytest

# Integration tests
pytest tests/integration/
```

### Manual Testing

1. Register a user:
```bash
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'
```

2. Login:
```bash
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

3. Create contest (as staff):
```bash
curl -X POST http://localhost:8002/api/v1/contests/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Contest","start_time":"2024-01-01T00:00:00Z","end_time":"2024-01-02T00:00:00Z","duration_minutes":1440}'
```

## Code Style

- Python: Follow PEP 8, use Black for formatting
- TypeScript: Follow ESLint rules, use Prettier
- Use type hints in Python
- Document functions with docstrings

## Environment Variables

Each service uses environment variables for configuration. See `.env.example` files in each service directory.

## Database Migrations

Use Alembic for database migrations:

```bash
cd services/auth-service
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

