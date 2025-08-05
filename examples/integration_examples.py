"""
UTM Shortener Integration Examples
This script shows how to integrate the UTM Shortener with various platforms
"""

import requests
import json
from datetime import datetime, timedelta

class UTMShortenerClient:
    """Client for interacting with UTM Shortener API"""
    
    def __init__(self, site_url, api_key, api_secret):
        self.site_url = site_url.rstrip('/')
        self.api_key = api_key
        self.api_secret = api_secret
        self.headers = {
            'Authorization': f'token {api_key}:{api_secret}',
            'Content-Type': 'application/json'
        }
    
    def create_campaign(self, campaign_data):
        """Create a new UTM campaign"""
        endpoint = f"{self.site_url}/api/method/utm_shortener.utm_shortener.api.create_utm_campaign"
        response = requests.post(endpoint, json=campaign_data, headers=self.headers)
        return response.json()
    
    def create_short_url(self, url_data):
        """Create a short URL"""
        endpoint = f"{self.site_url}/api/method/utm_shortener.utm_shortener.api.create_short_url"
        response = requests.post(endpoint, json=url_data, headers=self.headers)
        return response.json()
    
    def bulk_create_urls(self, campaign_id, urls):
        """Create multiple URLs at once"""
        endpoint = f"{self.site_url}/api/method/utm_shortener.utm_shortener.api.bulk_create_utm_urls"
        data = {
            "campaign": campaign_id,
            "url_list": urls
        }
        response = requests.post(endpoint, json=data, headers=self.headers)
        return response.json()
    
    def get_analytics(self, campaign_id):
        """Get campaign analytics"""
        endpoint = f"{self.site_url}/api/method/utm_shortener.utm_shortener.api.get_campaign_analytics"
        data = {"campaign_id": campaign_id}
        response = requests.post(endpoint, json=data, headers=self.headers)
        return response.json()

# Example 1: Email Marketing Integration
def email_marketing_example():
    """Example: Create tracked URLs for email campaign"""
    
    client = UTMShortenerClient(
        site_url="https://your-site.com",
        api_key="your_api_key",
        api_secret="your_api_secret"
    )
    
    # Create campaign for email newsletter
    campaign = client.create_campaign({
        "campaign_name": "Summer Newsletter 2024",
        "utm_source": "email",
        "utm_medium": "newsletter",
        "utm_campaign": "summer-2024",
        "utm_content": "header",
        "description": "Monthly newsletter featuring summer products"
    })
    
    if campaign["success"]:
        campaign_id = campaign["campaign_id"]
        
        # Create URLs for different sections
        urls = [
            {"url": "https://example.com/summer-collection", "alias": "summer-main"},
            {"url": "https://example.com/swimwear", "alias": "summer-swim"},
            {"url": "https://example.com/outdoor-gear", "alias": "summer-outdoor"},
            {"url": "https://example.com/sale", "alias": "summer-sale"}
        ]
        
        result = client.bulk_create_urls(campaign_id, urls)
        
        print("Email Campaign URLs Created:")
        for url in result["urls"]:
            print(f"- {url['short_url']} -> {url['original_url']}")
        
        # Generate email HTML with tracked links
        email_html = f"""
        <h1>Summer Collection 2024</h1>
        <p>Check out our amazing summer products!</p>
        <ul>
            <li><a href="{result['urls'][0]['short_url']}">Browse Full Collection</a></li>
            <li><a href="{result['urls'][1]['short_url']}">New Swimwear</a></li>
            <li><a href="{result['urls'][2]['short_url']}">Outdoor Gear</a></li>
            <li><a href="{result['urls'][3]['short_url']}">Summer Sale - Up to 50% Off!</a></li>
        </ul>
        """
        
        return email_html

