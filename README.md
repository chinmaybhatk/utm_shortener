# UTM Link Shortener

A comprehensive Frappe app for UTM parameter generation and URL shortening with advanced analytics.

## 🚀 Features

### 🔗 URL Shortening
- Generate short, memorable URLs
- Custom aliases support
- Bulk URL creation
- Expiration date management
- Domain blocking for security

### 📊 UTM Parameter Management
- Complete UTM parameter builder
- Template system for reusable campaigns
- Automatic URL generation with UTM parameters
- Campaign code generation

### 📈 Advanced Analytics
- Real-time click tracking
- Device type detection (Desktop/Mobile/Tablet)
- Browser and OS identification
- Geolocation tracking (optional)
- Country-wise analytics
- Unique visitor counting

### 🛡️ Security Features
- Rate limiting
- Domain blocking
- URL validation
- Malicious URL detection
- Permission-based access control

## 🔧 Installation

### Prerequisites
- Frappe Framework (v14+)
- ERPNext (optional but recommended)

### Setup
1. Clone this repository to your Frappe bench apps folder:
```bash
cd frappe-bench/apps
git clone https://github.com/chinmaybhatk/utm_shortener.git
```

2. Install the app to your site:
```bash
bench --site your-site.local install-app utm_shortener
```

3. Run database migrations:
```bash
bench --site your-site.local migrate
```

4. Create the required DocTypes manually:
   - UTM Campaign
   - Short URL
   - URL Click Log
   - UTM Template
   - UTM Shortener Settings (Single DocType)

5. Configure settings:
   - Go to UTM Shortener Settings
   - Set your base domain
   - Configure rate limits
   - Enable geolocation if needed

## 📚 Quick Start

### Creating a UTM Campaign
1. Navigate to **UTM Campaign** in the desk
2. Click **New**
3. Fill in campaign details:
   - Campaign Name: "Summer Sale 2025"
   - UTM Source: "email"
   - UTM Medium: "newsletter"
   - UTM Campaign: "summer_sale_2025"
4. Save

### Creating Short URLs
1. Go to **Short URL** in the desk
2. Click **New**
3. Enter your original URL
4. Select a UTM Campaign (optional)
5. Add custom alias (optional)
6. Save

## 🔌 API Usage

### Create Short URL
```python
import requests

response = requests.post('https://yoursite.com/api/method/utm_shortener.utm_shortener.api.create_short_url', {
    'original_url': 'https://example.com/product',
    'utm_campaign': 'summer_sale_campaign',
    'custom_alias': 'summer-sale'
})

data = response.json()
print(data['message']['short_url'])
```

### Get Analytics
```python
response = requests.get('https://yoursite.com/api/method/utm_shortener.utm_shortener.api.get_url_analytics', {
    'short_code': 'abc123'
})

analytics = response.json()['message']
print(f"Total clicks: {analytics['short_url']['total_clicks']}")
```

### Bulk Create URLs
```python
import json

urls = [
    {"url": "https://shop.com/laptops", "alias": "laptops"},
    {"url": "https://shop.com/phones", "alias": "phones"}
]

response = requests.post('https://yoursite.com/api/method/utm_shortener.utm_shortener.api.bulk_create_utm_urls', {
    'campaign': 'summer_sale_campaign',
    'url_list': json.dumps(urls)
})
```

## 📊 DocTypes

### UTM Campaign
Main campaign management with UTM parameters.
**Fields:**
- Campaign Name (Data, Required)
- Campaign Code (Data, Auto-generated, Unique)
- UTM Source (Data, Required)
- UTM Medium (Select: email, social, cpc, etc.)
- UTM Campaign (Data, Required)
- UTM Term (Data, Optional)
- UTM Content (Data, Optional)
- Description (Text Editor)
- Status (Select: Active, Inactive, Completed)
- Start Date/End Date

### Short URL
Individual shortened URLs with tracking.
**Fields:**
- Short Code (Data, Required, Unique, Auto-generated)
- Original URL (Long Text, Required)
- Short URL (Data, Read-only, Auto-generated)
- UTM Campaign (Link: UTM Campaign, Optional)
- Generated UTM URL (Long Text, Read-only)
- Custom Alias (Data, Optional, Unique)
- Total Clicks (Int, Default: 0, Read-only)
- Status (Select: Active, Inactive, Expired)
- Expiry Date (Date, Optional)
- Last Accessed (Datetime, Read-only)

### URL Click Log
Detailed click tracking records.
**Fields:**
- Short URL (Link: Short URL, Required)
- Timestamp (Datetime, Default: now)
- IP Address (Data)
- User Agent (Long Text)
- Referrer URL (Long Text)
- Country (Data)
- City (Data)
- Device Type (Select: Desktop, Mobile, Tablet, Unknown)
- Browser (Data)
- Operating System (Data)

### UTM Template
Reusable UTM parameter templates.
**Fields:**
- Template Name (Data, Required)
- Template Code (Data, Auto-generated)
- UTM Source/Medium (Data, Required)
- UTM Campaign/Term/Content Templates (Data)
- Description (Text)
- Is Active (Check, Default: 1)

### UTM Shortener Settings (Single DocType)
System-wide configuration.
**Fields:**
- Base Domain (Data, Default: "short.ly")
- Use HTTPS (Check, Default: 1)
- Default Expiry Days (Int, Default: 365)
- Rate Limit Per Hour (Int, Default: 100)
- Enable Geolocation (Check)
- Geolocation API Key (Password)
- Blocked Domains (Long Text)

## 🔒 Permissions

The app includes role-based permissions:
- **UTM Manager**: Full access to all features
- **UTM User**: Create and manage own URLs
- **UTM Viewer**: Read-only access to analytics

## ⏰ Scheduled Tasks

### Daily Tasks
- **cleanup_expired_urls**: Mark expired URLs as inactive
- **update_geolocation_data**: Update location data for recent clicks

### Hourly Tasks
- **reset_rate_limits**: Reset user rate limiting counters

## 🎨 Customization

### Adding Custom Fields
You can extend the doctypes with custom fields:

```python
# Add custom field to UTM Campaign
custom_field = {
    "dt": "UTM Campaign",
    "properties": [
        {
            "fieldname": "budget",
            "label": "Campaign Budget",
            "fieldtype": "Currency"
        }
    ]
}
```

## 🐛 Troubleshooting

### Common Issues

#### Short URLs not redirecting
- Check website route configuration in hooks.py
- Ensure the app is installed and migrated
- Verify domain settings

#### Rate limiting issues
- Check UTM Shortener Settings
- Adjust rate_limit_per_hour value

#### Analytics not tracking
- Verify click logs are being created
- Check browser restrictions
- Ensure proper permissions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Development Setup
```bash
# Install in development mode
bench get-app utm_shortener /path/to/local/repo
bench --site dev.local install-app utm_shortener
bench --site dev.local migrate
```

## 📄 License

MIT License - see LICENSE file for details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/chinmaybhatk/utm_shortener/issues)
- **Discussions**: [GitHub Discussions](https://github.com/chinmaybhatk/utm_shortener/discussions)

## 📝 Changelog

### v1.0.0
- Initial release
- Core URL shortening functionality
- UTM parameter generation
- Basic analytics
- API endpoints

---

**Made with ❤️ for the Frappe community**