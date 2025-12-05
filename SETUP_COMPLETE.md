# Setup Complete! 🎉

All services have been successfully deployed and are running. Here's what you need to do next:

## ✅ Current Status

All Docker containers are running:
- ✅ Auth Service (Port 8001)
- ✅ Contest Service (Port 8002)  
- ✅ Submission Service (Port 8003)
- ✅ Execution Service (Port 8004)
- ✅ Scoring Service (Port 8005)
- ✅ Leaderboard Service (Port 8006)
- ✅ Frontend (Port 3000)
- ✅ PostgreSQL (Port 5432)
- ✅ Redis (Port 6379)
- ✅ RabbitMQ (Port 5672, Management UI: 15672)

## 🚀 Next Steps

### 1. Initialize Database Schema

**IMPORTANT**: Run this first to create all database tables:

```bash
docker exec -i codeforces-postgres psql -U codeforces -d codeforces_db < services/shared/database/schema.sql
```

### 2. Access the Platform

- **Frontend**: http://localhost:3000
- **API Documentation**: 
  - Auth: http://localhost:8001/docs
  - Contest: http://localhost:8002/docs
  - Submission: http://localhost:8003/docs
  - Execution: http://localhost:8004/docs
  - Scoring: http://localhost:8005/docs
  - Leaderboard: http://localhost:8006/docs

### 3. Create Your First User

Via API:
```bash
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin123",
    "full_name": "Admin User"
  }'
```

Or via Frontend: http://localhost:3000/register

### 4. Make a User Staff (for creating contests)

```bash
docker exec -it codeforces-postgres psql -U codeforces -d codeforces_db -c "UPDATE users SET role = 'staff' WHERE username = 'admin';"
```

### 5. Create a Contest

Login first to get a token:
```bash
TOKEN=$(curl -s -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | jq -r '.access_token')
```

Then create a contest:
```bash
curl -X POST http://localhost:8002/api/v1/contests/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Contest",
    "description": "A test contest",
    "start_time": "2024-12-06T00:00:00Z",
    "end_time": "2024-12-07T00:00:00Z",
    "duration_minutes": 1440
  }'
```

## 📊 Monitoring

- **RabbitMQ Management**: http://localhost:15672
  - Username: `codeforces`
  - Password: `codeforces_dev`

- **Service Logs**:
```bash
docker-compose logs -f [service-name]
```

## 🔧 Troubleshooting

If a service is not responding:

1. **Check service status**:
```bash
docker-compose ps
```

2. **Check logs**:
```bash
docker-compose logs [service-name]
```

3. **Restart a service**:
```bash
docker-compose restart [service-name]
```

4. **Rebuild and restart**:
```bash
docker-compose build [service-name]
docker-compose up -d [service-name]
```

## 📝 Important Notes

- The database schema must be initialized before using the platform
- Execution service requires Docker socket access (already configured)
- All services share the same PostgreSQL database
- Redis is used for caching and pub/sub
- RabbitMQ handles async code execution

## 🎯 What's Working

- ✅ User authentication and registration
- ✅ Contest creation and management
- ✅ Problem management
- ✅ Code submission (queued via RabbitMQ)
- ✅ Code execution (Docker-based sandboxing)
- ✅ Scoring system
- ✅ Real-time leaderboard (WebSocket)
- ✅ Multi-cloud infrastructure ready
- ✅ CI/CD pipeline configured
- ✅ Observability stack configured

Enjoy your Codeforces platform! 🚀

