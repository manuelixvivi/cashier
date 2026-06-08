# Deployment Guide

## Docker Compose (Recommended)
```bash
cd docker
docker-compose up -d
```

## CasaOS
1. Copy `deployments/casaos/docker-compose.yml` to CasaOS
2. Update environment variables
3. Deploy via CasaOS UI

## Ubuntu Server
```bash
chmod +x deployments/ubuntu/setup.sh
sudo ./deployments/ubuntu/setup.sh
```

## Windows (Development)
```cmd
deployments/windows/setup.bat
```

## Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| SECRET_KEY | Flask secret key | dev-secret-key |
| JWT_SECRET_KEY | JWT signing key | jwt-secret-key |
| MONGO_URI | MongoDB connection | mongodb://localhost:27017/pos_ai_db |
| REDIS_URL | Redis connection | redis://localhost:6379/0 |
| AI_MODE | AI mode (online/offline/hybrid) | offline |
| GROQ_API_KEY | Groq API key (for online mode) | - |

## First Run
1. Start services
2. Register admin user: `POST /api/v1/auth/register`
3. Initialize settings: `POST /api/v1/settings/init`
