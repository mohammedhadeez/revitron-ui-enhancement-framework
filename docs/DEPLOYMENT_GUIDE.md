# 🚀 Deployment Guide

**Revitron UI Enhancement Framework v2.0 (Self-Reflection Integrated)**

This comprehensive deployment guide covers production deployment strategies, environment setup, and operational procedures for the Revitron UI Enhancement Framework in enterprise AEC environments.

---

## 🎯 Deployment Overview

### **Framework Vision**
Deploy a production-ready system that enables AEC professionals to systematically enhance Revitron UI with validated, implementable button suggestions backed by comprehensive technical specifications and quality assurance.

### **Deployment Objectives**
- ✅ **High Availability**: 99.9% uptime for critical AEC workflows
- ✅ **Scalability**: Support 10-100 concurrent users
- ✅ **Performance**: Sub-60 second processing for 250 button generation
- ✅ **Quality**: 10/10 performance across all dimensions (v2.0 standard)
- ✅ **Security**: Enterprise-grade security and access controls
- ✅ **Maintainability**: Simplified operations and monitoring

---

## 🏗️ Architecture Overview

### **Deployment Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                        │
│                   (nginx/HAProxy)                       │
└─────────────────────┬───────────────────────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
┌───▼───┐         ┌───▼───┐         ┌───▼───┐
│App    │         │App    │         │App    │
│Server │         │Server │         │Server │
│   1   │         │   2   │         │   3   │
└───┬───┘         └───┬───┘         └───┬───┘
    │                 │                 │
    └─────────────────┼─────────────────┘
                      │
┌─────────────────────▼─────────────────────┐
│            Shared Storage Layer            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ Config  │  │  Cache  │  │  Logs   │   │
│  │ Store   │  │  Redis  │  │   ELK   │   │
│  └─────────┘  └─────────┘  └─────────┘   │
└───────────────────────────────────────────┘
```

### **Component Distribution**
- **Application Servers**: Framework processing engines
- **Load Balancer**: Request distribution and failover
- **Shared Storage**: Configuration, cache, and logging
- **Monitoring**: Health checks and performance metrics
- **Backup Systems**: Data protection and recovery

---

## 🛠️ Prerequisites

### **System Requirements**

#### **Minimum Requirements**
```yaml
hardware:
  cpu_cores: 4
  memory_gb: 8
  disk_space_gb: 50
  network: "1 Gbps"

software:
  operating_system: ["Windows Server 2019+", "Ubuntu 20.04+", "CentOS 8+"]
  python_version: "3.7+"
  git_version: "2.20+"
```

#### **Recommended Requirements**
```yaml
hardware:
  cpu_cores: 8
  memory_gb: 16
  disk_space_gb: 100
  network: "10 Gbps"
  storage_type: "SSD"

software:
  operating_system: ["Windows Server 2022", "Ubuntu 22.04 LTS"]
  python_version: "3.11+"
  container_runtime: "Docker 24.0+"
```

### **Network Requirements**
- **Outbound HTTPS (443)**: Access to documentation sources
- **Internal HTTP (8080)**: Load balancer communication
- **Internal TCP (6379)**: Redis cache (if used)
- **Internal TCP (5432)**: PostgreSQL database (if used)

### **Security Requirements**
- **SSL/TLS Certificates**: For encrypted communication
- **Service Accounts**: Dedicated service accounts for framework processes
- **Firewall Rules**: Properly configured network security
- **Access Controls**: Role-based access to framework resources

---

## 📦 Deployment Methods

## **Method 1: Production Server Deployment**

### **Step 1: Environment Preparation**

```bash
# Create dedicated user for framework
sudo useradd -m -s /bin/bash revitron-framework
sudo usermod -aG sudo revitron-framework

# Switch to framework user
sudo su - revitron-framework

