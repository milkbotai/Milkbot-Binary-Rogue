# Operations

This document describes deployment, runtime execution, monitoring, and operational procedures for Binary‑Rogue.

---

## Runtime Model

Binary‑Rogue runs as a scheduled batch process that produces static artifacts.

### Operational Characteristics

- **Periodic execution** – Scheduled builds (recommended: every 15 minutes)
- **Atomic outputs** – Artifacts written atomically (tmp → rename)
- **Stateless builds** – No persistent state between runs
- **Environment configuration** – Secrets via environment variables
- **Structured logging** – JSON logs for parsing and analysis

### Execution Flow

```
Trigger (cron/webhook) → Build Process → Validation → Atomic Write → Serve
```

---

## Infrastructure

### Primary Deployment

**VPS Details:**
- Primary IP: **86.48.24.74**
- Operating System: Ubuntu 24.04 LTS (or compatible Linux)
- Architecture: x86_64
- Memory: Minimum 2GB RAM (4GB recommended)
- Storage: Minimum 20GB (for logs, artifacts, caching)

### Network Configuration

- **Ingress:** HTTPS (443) for artifact serving
- **Egress:** HTTPS (443) for source fetching
- **Internal:** No inter‑service communication required

---

## Deployment Requirements

### System Dependencies

```bash
# Required packages
sudo apt-get update
sudo apt-get install -y \
    python3.11 \
    python3-pip \
    nginx \
    systemd \
    git

# Python dependencies
pip3 install -r requirements.txt
```

### File System Layout

```
/opt/binary-rogue/
├── bin/
│   └── build           # Build executable
├── config/
│   └── sources.yaml    # Source configuration
├── logs/
│   └── builds/         # Build logs (rotated)
├── artifacts/
│   ├── current/        # Latest artifacts (served by nginx)
│   └── archive/        # Historical artifacts (optional)
└── cache/
    └── embeddings/     # Cached semantic vectors
```

### User and Permissions

```bash
# Create service user
sudo useradd -r -s /bin/false binary-rogue

# Set ownership
sudo chown -R binary-rogue:binary-rogue /opt/binary-rogue

# Set permissions
sudo chmod 755 /opt/binary-rogue/artifacts/current
sudo chmod 700 /opt/binary-rogue/config
```

---

## Configuration

### Environment Variables

```bash
# Required
export BR_CONFIG_PATH="/opt/binary-rogue/config/sources.yaml"
export BR_OUTPUT_DIR="/opt/binary-rogue/artifacts/current"
export BR_LOG_DIR="/opt/binary-rogue/logs"

# Optional
export BR_CACHE_DIR="/opt/binary-rogue/cache"
export BR_BUILD_TIMEOUT="90"
export BR_LOG_LEVEL="INFO"

# Secrets (source API keys)
export BR_SOURCE_API_KEY_NEWSAPI="sk-..."
export BR_SOURCE_API_KEY_TWITTER="..."
```

### Source Configuration

```yaml
# /opt/binary-rogue/config/sources.yaml
sources:
  - name: tech_news_rss
    type: rss
    url: https://example.com/tech/rss
    enabled: true
    
  - name: crypto_feed
    type: rss
    url: https://example.com/crypto/rss
    enabled: true
    
  - name: newsapi
    type: api
    endpoint: https://newsapi.org/v2/top-headlines
    auth:
      type: apikey
      env_var: BR_SOURCE_API_KEY_NEWSAPI
    enabled: true
```

---

## Service Management

### Systemd Service

```ini
# /etc/systemd/system/binary-rogue.service
[Unit]
Description=Binary-Rogue Build Service
After=network.target

[Service]
Type=oneshot
User=binary-rogue
Group=binary-rogue
WorkingDirectory=/opt/binary-rogue
EnvironmentFile=/opt/binary-rogue/config/env
ExecStart=/opt/binary-rogue/bin/build
StandardOutput=journal
StandardError=journal
SyslogIdentifier=binary-rogue

[Install]
WantedBy=multi-user.target
```

### Systemd Timer

```ini
# /etc/systemd/system/binary-rogue.timer
[Unit]
Description=Binary-Rogue Build Timer
Requires=binary-rogue.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=15min
Unit=binary-rogue.service

[Install]
WantedBy=timers.target
```

### Service Commands

```bash
# Enable and start timer
sudo systemctl enable binary-rogue.timer
sudo systemctl start binary-rogue.timer

# Check status
sudo systemctl status binary-rogue.timer
sudo systemctl list-timers binary-rogue.timer

# Manual build
sudo systemctl start binary-rogue.service

# View logs
sudo journalctl -u binary-rogue.service -f
```

