#!/bin/bash
# Ubuntu Deployment Script for POS AI Backend

set -e

echo "=== POS AI Backend Ubuntu Setup ==="

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y python3-pip python3-venv mongodb redis-server nginx git

# Start services
sudo systemctl start mongodb
sudo systemctl enable mongodb
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Create app directory
sudo mkdir -p /opt/pos-ai-backend
sudo chown $USER:$USER /opt/pos-ai-backend

# Clone repository (or copy files)
cd /opt/pos-ai-backend
# git clone <your-repo> . || echo "Copy files manually"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)
FLASK_ENV=production
MONGO_URI=mongodb://localhost:27017/pos_ai_db
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
AI_MODE=offline
EOF

# Create systemd service
sudo tee /etc/systemd/system/pos-ai-backend.service > /dev/null << 'EOF'
[Unit]
Description=POS AI Backend
After=network.target mongodb.service redis-server.service

[Service]
User=$USER
WorkingDirectory=/opt/pos-ai-backend
Environment="PATH=/opt/pos-ai-backend/venv/bin"
ExecStart=/opt/pos-ai-backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create celery worker service
sudo tee /etc/systemd/system/pos-celery-worker.service > /dev/null << 'EOF'
[Unit]
Description=POS AI Celery Worker
After=network.target mongodb.service redis-server.service

[Service]
User=$USER
WorkingDirectory=/opt/pos-ai-backend
Environment="PATH=/opt/pos-ai-backend/venv/bin"
ExecStart=/opt/pos-ai-backend/venv/bin/celery -A app.tasks.celery_worker worker --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start services
sudo systemctl daemon-reload
sudo systemctl enable pos-ai-backend
sudo systemctl enable pos-celery-worker
sudo systemctl start pos-ai-backend
sudo systemctl start pos-celery-worker

# Setup nginx
sudo tee /etc/nginx/sites-available/pos-ai-backend > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/pos-ai-backend /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl restart nginx

echo "=== Setup Complete ==="
echo "API running at http://localhost"
echo "Check status: sudo systemctl status pos-ai-backend"