# Example 2: Social Media Integration
def social_media_example():
    """Example: Create tracked URLs for social media posts"""
    
    client = UTMShortenerClient(
        site_url="https://your-site.com",
        api_key="your_api_key",
        api_secret="your_api_secret"
    )
    
    # Different campaigns for different social platforms
    social_platforms = [
        {
            "platform": "facebook",
            "post_url": "https://example.com/new-product-launch",
            "utm_content": "organic-post"
        },
        {
            "platform": "twitter",
            "post_url": "https://example.com/new-product-launch",
            "utm_content": "tweet"
        },
        {
            "platform": "linkedin",
            "post_url": "https://example.com/new-product-launch",
            "utm_content": "article"
        },
        {
            "platform": "instagram",
            "post_url": "https://example.com/new-product-launch",
            "utm_content": "story"
        }
    ]
    
    campaign = client.create_campaign({
        "campaign_name": "Product Launch Social Media",
        "utm_source": "social",
        "utm_medium": "post",
        "utm_campaign": "product-launch-2024",
        "description": "Cross-platform social media campaign"
    })
    
    if campaign["success"]:
        campaign_id = campaign["campaign_id"]
        social_urls = {}
        
        for platform in social_platforms:
            # Create platform-specific URL
            url_result = client.create_short_url({
                "original_url": platform["post_url"],
                "utm_campaign": campaign_id,
                "custom_alias": f"launch-{platform['platform']}",
                "expiry_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            })
            
            if url_result["success"]:
                social_urls[platform["platform"]] = url_result["short_url"]
        
        print("Social Media URLs:")
        for platform, url in social_urls.items():
            print(f"{platform.capitalize()}: {url}")
        
        return social_urls

# Example 3: QR Code Campaign
def qr_code_campaign_example():
    """Example: Create URLs for print materials with QR codes"""
    
    client = UTMShortenerClient(
        site_url="https://your-site.com",
        api_key="your_api_key",
        api_secret="your_api_secret"
    )
    
    # Create campaign for print materials
    campaign = client.create_campaign({
        "campaign_name": "Print Ads Q3 2024",
        "utm_source": "print",
        "utm_medium": "qr-code",
        "utm_campaign": "print-q3-2024",
        "description": "QR codes for magazine and billboard ads"
    })
    
    if campaign["success"]:
        campaign_id = campaign["campaign_id"]
        
        # Create URLs for different print locations
        print_locations = [
            {"name": "Times Magazine", "url": "https://example.com/exclusive-offer", "alias": "times-offer"},
            {"name": "Billboard NYC", "url": "https://example.com/nyc-special", "alias": "nyc-billboard"},
            {"name": "Airport Display", "url": "https://example.com/traveler-deal", "alias": "airport-deal"}
        ]
        
        qr_codes = []
        
        for location in print_locations:
            url_result = client.create_short_url({
                "original_url": location["url"],
                "utm_campaign": campaign_id,
                "custom_alias": location["alias"]
            })
            
            if url_result["success"]:
                # In real implementation, fetch QR code from the system
                qr_codes.append({
                    "location": location["name"],
                    "short_url": url_result["short_url"],
                    "qr_code": f"QR code for {url_result['short_url']}"  # Placeholder
                })
        
        return qr_codes

# Example 4: A/B Testing URLs
def ab_testing_example():
    """Example: Create URLs for A/B testing different landing pages"""
    
    client = UTMShortenerClient(
        site_url="https://your-site.com",
        api_key="your_api_key",
        api_secret="your_api_secret"
    )
    
    # Create campaign for A/B test
    campaign = client.create_campaign({
        "campaign_name": "Landing Page A/B Test",
        "utm_source": "email",
        "utm_medium": "campaign",
        "utm_campaign": "ab-test-landing",
        "description": "Testing two different landing page designs"
    })
    
    if campaign["success"]:
        campaign_id = campaign["campaign_id"]
        
        # Create URLs for variants
        variants = [
            {
                "variant": "A",
                "url": "https://example.com/landing-v1",
                "alias": "test-a",
                "content": "hero-image"
            },
            {
                "variant": "B", 
                "url": "https://example.com/landing-v2",
                "alias": "test-b",
                "content": "video-hero"
            }
        ]
        
        test_urls = []
        
        for variant in variants:
            url_result = client.create_short_url({
                "original_url": variant["url"],
                "utm_campaign": campaign_id,
                "custom_alias": variant["alias"]
            })
            
            if url_result["success"]:
                test_urls.append({
                    "variant": variant["variant"],
                    "short_url": url_result["short_url"],
                    "utm_content": variant["content"]
                })
        
        # After some time, check analytics
        analytics = client.get_analytics(campaign_id)
        
        return {
            "test_urls": test_urls,
            "analytics": analytics
        }

# Example 5: API Webhook Integration
def webhook_integration_example():
    """Example: Automatically create short URLs via webhook"""
    
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    client = UTMShortenerClient(
        site_url="https://your-site.com",
        api_key="your_api_key",
        api_secret="your_api_secret"
    )
    
    @app.route('/webhook/create-short-url', methods=['POST'])
    def create_short_url_webhook():
        """Webhook endpoint to create short URLs automatically"""
        
        data = request.json
        
        # Validate webhook data
        if not data.get('url') or not data.get('campaign_id'):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Create short URL
        result = client.create_short_url({
            "original_url": data['url'],
            "utm_campaign": data['campaign_id'],
            "custom_alias": data.get('alias'),
            "expiry_date": data.get('expiry_date')
        })
        
        if result["success"]:
            # You could also send this to another system
            return jsonify({
                "success": True,
                "short_url": result["short_url"],
                "short_code": result["short_code"]
            })
        else:
            return jsonify({"error": result.get("error", "Unknown error")}), 500
    
    return app

# Example 6: Scheduled Analytics Report
def analytics_report_example():
    """Example: Generate weekly analytics report"""
    
    client = UTMShortenerClient(
        site_url="https://your-site.com",
        api_key="your_api_key",
        api_secret="your_api_secret"
    )
    
    # Get all active campaigns
    # In real implementation, you'd fetch this from the API
    active_campaigns = ["campaign-1", "campaign-2", "campaign-3"]
    
    report_data = []
    
    for campaign_id in active_campaigns:
        analytics = client.get_analytics(campaign_id)
        
        if analytics["success"]:
            report_data.append({
                "campaign": analytics["campaign"]["name"],
                "total_clicks": analytics["analytics"]["total_clicks"],
                "unique_visitors": analytics["analytics"]["unique_visitors"],
                "top_sources": analytics.get("source_breakdown", [])[:5]
            })
    
    # Generate report
    report = "Weekly UTM Campaign Report\n"
    report += "=" * 50 + "\n\n"
    
    for data in report_data:
        report += f"Campaign: {data['campaign']}\n"
        report += f"Total Clicks: {data['total_clicks']}\n"
        report += f"Unique Visitors: {data['unique_visitors']}\n"
        report += "Top Traffic Sources:\n"
        
        for source in data['top_sources']:
            report += f"  - {source.get('source', 'Unknown')}: {source.get('clicks', 0)} clicks\n"
        
        report += "\n"
    
    return report

if __name__ == "__main__":
    # Run examples
    print("UTM Shortener Integration Examples\n")
    
    print("1. Email Marketing Example")
    print("-" * 30)
    # email_html = email_marketing_example()
    
    print("\n2. Social Media Example")
    print("-" * 30)
    # social_urls = social_media_example()
    
    print("\n3. QR Code Campaign Example")
    print("-" * 30)
    # qr_codes = qr_code_campaign_example()
    
    print("\nNote: Update the API credentials before running these examples!")
