# UTM Shortener Deployment Guide

This guide will help you deploy the UTM Shortener to production and configure it for optimal performance.

## Pre-Deployment Checklist

- [ ] Frappe/ERPNext v14+ installed
- [ ] Domain/subdomain configured with DNS
- [ ] SSL certificate installed
- [ ] Backup of existing data
- [ ] Nginx/Apache configured

## Step 1: Install the Application

### 1.1 Get the App
```bash
cd ~/frappe-bench
bench get-app https://github.com/chinmaybhatk/utm_shortener.git --branch main
```

### 1.2 Install on Site
```bash
bench --site your-site.com install-app utm_shortener
bench --site your-site.com migrate
```

### 1.3 Clear Cache
```bash
bench --site your-site.com clear-cache
bench --site your-site.com clear-website-cache
```

## Step 2: Configure Domain Settings

### 2.1 Access Settings
1. Login to your ERPNext instance
2. Search for "UTM Shortener Settings"
3. Configure the following:

```
Short Domain: link.yourdomain.com
Use HTTPS: ✓ (checked)
Custom Domain Enabled: ✓ (checked)
Rate Limit per Hour: 1000
Bulk Create Limit: 100
Analytics Retention Days: 365
Enable Geo Tracking: ✓ (checked)
```

### 2.2 Save Settings
Click "Save" to apply the configuration.

## Step 3: Configure Web Server

### 3.1 Nginx Configuration

Add this to your nginx configuration file:

```nginx
# For subdomain setup (e.g., link.yourdomain.com)
server {
    listen 80;
    server_name link.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name link.yourdomain.com;
    
    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /s/ {
        proxy_pass http://localhost:8000/s/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Cache control for redirects
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        add_header Expires "0";
    }
}
```

### 3.2 Apache Configuration

If using Apache:

```apache
<VirtualHost *:80>
    ServerName link.yourdomain.com
    Redirect permanent / https://link.yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName link.yourdomain.com
    
    SSLEngine on
    SSLCertificateFile /path/to/ssl/cert.pem
    SSLCertificateKeyFile /path/to/ssl/key.pem
    
    ProxyPreserveHost On
    ProxyPass / http://localhost:8000/
    ProxyPassReverse / http://localhost:8000/
    
    <Location /s/>
        ProxyPass http://localhost:8000/s/
        ProxyPassReverse http://localhost:8000/s/
        Header set Cache-Control "no-cache, no-store, must-revalidate"
        Header set Pragma "no-cache"
        Header set Expires "0"
    </Location>
</VirtualHost>
```

### 3.3 Reload Web Server
```bash
# For Nginx
sudo nginx -t
sudo systemctl reload nginx

# For Apache
sudo apache2ctl configtest
sudo systemctl reload apache2
```

## Step 4: Set Up Scheduled Tasks

Ensure scheduled tasks are running:

```bash
bench --site your-site.com enable-scheduler
bench --site your-site.com doctor
```

Check scheduled tasks:
```bash
bench --site your-site.com show-config | grep scheduler
```

## Step 5: Run Tests

### 5.1 Run Test Script
```bash
bench --site your-site.com console
```

In the console:
```python
from utm_shortener.tests.test_utm_shortener import test_utm_shortener
test_utm_shortener()
```

### 5.2 Manual Testing
1. Create a test campaign
2. Generate a short URL
3. Access the short URL in a browser
4. Verify redirect works
5. Check analytics are recorded

## Step 6: Performance Optimization

### 6.1 Enable Redis Cache
Ensure Redis is configured in your site config:

```bash
bench --site your-site.com set-config cache_backend "redis"
```

### 6.2 Database Indexes
Run the following SQL to add indexes for better performance:

```sql
-- Add indexes for URL Click Log
CREATE INDEX idx_short_url_timestamp ON `tabURL Click Log` (short_url, timestamp);
CREATE INDEX idx_referrer_source ON `tabURL Click Log` (referrer_source);
CREATE INDEX idx_device_type ON `tabURL Click Log` (device_type);

-- Add indexes for Short URL
CREATE INDEX idx_short_code ON `tabShort URL` (short_code);
CREATE INDEX idx_utm_campaign ON `tabShort URL` (utm_campaign);
CREATE INDEX idx_status_expiry ON `tabShort URL` (status, expiry_date);
```