---

## Web Server Configuration

### Nginx Configuration

```nginx
# /etc/nginx/sites-available/binary-rogue
server {
    listen 443 ssl http2;
    server_name binary-rogue.example.com;
    
    ssl_certificate /etc/letsencrypt/live/binary-rogue.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/binary-rogue.example.com/privkey.pem;
    
    root /opt/binary-rogue/artifacts/current;
    
    # CORS headers for frontend consumption
    add_header Access-Control-Allow-Origin "*";
    add_header Access-Control-Allow-Methods "GET, OPTIONS";
    
    # Cache control
    location /headlines.json {
        add_header Cache-Control "public, max-age=300"; # 5 minutes
        try_files $uri =404;
    }
    
    # Health check endpoint
    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }
    
    # Metrics endpoint (optional)
    location /metrics {
        alias /opt/binary-rogue/artifacts/current/metrics.json;
        add_header Cache-Control "no-cache";
    }
}
```

### SSL/TLS

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d binary-rogue.example.com

# Auto-renewal is configured automatically
```

---

## Logging

### Structured Log Format

All logs must be JSON with required fields:

```json
{
  "timestamp": "2026-01-18T14:30:15.234Z",
  "level": "INFO",
  "build_id": "20260118-1430-a3f7b2c1",
  "phase": "acquire",
  "message": "Fetched 127 signals from tech_news_rss",
  "metadata": {
    "source": "tech_news_rss",
    "signal_count": 127,
    "duration_ms": 2341
  }
}
```

### Log Levels

- **DEBUG** – Detailed diagnostic information
- **INFO** – Normal operational events
- **WARN** – Unexpected but handled situations
- **ERROR** – Errors that don't stop the build
- **CRITICAL** – Build failures requiring intervention

### Log Rotation

```bash
# /etc/logrotate.d/binary-rogue
/opt/binary-rogue/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0640 binary-rogue binary-rogue
}
```

---

## Monitoring

### Health Checks

**Endpoint:** `https://binary-rogue.example.com/health`

**Expected Response:**
```
HTTP/1.1 200 OK
Content-Type: text/plain

OK
```

**Monitoring Service:**
```bash
# Check health every minute
*/1 * * * * curl -sf https://binary-rogue.example.com/health || alert
```

### Metrics Endpoint

**Endpoint:** `https://binary-rogue.example.com/metrics.json`

**Response Format:**
```json
{
  "last_build": {
    "timestamp": "2026-01-18T14:30:00Z",
    "build_id": "20260118-1430-a3f7b2c1",
    "duration_ms": 28450,
    "signal_count": 427,
    "story_count": 156,
    "status": "success"
  },
  "uptime_seconds": 86400,
  "total_builds": 2341,
  "failed_builds": 12,
  "average_duration_ms": 25340
}
```

### Alerting Conditions

Alert when:

1. **Health check fails** (3 consecutive failures)
2. **Build duration > 60s** (3 consecutive builds)
3. **Build failure rate > 5%** (last 100 builds)
4. **Zero signals acquired** (2 consecutive builds)
5. **Artifact not updated** (> 30 minutes since last update)
6. **Disk space < 10%** (artifact directory)

### Monitoring Tools

Recommended:
- **Prometheus** + **Grafana** for metrics visualization
- **PagerDuty** or **OpsGenie** for alerting
- **Datadog** or **New Relic** for APM (optional)

---

## Backup and Recovery

### Artifact Retention

**Strategy:** Keep last 30 days of artifacts

```bash
# Daily cleanup cron job
0 2 * * * find /opt/binary-rogue/artifacts/archive -mtime +30 -delete
```

**Archive Structure:**
```
artifacts/archive/
├── 2026-01-18/
│   ├── 1430-headlines.json
│   ├── 1445-headlines.json
│   └── 1500-headlines.json
└── 2026-01-17/
    └── ...
```

### Backup Procedure

```bash
#!/bin/bash
# /opt/binary-rogue/bin/backup.sh

DATE=$(date +%Y-%m-%d)
BACKUP_DIR="/opt/binary-rogue/artifacts/archive/$DATE"

# Create archive directory
mkdir -p "$BACKUP_DIR"

# Copy current artifact
cp /opt/binary-rogue/artifacts/current/headlines.json \
   "$BACKUP_DIR/$(date +%H%M)-headlines.json"

# Compress old archives
find "$BACKUP_DIR" -name "*.json" -mtime +7 -exec gzip {} \;
```