# Create directory structure
mkdir -p ~/revitron-framework/{config,logs,cache,backups}
cd ~/revitron-framework
```

### **Step 2: Framework Installation**

```bash
# Clone repository
git clone https://github.com/mohammedhadeez/revitron-ui-enhancement-framework.git
cd revitron-ui-enhancement-framework

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install framework in development mode
pip install -e .

# Verify installation
python main_controller.py --version
python main_controller.py --health-check
```

### **Step 3: Configuration Setup**

```bash
# Copy production configuration
cp config/framework_config.yaml config/production_config.yaml

# Customize for production environment
nano config/production_config.yaml
```

**Production Configuration Example:**
```yaml
framework:
  strict_mode: true
  debug_mode: false
  performance_monitoring: true

logging:
  level: "INFO"
  files:
    main_log: "/var/log/revitron-framework/framework.log"
    error_log: "/var/log/revitron-framework/errors.log"

performance:
  memory_management:
    max_memory_mb: 8192
  processing:
    parallel_processing: true
    max_workers: 6
```

### **Step 4: System Service Setup**

**Create systemd service file:**
```bash
sudo nano /etc/systemd/system/revitron-framework.service
```

```ini
[Unit]
Description=Revitron UI Enhancement Framework
After=network.target

[Service]
Type=simple
User=revitron-framework
Group=revitron-framework
WorkingDirectory=/home/revitron-framework/revitron-framework
Environment=PATH=/home/revitron-framework/revitron-framework/venv/bin
ExecStart=/home/revitron-framework/revitron-framework/venv/bin/python main_controller.py --config config/production_config.yaml --daemon
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=revitron-framework

[Install]
WantedBy=multi-user.target
```

**Enable and start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable revitron-framework
sudo systemctl start revitron-framework
sudo systemctl status revitron-framework
```

---

## **Method 2: Docker Container Deployment**

### **Step 1: Docker Setup**

**Create Dockerfile:**
```dockerfile
# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install framework
RUN pip install -e .

# Create non-root user
RUN useradd -m -u 1000 framework && chown -R framework:framework /app
USER framework

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python main_controller.py --health-check

# Default command
CMD ["python", "main_controller.py", "--config", "config/production_config.yaml"]
```

### **Step 2: Docker Compose for Production**

**Create docker-compose.yml:**
```yaml
version: '3.8'

services:
  revitron-framework:
    build: .
    restart: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - ./config:/app/config:ro
      - ./logs:/app/logs
      - ./cache:/app/cache
      - ./output:/app/output
    environment:
      - REVITRON_FRAMEWORK_ENV=production
      - REVITRON_FRAMEWORK_LOG_LEVEL=INFO
    depends_on:
      - redis
      - postgres
    networks:
      - revitron-network

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - revitron-network

  postgres:
    image: postgres:15-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: revitron_framework
      POSTGRES_USER: revitron
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - revitron-network

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/ssl/certs:ro
    depends_on:
      - revitron-framework
    networks:
      - revitron-network

volumes:
  redis_data:
  postgres_data:

networks:
  revitron-network:
    driver: bridge
```

### **Step 3: Deploy with Docker Compose**

```bash
# Create environment file
cat > .env << EOF
DB_PASSWORD=your_secure_password_here
REVITRON_FRAMEWORK_ENV=production
EOF

# Start services
docker-compose up -d

# Check service status
docker-compose ps
docker-compose logs revitron-framework
```

---

## **Method 3: Kubernetes Deployment**

### **Step 1: Kubernetes Manifests**

**Create namespace:**
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: revitron-framework
```

**Deployment manifest:**
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: revitron-framework
  namespace: revitron-framework
spec:
  replicas: 3
  selector:
    matchLabels:
      app: revitron-framework
  template:
    metadata:
      labels:
        app: revitron-framework
    spec:
      containers:
      - name: framework
        image: revitron-framework:2.0.0
        ports:
        - containerPort: 8080
        env:
        - name: REVITRON_FRAMEWORK_ENV
          value: "production"
        resources:
          requests:
            memory: "2Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

**Service manifest:**
```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: revitron-framework-service
  namespace: revitron-framework
