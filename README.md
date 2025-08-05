# UTM Shortener Enhanced

An advanced UTM tracking and URL shortening solution for Frappe/ERPNext that provides Bitly-like functionality with powerful analytics.

## Features

### Core Features
- **URL Shortening**: Create short URLs with custom aliases or auto-generated codes
- **UTM Campaign Management**: Organize URLs by campaigns with full UTM parameter support
- **Click Tracking**: Track every click with detailed analytics
- **Custom Domains**: Support for custom short domains
- **Bulk Operations**: Create multiple short URLs at once
- **Rate Limiting**: Prevent abuse with configurable rate limits
- **URL Expiration**: Set expiration dates for temporary links
- **QR Code Generation**: Auto-generate QR codes for short URLs

### Analytics Features
- **Real-time Click Tracking**: Monitor clicks as they happen
- **Geographic Analytics**: Track visitor locations
- **Device & Browser Analytics**: Understand your audience's technology
- **Referrer Tracking**: See where your traffic comes from
- **Conversion Source Analysis**: Track which UTM sources drive the most traffic
- **Campaign Performance**: Comprehensive campaign-level analytics

## Installation

```bash
bench get-app https://github.com/chinmaybhatk/utm_shortener.git
bench --site your-site-name install-app utm_shortener
```

## Configuration

### 1. UTM Shortener Settings
Navigate to **UTM Shortener Settings** to configure:
- Default short domain
- Rate limits per hour
- URL expiration defaults
- Analytics retention period

### 2. Setting Up Short URL Routing
The app automatically sets up routing for short URLs at `/s/{short_code}`

## Usage

### Creating a UTM Campaign

```python
import frappe

# Create a new UTM campaign
result = frappe.call('utm_shortener.utm_shortener.api.create_utm_campaign',
    campaign_name='Walue.biz Social Media Launch',
    utm_source='social',
    utm_medium='post',
    utm_campaign='walue-launch-2024',
    utm_term='business-solution',
    utm_content='announcement',
    description='Launch campaign for Walue.biz on social media'
)

print(f"Campaign ID: {result['campaign_id']}")
```

### Creating Short URLs

#### Via API
```python
# Create a short URL with custom alias
result = frappe.call('utm_shortener.utm_shortener.api.create_short_url',
    original_url='https://walue.biz/features',
    utm_campaign='4bs459tanr',  # Campaign ID
    custom_alias='walue-social',
    expiry_date='2024-12-31'
)

print(f"Short URL: {result['short_url']}")
# Output: https://meta-app.frappe.cloud/s/walue-social
```

#### Via Web Interface
1. Navigate to the public URL shortener page at `/utm-shortener`
2. Enter your long URL
3. Select a campaign (optional)
4. Add a custom alias (optional)
5. Set expiration date (optional)
6. Click "Shorten URL"

### Bulk URL Creation

```python
# Create multiple URLs for a campaign
urls = [
    {"url": "https://walue.biz/pricing", "alias": "walue-pricing"},
    {"url": "https://walue.biz/demo", "alias": "walue-demo"},
    {"url": "https://walue.biz/contact"}  # Auto-generated alias
]

result = frappe.call('utm_shortener.utm_shortener.api.bulk_create_utm_urls',
    campaign='4bs459tanr',
    url_list=urls
)

print(f"Created {result['created_count']} URLs")
```

### Accessing Analytics

#### URL Analytics
```python
# Get analytics for a specific short URL
analytics = frappe.call('utm_shortener.utm_shortener.api.get_url_analytics',
    short_code='walue-social'
)

print(f"Total Clicks: {analytics['short_url']['total_clicks']}")
print(f"Recent Clicks: {analytics['recent_clicks']}")
```

#### Campaign Analytics
```python
# Get campaign-level analytics
campaign_data = frappe.call('utm_shortener.utm_shortener.api.get_campaign_analytics',
    campaign_id='4bs459tanr'
)

print(f"Total Campaign Clicks: {campaign_data['analytics']['total_clicks']}")
print(f"Unique Visitors: {campaign_data['analytics']['unique_visitors']}")
print(f"Top Sources: {campaign_data['source_breakdown']}")
```

## DocTypes

### 1. UTM Campaign
- Stores campaign information
- Links to multiple short URLs
- Tracks overall campaign performance

### 2. Short URL
- Individual shortened URLs
- Tracks clicks and analytics
- Supports custom aliases and expiration

### 3. URL Click Log
- Records every click event
- Stores visitor information
- Powers analytics reports

### 4. UTM Template
- Reusable UTM parameter sets
- Quick campaign creation

### 5. UTM Shortener Settings
- Global configuration
- Rate limiting settings
- Default values

## API Reference

### Public APIs (No Authentication Required)
- `redirect_short_url(short_code)`: Handles short URL redirects

### Authenticated APIs

#### create_utm_campaign
Create a new UTM campaign
```python
create_utm_campaign(
    campaign_name: str,
    utm_source: str,
    utm_medium: str,
    utm_campaign: str,
    utm_term: str = None,
    utm_content: str = None,
    description: str = None
)
```

#### create_short_url
Create a single short URL
```python
create_short_url(
    original_url: str,
    utm_campaign: str = None,
    custom_alias: str = None,
    expiry_date: str = None
)
```

#### bulk_create_utm_urls
Create multiple short URLs
```python
bulk_create_utm_urls(
    campaign: str,
    url_list: List[dict]
)
```

#### get_url_analytics
Get analytics for a short URL
```python
get_url_analytics(short_code: str)
```

#### get_campaign_analytics
Get analytics for an entire campaign
```python
get_campaign_analytics(campaign_id: str)
```

## Testing Short URLs

After creating a short URL, test it by:
1. Opening the short URL in a browser: `https://your-domain.com/s/your-alias`
2. Checking that it redirects to the correct destination
3. Verifying that the click is tracked in analytics

## Scheduled Tasks

The app includes scheduled tasks for:
- **Daily**: Clean up expired URLs
- **Hourly**: Reset rate limits

## Security Features

- Rate limiting to prevent abuse
- Permission-based access control
- IP tracking for security analysis
- Automatic URL validation

## Best Practices

1. **Use Descriptive Aliases**: Make short codes memorable and relevant
2. **Set Expiration Dates**: For time-sensitive campaigns
3. **Monitor Analytics**: Regular review of click patterns
4. **Organize by Campaigns**: Group related URLs together
5. **Test Before Sharing**: Always test short URLs before distribution

## Troubleshooting

### Short URL Not Redirecting
1. Check if the URL status is "Active"
2. Verify the URL hasn't expired
3. Ensure the short code is correct
4. Check server logs for errors

### Analytics Not Updating
1. Verify URL Click Log doctype permissions
2. Check if scheduled tasks are running
3. Review error logs

### Rate Limit Issues
1. Check UTM Shortener Settings
2. Adjust rate limits as needed
3. Monitor usage patterns

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and feature requests, please use the [GitHub Issues](https://github.com/chinmaybhatk/utm_shortener/issues) page.
