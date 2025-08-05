# UTM Shortener Settings DocType Updates

## New Fields Required:

### Domain Configuration
1. **short_domain** (Data)
   - Label: "Short Domain"
   - Description: "Your short domain (e.g., yourdomain.com or short.yourdomain.com)"
   - Default: Site URL
   - Example: "example.com" or "link.example.com"

2. **use_https** (Check)
   - Label: "Use HTTPS"
   - Description: "Use HTTPS for short URLs"
   - Default: 1

3. **custom_domain_enabled** (Check)
   - Label: "Custom Domain Enabled"
   - Description: "Enable if using a custom short domain different from main site"
   - Default: 0

4. **fallback_to_site_url** (Check)
   - Label: "Fallback to Site URL"
   - Description: "Use site URL if custom domain is not configured"
   - Default: 1

### Analytics Configuration
5. **enable_geo_tracking** (Check)
   - Label: "Enable Geographic Tracking"
   - Description: "Track visitor locations (requires GeoIP)"
   - Default: 1

6. **analytics_retention_days** (Int)
   - Label: "Analytics Retention (Days)"
   - Description: "How long to keep click logs"
   - Default: 365

### Rate Limiting
7. **rate_limit_per_hour** (Int)
   - Label: "Rate Limit per Hour"
   - Description: "Maximum URLs per user per hour"
   - Default: 100

8. **bulk_create_limit** (Int)
   - Label: "Bulk Create Limit"
   - Description: "Maximum URLs in one bulk operation"
   - Default: 50