spec:
  selector:
    app: revitron-framework
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

### **Step 2: Deploy to Kubernetes**

```bash
# Apply manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check deployment
kubectl get pods -n revitron-framework
kubectl get services -n revitron-framework

# View logs
kubectl logs -f deployment/revitron-framework -n revitron-framework
```

---

## 🔧 Load Balancer Configuration

### **Nginx Load Balancer**

**nginx.conf:**
```nginx
upstream revitron_framework {
    least_conn;
    server framework1:8080 weight=1 max_fails=3 fail_timeout=30s;
    server framework2:8080 weight=1 max_fails=3 fail_timeout=30s;
    server framework3:8080 weight=1 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name revitron-framework.company.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name revitron-framework.company.com;
    
    ssl_certificate /etc/ssl/certs/revitron-framework.crt;
    ssl_certificate_key /etc/ssl/private/revitron-framework.key;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    
    location / {
        proxy_pass http://revitron_framework;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_timeout 300s;
    }
    
    location /health {
        proxy_pass http://revitron_framework;
        access_log off;
    }
}
```

### **HAProxy Configuration**

**haproxy.cfg:**
```
global
    daemon
    user haproxy
    group haproxy
    chroot /var/lib/haproxy
    stats socket /var/run/haproxy.sock mode 660

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend revitron_frontend
    bind *:80
    bind *:443 ssl crt /etc/ssl/certs/revitron-framework.pem
    redirect scheme https if !{ ssl_fc }
    default_backend revitron_backend

backend revitron_backend
    balance roundrobin
    option httpchk GET /health
    server framework1 10.0.1.10:8080 check inter 2000ms
    server framework2 10.0.1.11:8080 check inter 2000ms
    server framework3 10.0.1.12:8080 check inter 2000ms

listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats admin if TRUE
```

---

## 📊 Monitoring and Logging

### **Application Monitoring**

**Health Check Endpoint:**
```python
# Add to main_controller.py
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'version': '2.0.0',
        'timestamp': datetime.utcnow().isoformat(),
        'components': {
            'research': check_research_health(),
            'validation': check_validation_health(),
            'generation': check_generation_health()
        }
    }
```

**Monitoring Script:**
```bash
#!/bin/bash
# monitor_framework.sh

ENDPOINT="http://localhost:8080/health"
LOG_FILE="/var/log/revitron-framework/monitor.log"

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    RESPONSE=$(curl -s -w "%{http_code}" "$ENDPOINT")
    HTTP_CODE="${RESPONSE: -3}"
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo "$TIMESTAMP - Framework healthy" >> "$LOG_FILE"
    else
        echo "$TIMESTAMP - Framework unhealthy (HTTP $HTTP_CODE)" >> "$LOG_FILE"
        # Send alert (customize as needed)
        # mail -s "Framework Alert" admin@company.com < "$LOG_FILE"
    fi
    
    sleep 60
done
```

### **Log Aggregation with ELK Stack**

**Elasticsearch Configuration:**
```yaml
# elasticsearch.yml
cluster.name: revitron-logs
node.name: node-1
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
network.host: 0.0.0.0
http.port: 9200
discovery.type: single-node
```

**Logstash Configuration:**
```ruby
# logstash.conf
input {
  file {
    path => "/var/log/revitron-framework/*.log"
    start_position => "beginning"
    codec => "json"
  }
}

filter {
  if [level] == "ERROR" or [level] == "CRITICAL" {
    mutate {
      add_tag => ["alert"]
    }
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "revitron-framework-%{+YYYY.MM.dd}"
  }
}
```

**Kibana Dashboard:**
Create dashboards for:
- Framework performance metrics
- Error rate trends
- User activity patterns
- System resource utilization
- Quality metrics tracking

