# UTM Shortener Setup Guide

This guide will help you set up the UTM Shortener for your own domain and start tracking campaigns.

## Initial Setup

### 1. Install the App
```bash
bench get-app https://github.com/chinmaybhatk/utm_shortener.git
bench --site your-site-name install-app utm_shortener
bench migrate
```

### 2. Configure Domain Settings

1. Go to **UTM Shortener Settings** (use the search bar)
2. Configure the following:

#### Domain Configuration
- **Short Domain**: Enter your domain (e.g., `yourdomain.com` or `link.yourdomain.com`)
  - If using a subdomain, make sure it's configured in your DNS
  - Example: `link.example.com` or just `example.com`
- **Use HTTPS**: Check if your domain has SSL certificate
- **Custom Domain Enabled**: Check if using a different domain than your ERPNext instance

#### Example Configurations:

**Option 1: Using Main Domain**
```
Short Domain: example.com
Use HTTPS: ✓
Custom Domain Enabled: ☐
```
Your short URLs will be: `https://example.com/s/abc123`

**Option 2: Using Subdomain**
```
Short Domain: link.example.com
Use HTTPS: ✓
Custom Domain Enabled: ✓
```
Your short URLs will be: `https://link.example.com/s/abc123`

**Option 3: Using Different Domain**
```
Short Domain: short.link
Use HTTPS: ✓
Custom Domain Enabled: ✓
```
Your short URLs will be: `https://short.link/s/abc123`

### 3. Configure Web Server

Add the following to your nginx configuration to handle short URL redirects:

```nginx
# For subdomain setup (link.example.com)
server {
    server_name link.example.com;
    
    location /s/ {
        proxy_pass http://your-erpnext-server;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# For main domain setup (add to existing server block)
location /s/ {
    proxy_pass http://your-erpnext-server;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## Creating Your First Campaign

### Step 1: Create a UTM Campaign

```python
# Via Script
campaign = frappe.get_doc({
    "doctype": "UTM Campaign",
    "campaign_name": "Summer Sale 2024",
    "utm_source": "email",
    "utm_medium": "newsletter",
    "utm_campaign": "summer-sale-2024",
    "utm_term": "discount",
    "utm_content": "header-banner",
    "description": "Summer promotional campaign via email newsletter"
}).insert()

print(f"Campaign created: {campaign.name}")
```

Or use the UI:
1. Go to **UTM Campaign** list
2. Click **New**
3. Fill in the campaign details
4. Save

### Step 2: Create Short URLs

```python
# Create a short URL for the campaign
short_url = frappe.get_doc({
    "doctype": "Short URL",
    "original_url": "https://example.com/products/summer-collection",
    "utm_campaign": campaign.name,
    "custom_alias": "summer-sale"  # Optional
}).insert()

print(f"Short URL created: {short_url.short_url}")
# Output: https://link.example.com/s/summer-sale
```

### Step 3: Generate Multiple URLs for Different Channels

```python
# Create URLs for different channels
channels = [
    {"url": "https://example.com/products", "alias": "summer-products"},
    {"url": "https://example.com/offers", "alias": "summer-offers"},
    {"url": "https://example.com/new-arrivals", "alias": "summer-new"}
]

for channel in channels:
    frappe.get_doc({
        "doctype": "Short URL",
        "original_url": channel["url"],
        "utm_campaign": campaign.name,
        "custom_alias": channel["alias"]
    }).insert()
```

## Tracking Analytics

### Real-time Click Tracking
When someone clicks your short URL:
1. They're redirected to the destination with UTM parameters
2. The click is logged with:
   - Timestamp
   - IP address (for geographic data)
   - Browser and device information
   - Referrer (where they came from)

### Viewing Analytics

#### Via API:
```python
# Get URL analytics
analytics = frappe.call(
    'utm_shortener.utm_shortener.api.get_url_analytics',
    short_code='summer-sale'
)

print(f"Total Clicks: {analytics['short_url']['total_clicks']}")
print(f"Recent Clicks: {analytics['recent_clicks']}")

# Get campaign analytics
campaign_analytics = frappe.call(
    'utm_shortener.utm_shortener.api.get_campaign_analytics',
    campaign_id=campaign.name
)

