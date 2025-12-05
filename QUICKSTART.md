# Quick Start Guide

## ✅ Services are Running!

All containers have been successfully started. Here's what to do next:

## 1. Initialize the Database

First, you need to create the database schema:

```bash
# Connect to PostgreSQL and run the schema
docker exec -i codeforces-postgres psql -U codeforces -d codeforces_db < services/shared/database/schema.sql
```

Or manually:

```bash
docker exec -it codeforces-postgres psql -U codeforces -d codeforces_db
```

Then paste the contents of `services/shared/database/schema.sql`

## 2. Access the Services

### Frontend
- **URL**: http://localhost:3000
- Open in your browser to see the Codeforces platform

### Backend Services (API Documentation)
- **Auth Service**: http://localhost:8001/docs
- **Contest Service**: http://localhost:8002/docs
- **Submission Service**: http://localhost:8003/docs
- **Execution Service**: http://localhost:8004/docs
- **Scoring Service**: http://localhost:8005/docs
- **Leaderboard Service**: http://localhost:8006/docs

### Infrastructure Services
- **RabbitMQ Management**: http://localhost:15672 (username: codeforces, password: codeforces_dev)
- **PostgreSQL**: localhost:5432 (user: codeforces, password: codeforces_dev, db: codeforces_db)
- **Redis**: localhost:6379

## 3. Test the Platform

### Step 1: Register a User

```bash
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "Test User"
  }'
```

### Step 2: Login

```bash
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"
```

Save the `access_token` from the response.

### Step 3: Create a Contest (as Staff)

First, create a staff user in the database:

```bash
docker exec -it codeforces-postgres psql -U codeforces -d codeforces_db -c "
UPDATE users SET role = 'staff' WHERE username = 'testuser';
"
```

Then create a contest:

```bash
curl -X POST http://localhost:8002/api/v1/contests/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Contest",
    "description": "A test contest",
    "start_time": "2024-12-06T00:00:00Z",
    "end_time": "2024-12-07T00:00:00Z",
    "duration_minutes": 1440
  }'
```

### Step 4: Access the Frontend

1. Open http://localhost:3000 in your browser
2. Click "Register" to create an account
3. Login with your credentials
4. Browse contests and submit code!

## 4. Check Service Health

```bash
# Check all service health endpoints
curl http://localhost:8001/health  # Auth
curl http://localhost:8002/health  # Contest
curl http://localhost:8003/health  # Submission
curl http://localhost:8004/health  # Execution
curl http://localhost:8005/health  # Scoring
curl http://localhost:8006/health  # Leaderboard
```

## 5. View Logs

```bash
# View logs for all services
docker-compose logs -f

# View logs for a specific service
docker-compose logs -f auth-service
docker-compose logs -f frontend
```

## 6. Stop Services

```bash
docker-compose down
```

## 7. Restart Services

```bash
docker-compose restart
```

## Troubleshooting

### Database Connection Issues
If services can't connect to the database:
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres
```

### Service Not Starting
```bash
# Check service logs
docker-compose logs <service-name>

# Restart a specific service
docker-compose restart <service-name>
```

### Frontend Not Loading
- Make sure port 3000 is not in use
- Check frontend logs: `docker-compose logs frontend`
- Verify environment variables in `docker-compose.yml`

## Next Steps

1. **Set up the database schema** (see step 1 above)
2. **Create your first user** via the frontend or API
3. **Create a contest** (requires staff role)
4. **Add problems to the contest**
5. **Submit code** and watch it execute!

## Development

For local development without Docker:

```bash
# Start only infrastructure services
docker-compose up -d postgres redis rabbitmq

# Run services locally
cd services/auth-service && uvicorn app.main:app --port 8001 --reload
cd services/contest-service && uvicorn app.main:app --port 8002 --reload
# ... etc
```

## Production Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for multi-cloud deployment instructions.