---

## 🔐 Security Configuration

### **SSL/TLS Setup**

**Generate SSL Certificate:**
```bash
# Self-signed certificate (development)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/revitron-framework.key \
  -out /etc/ssl/certs/revitron-framework.crt \
  -subj "/CN=revitron-framework.company.com"

# Let's Encrypt certificate (production)
sudo certbot --nginx -d revitron-framework.company.com
```

### **Firewall Configuration**

**UFW (Ubuntu):**
```bash
# Allow SSH
sudo ufw allow ssh

# Allow HTTP and HTTPS
sudo ufw allow 'Nginx Full'

# Allow specific ports
sudo ufw allow 8080/tcp
sudo ufw allow 6379/tcp

# Enable firewall
sudo ufw --force enable
sudo ufw status
```

**iptables:**
```bash
# Allow established connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow framework port
iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

# Drop all other traffic
iptables -A INPUT -j DROP

# Save rules
iptables-save > /etc/iptables/rules.v4
```

### **Access Control**

**API Key Authentication (Future Enhancement):**
```yaml
# config/production_config.yaml
security:
  authentication:
    enabled: true
    method: "api_key"
    api_keys:
      - key: "prod_key_1"
        permissions: ["read", "write"]
      - key: "readonly_key_1" 
        permissions: ["read"]
```

---

## 💾 Backup and Recovery

### **Automated Backup Strategy**

**Backup Script:**
```bash
#!/bin/bash
# backup_framework.sh

BACKUP_DIR="/var/backups/revitron-framework"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="framework_backup_$DATE"

# Create backup directory
mkdir -p "$BACKUP_DIR/$BACKUP_NAME"

# Backup configuration
cp -r /home/revitron-framework/revitron-framework/config "$BACKUP_DIR/$BACKUP_NAME/"

# Backup logs (last 7 days)
find /var/log/revitron-framework -name "*.log" -mtime -7 -exec cp {} "$BACKUP_DIR/$BACKUP_NAME/" \;

# Backup generated outputs
cp -r /home/revitron-framework/revitron-framework/output "$BACKUP_DIR/$BACKUP_NAME/"

# Create archive
tar -czf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" -C "$BACKUP_DIR" "$BACKUP_NAME"

# Remove temporary directory
rm -rf "$BACKUP_DIR/$BACKUP_NAME"

# Cleanup old backups (keep last 30 days)
find "$BACKUP_DIR" -name "framework_backup_*.tar.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_DIR/$BACKUP_NAME.tar.gz"
```

**Cron Job for Automated Backups:**
```bash
# Add to crontab
sudo crontab -e

# Daily backup at 2 AM
0 2 * * * /usr/local/bin/backup_framework.sh

# Weekly full backup (Sundays at 1 AM)
0 1 * * 0 /usr/local/bin/full_backup_framework.sh
```

### **Disaster Recovery Procedure**

**Recovery Steps:**
1. **Stop Services**: `sudo systemctl stop revitron-framework`
2. **Restore Configuration**: Extract backup and restore config files
3. **Verify Dependencies**: Ensure all dependencies are installed
4. **Test Configuration**: Run configuration validation
5. **Start Services**: `sudo systemctl start revitron-framework`
6. **Verify Operation**: Run health checks and functionality tests

**Recovery Script:**
```bash
#!/bin/bash
# recover_framework.sh

BACKUP_FILE="$1"
FRAMEWORK_HOME="/home/revitron-framework/revitron-framework"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file.tar.gz>"
    exit 1
fi

# Stop framework service
sudo systemctl stop revitron-framework

# Backup current state
mv "$FRAMEWORK_HOME/config" "$FRAMEWORK_HOME/config.backup.$(date +%s)"

# Extract backup
tar -xzf "$BACKUP_FILE" -C /tmp/
cp -r /tmp/framework_backup_*/config "$FRAMEWORK_HOME/"

# Verify configuration
python "$FRAMEWORK_HOME/main_controller.py" --validate-config

# Start service
sudo systemctl start revitron-framework

# Verify health
sleep 10
python "$FRAMEWORK_HOME/main_controller.py" --health-check

echo "Recovery completed successfully"
```

