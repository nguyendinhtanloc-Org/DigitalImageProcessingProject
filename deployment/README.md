# Deployment - Docker Setup

**Owner:** Tấn Lộc | **Deadline:** 18/12/2025

## Chạy toàn bộ hệ thống

```bash
cd deployment
docker-compose up --build
```

## Truy cập

- Frontend: http://localhost:3000
- Backend: http://localhost:8080
- Model Service: http://localhost:5000
- Swagger UI: http://localhost:8080/swagger-ui.html

## Services

```yaml
services:
  model-service:   # Flask:5000 - Load models
  backend:         # Spring Boot:8080 - API
  frontend:        # React:3000 - UI
```

## Commands

```bash
# Stop
docker-compose down

# Logs
docker-compose logs -f

# Rebuild
docker-compose build --no-cache
```