### 6.3 Configure GeoIP (Optional)
For geographic tracking:

1. Install GeoIP database:
```bash
sudo apt-get install geoip-database
pip install geoip2
```

2. Update the `get_country_from_ip` method in Short URL model

## Step 7: Security Configuration

### 7.1 Rate Limiting
Configure fail2ban for additional protection:

```bash
sudo nano /etc/fail2ban/filter.d/utm-shortener.conf
```

Add:
```ini
[Definition]
failregex = ^<HOST> .* "GET /s/.* HTTP/.*" 404
ignoreregex =
```

### 7.2 Firewall Rules
If using UFW:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

## Step 8: Monitoring Setup

### 8.1 Log Monitoring
Monitor redirect logs:
```bash
tail -f ~/frappe-bench/logs/web.*.log | grep "/s/"
```

### 8.2 Error Monitoring
Check for errors:
```bash
tail -f ~/frappe-bench/logs/web.error.log
```

### 8.3 Analytics Monitoring
Create a monitoring script:

```python
# monitoring.py
import frappe

def check_utm_health():
    # Check recent clicks
    recent_clicks = frappe.db.count("URL Click Log", {
        "timestamp": [">=", frappe.utils.add_days(frappe.utils.now(), -1)]
    })
    
    # Check active URLs
    active_urls = frappe.db.count("Short URL", {"status": "Active"})
    
    # Check error rate
    errors = frappe.db.count("Error Log", {
        "method": ["like", "%utm_shortener%"],
        "creation": [">=", frappe.utils.add_days(frappe.utils.now(), -1)]
    })
    
    print(f"Health Check:")
    print(f"- Recent Clicks (24h): {recent_clicks}")
    print(f"- Active URLs: {active_urls}")
    print(f"- Errors (24h): {errors}")
    
    return {
        "recent_clicks": recent_clicks,
        "active_urls": active_urls,
        "errors": errors,
        "status": "healthy" if errors < 10 else "needs_attention"
    }
```

## Step 9: Backup Configuration

### 9.1 Database Backup
Add UTM tables to backup routine:
```bash
# Add to backup script
mysqldump -u root -p your_database \
  tabShort\ URL \
  tabUTM\ Campaign \
  tabURL\ Click\ Log \
  tabUTM\ Template \
  tabUTM\ Shortener\ Settings \
  > utm_backup_$(date +%Y%m%d).sql
```

### 9.2 Automated Backups
Create a cron job:
```bash
crontab -e
```

Add:
```
0 2 * * * /home/frappe/backup_utm.sh
```

## Step 10: Go Live Checklist

- [ ] Domain DNS configured and propagated
- [ ] SSL certificate valid and installed
- [ ] Web server configuration tested
- [ ] Short URL redirect tested
- [ ] Analytics tracking verified
- [ ] Rate limiting configured
- [ ] Backup system in place
- [ ] Monitoring alerts set up
- [ ] Documentation provided to team

## Troubleshooting

### Short URLs Not Working
1. Check nginx/apache logs
2. Verify DNS propagation: `dig link.yourdomain.com`
3. Test with curl: `curl -I https://link.yourdomain.com/s/test`
4. Check Frappe logs: `bench --site your-site.com console`

### Analytics Not Recording
1. Check scheduler status: `bench doctor`
2. Verify permissions on URL Click Log
3. Check browser console for JavaScript errors
4. Review server logs for tracking errors

### Performance Issues
1. Check database indexes
2. Monitor Redis cache hit rate
3. Review nginx access logs for patterns
4. Consider CDN for static assets

## Support

For deployment issues:
1. Check error logs in `~/frappe-bench/logs/`
2. Review [GitHub Issues](https://github.com/chinmaybhatk/utm_shortener/issues)
3. Enable debug mode temporarily: `bench --site your-site.com set-config developer_mode 1`