---

## 🔄 Deployment Automation

### **CI/CD Pipeline with GitHub Actions**

**.github/workflows/deploy.yml:**
```yaml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -e .
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v
    
    - name: Build Docker image
      run: |
        docker build -t revitron-framework:${{ github.ref_name }} .
        docker tag revitron-framework:${{ github.ref_name }} revitron-framework:latest
    
    - name: Deploy to production
      run: |
        # Deploy to production servers
        ssh production-server "docker pull revitron-framework:latest"
        ssh production-server "docker-compose up -d"
```

### **Ansible Deployment Playbook**

**playbooks/deploy.yml:**
```yaml
---
- name: Deploy Revitron Framework
  hosts: production_servers
  become: yes
  
  vars:
    framework_user: revitron-framework
    framework_home: /home/{{ framework_user }}/revitron-framework
    
  tasks:
    - name: Create framework user
      user:
        name: "{{ framework_user }}"
        home: "/home/{{ framework_user }}"
        shell: /bin/bash
    
    - name: Install Python dependencies
      apt:
        name:
          - python3
          - python3-pip
          - python3-venv
          - git
        state: present
    
    - name: Clone framework repository
      git:
        repo: https://github.com/mohammedhadeez/revitron-ui-enhancement-framework.git
        dest: "{{ framework_home }}"
        version: "{{ framework_version | default('main') }}"
      become_user: "{{ framework_user }}"
    
    - name: Install framework
      pip:
        requirements: "{{ framework_home }}/requirements.txt"
        virtualenv: "{{ framework_home }}/venv"
      become_user: "{{ framework_user }}"
    
    - name: Create systemd service
      template:
        src: revitron-framework.service.j2
        dest: /etc/systemd/system/revitron-framework.service
      notify:
        - reload systemd
        - restart framework
    
    - name: Enable and start service
      systemd:
        name: revitron-framework
        enabled: yes
        state: started
  
  handlers:
    - name: reload systemd
      systemd:
        daemon_reload: yes
    
    - name: restart framework
      systemd:
        name: revitron-framework
        state: restarted
```

---

## 📈 Performance Optimization

### **Database Optimization (if using PostgreSQL)**

**postgresql.conf optimizations:**
```
# Memory settings
shared_buffers = 2GB
effective_cache_size = 6GB
work_mem = 64MB

# Checkpoint settings
checkpoint_completion_target = 0.9
wal_buffers = 16MB

# Connection settings
max_connections = 200
```

### **Redis Cache Optimization**

**redis.conf optimizations:**
```
# Memory management
maxmemory 2gb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000

# Performance
tcp-keepalive 300
timeout 300
```

### **Application Performance Tuning**

**Production configuration optimizations:**
```yaml
performance:
  parallel_processing: true
  max_workers: 8
  memory_management:
    max_memory_mb: 8192
    aggressive_gc: true
  
caching:
  enable_research_cache: true
  enable_validation_cache: true
  cache_duration_hours: 24
  cache_cleanup_interval_hours: 6
```

---

## 📋 Operational Procedures

### **Deployment Checklist**

#### **Pre-Deployment**
- [ ] Backup current production environment
- [ ] Test deployment in staging environment
- [ ] Verify all dependencies are updated
- [ ] Review configuration changes
- [ ] Notify stakeholders of deployment window

#### **Deployment**
- [ ] Stop existing services gracefully
- [ ] Deploy new version
- [ ] Update configuration files
- [ ] Restart services
- [ ] Verify health checks pass
- [ ] Monitor logs for errors