print(f"Campaign Performance:")
print(f"Total Clicks: {campaign_analytics['analytics']['total_clicks']}")
print(f"Unique Visitors: {campaign_analytics['analytics']['unique_visitors']}")
print(f"Top Sources: {campaign_analytics['source_breakdown']}")
```

#### Via UI:
1. Go to **UTM Campaign** list
2. Open your campaign
3. View the analytics dashboard

## Advanced Features

### 1. Bulk Import URLs
Create a CSV file with columns: `url`, `custom_alias`
```csv
url,custom_alias
https://example.com/product-1,prod1-summer
https://example.com/product-2,prod2-summer
https://example.com/category/summer,cat-summer
```

Then import using Data Import Tool.

### 2. QR Codes
Each short URL automatically generates a QR code:
```python
short_url_doc = frappe.get_doc("Short URL", {"short_code": "summer-sale"})
qr_code_base64 = short_url_doc.qr_code
# Use this in your marketing materials
```

### 3. URL Expiration
Set URLs to expire after campaigns end:
```python
frappe.get_doc({
    "doctype": "Short URL",
    "original_url": "https://example.com/limited-offer",
    "utm_campaign": campaign.name,
    "custom_alias": "limited-time",
    "expiry_date": "2024-08-31"
}).insert()
```

### 4. API Integration
Use the REST API for external integrations:

```bash
# Create short URL via API
curl -X POST https://your-site.com/api/method/utm_shortener.utm_shortener.api.create_short_url \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://example.com/page",
    "utm_campaign": "campaign-id",
    "custom_alias": "my-link"
  }'
```

## Understanding Analytics

### Conversion Sources
The system tracks where visitors come from:
- **Direct**: Typed URL or bookmark
- **Social Media**: Facebook, Twitter, LinkedIn, etc.
- **Search Engines**: Google, Bing, etc.
- **Email**: Email clients
- **Other Websites**: Referral traffic

### Geographic Data
- Country-level tracking (requires GeoIP integration)
- Useful for regional campaign optimization

### Device Analytics
- **Device Type**: Desktop, Mobile, Tablet
- **Browser**: Chrome, Firefox, Safari, etc.
- **Operating System**: Windows, macOS, iOS, Android, etc.

## Best Practices

1. **Consistent Naming**: Use a naming convention for campaigns and aliases
   - Example: `{year}-{season}-{channel}-{content}`
   - `2024-summer-email-header`

2. **UTM Parameter Standards**:
   - **utm_source**: Where the traffic comes from (google, newsletter, facebook)
   - **utm_medium**: Marketing medium (cpc, email, social)
   - **utm_campaign**: Campaign name (summer-sale-2024)
   - **utm_term**: Paid keywords (optional)
   - **utm_content**: Differentiate similar content (header-link, footer-link)

3. **Regular Monitoring**: Check analytics weekly to optimize campaigns

4. **Clean Up**: Archive or delete expired campaigns to keep data organized

## Troubleshooting

### URLs Not Redirecting
1. Check if nginx/web server is configured correctly
2. Verify the short URL status is "Active"
3. Check if URL has expired
4. Review error logs: `bench --site your-site-name console`

### Analytics Not Showing
1. Ensure URL Click Log DocType has proper permissions
2. Check if scheduled jobs are running: `bench doctor`
3. Verify tracking code is working in browser console

### Domain Not Working
1. Verify DNS settings for custom domain
2. Check SSL certificate is valid
3. Ensure domain is configured in UTM Shortener Settings
4. Test with curl: `curl -I https://your-domain.com/s/test`

## Integration Examples

### Email Marketing
```html
<!-- In your email template -->
<a href="https://link.yourdomain.com/s/summer-header">
  Shop Summer Collection
</a>
```

### Social Media
```
Check out our summer sale! 
👉 https://link.yourdomain.com/s/summer-social
```

### Print Materials
Include QR codes generated by the system for offline-to-online tracking.

## Support

For issues or questions:
1. Check the [GitHub Issues](https://github.com/chinmaybhatk/utm_shortener/issues)
2. Review error logs in your ERPNext instance
3. Ensure all DocTypes are properly installed