### Recovery Procedures

**Scenario 1: Corrupted Artifact**
```bash
# Restore from last known good
cp /opt/binary-rogue/artifacts/archive/2026-01-18/1445-headlines.json \
   /opt/binary-rogue/artifacts/current/headlines.json
```

**Scenario 2: Failed Build**
```bash
# Check logs
sudo journalctl -u binary-rogue.service --since "10 minutes ago"

# Re-run manually
sudo systemctl start binary-rogue.service

# Monitor
sudo journalctl -u binary-rogue.service -f
```

**Scenario 3: Complete System Failure**
```bash
# Restore from off-site backup
rsync -avz backup-server:/backups/binary-rogue/latest/ /opt/binary-rogue/

# Verify configuration
/opt/binary-rogue/bin/build --validate-config

# Test build
/opt/binary-rogue/bin/build --dry-run

# Resume service
sudo systemctl start binary-rogue.timer
```

---

## Performance Optimization

### Caching Strategy

**Semantic Embeddings:**
```bash
# Cache directory
/opt/binary-rogue/cache/embeddings/
├── abc123.npy    # Cached embedding for signal hash
└── def456.npy
```

**Cache Policy:**
- TTL: 7 days
- Max size: 5GB
- Eviction: LRU

### Resource Limits

```ini
# /etc/systemd/system/binary-rogue.service
[Service]
MemoryMax=4G
CPUQuota=200%
TasksMax=100
```

### Concurrent Source Fetching

```yaml
# config/sources.yaml
parallel_fetch: 5  # Fetch from 5 sources concurrently
timeout_per_source: 10  # 10 second timeout per source
```

---

## Security

### Secrets Management

**Never commit secrets to git.**

Store in environment file:
```bash
# /opt/binary-rogue/config/env
# chmod 600, owned by binary-rogue user
BR_SOURCE_API_KEY_NEWSAPI=sk-...
BR_SOURCE_API_KEY_TWITTER=...
```

### Network Security

```bash
# Firewall rules (UFW)
sudo ufw allow 443/tcp
sudo ufw enable

# Rate limiting (nginx)
limit_req_zone $binary_remote_addr zone=api:10m rate=60r/m;
limit_req zone=api burst=10 nodelay;
```

### Dependency Auditing

```bash
# Monthly security audit
pip-audit --requirement requirements.txt

# Update dependencies
pip install --upgrade -r requirements.txt
```

---

## Troubleshooting

### Common Issues

**Build Timeout:**
```bash
# Increase timeout
export BR_BUILD_TIMEOUT=120

# Check slow sources
grep "duration_ms" /opt/binary-rogue/logs/latest.log | sort -k duration_ms
```

**High Memory Usage:**
```bash
# Monitor memory
watch -n 1 'systemctl status binary-rogue.service | grep Memory'

# Reduce cache size
export BR_CACHE_MAX_SIZE_GB=2
```

**Source Connection Failures:**
```bash
# Test source manually
curl -v https://example.com/rss

# Check DNS
dig example.com

# Check firewall
sudo iptables -L -n
```

### Debug Mode

```bash
# Enable debug logging
export BR_LOG_LEVEL=DEBUG

# Run interactively
sudo -u binary-rogue /opt/binary-rogue/bin/build --verbose
```

---

## Maintenance

### Regular Tasks

**Daily:**
- Monitor build success rate
- Check disk space
- Review error logs

**Weekly:**
- Review performance metrics
- Check for slow sources
- Audit security logs

**Monthly:**
- Update dependencies
- Review configuration
- Test backup restoration
- Capacity planning

### Upgrade Procedure

```bash
# 1. Backup current version
sudo cp -r /opt/binary-rogue /opt/binary-rogue.backup

# 2. Stop service
sudo systemctl stop binary-rogue.timer

# 3. Deploy new version
sudo rsync -avz new-version/ /opt/binary-rogue/

# 4. Validate configuration
/opt/binary-rogue/bin/build --validate-config

# 5. Test build
/opt/binary-rogue/bin/build --dry-run

# 6. Start service
sudo systemctl start binary-rogue.timer

# 7. Monitor
sudo journalctl -u binary-rogue.service -f
```

---

## Boundaries

Operations define how the system runs and must not redefine:
- Semantic meaning of data
- Evaluator interfaces or behavior
- Schema structure
- Determinism guarantees

Operational changes should be implementation details invisible to specification consumers.