#### **Post-Deployment**
- [ ] Run functionality tests
- [ ] Verify performance metrics
- [ ] Check all integrations
- [ ] Update documentation
- [ ] Notify stakeholders of completion

### **Maintenance Procedures**

#### **Daily Tasks**
- Monitor application logs
- Check system resource utilization
- Verify backup completion
- Review performance metrics

#### **Weekly Tasks**
- Analyze usage patterns
- Review error trends
- Update security patches
- Clean up log files
- Test backup restoration

#### **Monthly Tasks**
- Performance optimization review
- Capacity planning assessment
- Security audit
- Documentation updates
- Dependency updates

---

## 🚨 Troubleshooting Deployment Issues

### **Common Deployment Problems**

#### **Service Won't Start**
```bash
# Check service status
sudo systemctl status revitron-framework

# Check logs
sudo journalctl -u revitron-framework -f

# Validate configuration
python main_controller.py --validate-config
```

#### **High Memory Usage**
```bash
# Monitor memory usage
top -p $(pgrep -f main_controller.py)

# Adjust memory limits
# Edit config/production_config.yaml
performance:
  memory_management:
    max_memory_mb: 4096  # Reduce from 8192
```

#### **Slow Performance**
```bash
# Enable performance profiling
python main_controller.py --profile --output performance_report.txt

# Check system resources
iostat -x 1
sar -u 1
```

### **Emergency Procedures**

#### **Service Recovery**
```bash
# Emergency restart
sudo systemctl restart revitron-framework

# Fallback to previous version
git checkout v1.0.0
sudo systemctl restart revitron-framework

# Disable problematic features
python main_controller.py --disable-validation --disable-research
```

#### **Load Balancer Failover**
```bash
# Remove unhealthy server from pool
# Edit nginx.conf and comment out problematic server
nginx -s reload

# Or via HAProxy stats interface
echo "disable server revitron_backend/framework2" | socat stdio /var/run/haproxy.sock
```

---

## 🎯 Success Metrics

### **Deployment Success Criteria**

- ✅ **Service Availability**: 99.9% uptime achieved
- ✅ **Performance**: Response times < 60 seconds for full processing
- ✅ **Quality**: All v2.0 self-reflection improvements active
- ✅ **Scalability**: Handles peak concurrent users
- ✅ **Monitoring**: All health checks passing
- ✅ **Security**: All security measures implemented

### **Key Performance Indicators**

```yaml
deployment_kpis:
  availability:
    target: 99.9%
    measurement: "uptime monitoring"
  
  performance:
    response_time_p95: "< 60s"
    throughput: "> 100 requests/hour"
    resource_utilization: "< 80%"
  
  quality:
    error_rate: "< 1%"
    validation_coverage: "100%"
    user_satisfaction: "> 4.5/5"
```

---

## 🔄 Rollback Procedures

### **Automated Rollback**

```bash
#!/bin/bash
# rollback_framework.sh

PREVIOUS_VERSION="$1"
SERVICE_NAME="revitron-framework"

# Stop current service
sudo systemctl stop "$SERVICE_NAME"

# Switch to previous version
cd /home/revitron-framework/revitron-framework
git checkout "$PREVIOUS_VERSION"

# Restore previous configuration if needed
if [ -f "config/config.backup" ]; then
    cp config/config.backup config/production_config.yaml
fi

# Restart service
sudo systemctl start "$SERVICE_NAME"

# Verify rollback
sleep 10
python main_controller.py --health-check

echo "Rollback to $PREVIOUS_VERSION completed"
```

---

**🎯 Deployment Vision**: Successfully deploy a production-ready framework that transforms AEC workflow efficiency through systematic UI enhancement, achieving 10/10 performance across all quality dimensions while maintaining enterprise-grade reliability and security.

**🚀 Next Steps**: After successful deployment, refer to the [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for operational guidance and [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for issue resolution procedures.
