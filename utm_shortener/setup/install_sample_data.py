import frappe
from frappe.utils import now_datetime, add_days, get_datetime
import random
import string

def install_sample_data():
    """Install sample data for UTM Shortener app"""
    print("Installing UTM Shortener sample data...")
    
    # Create sample UTM Campaigns
    campaigns = create_sample_campaigns()
    
    # Create sample UTM Templates
    templates = create_sample_templates()
    
    # Create sample Short URLs
    short_urls = create_sample_short_urls(campaigns)
    
    # Create sample click logs
    create_sample_click_logs(short_urls)
    
    # Create UTM Shortener Settings
    create_sample_settings()
    
    frappe.db.commit()
    print("Sample data installation completed!")
    
    return {
        "campaigns": len(campaigns),
        "templates": len(templates),
        "short_urls": len(short_urls),
        "message": "Sample data installed successfully!"
    }

def create_sample_campaigns():
    """Create sample UTM campaigns"""
    campaigns = []
    
    sample_campaigns = [
        {
            "campaign_name": "Summer Sale 2025",
            "utm_source": "email",
            "utm_medium": "newsletter",
            "utm_campaign": "summer_sale_2025",
            "utm_content": "header_cta",
            "description": "Summer collection promotional campaign",
            "status": "Active",
            "start_date": get_datetime().date(),
            "end_date": add_days(get_datetime().date(), 30)
        },
        {
            "campaign_name": "Product Launch - Social",
            "utm_source": "facebook",
            "utm_medium": "social",
            "utm_campaign": "product_launch_q2",
            "utm_content": "video_ad",
            "description": "New product launch campaign on social media",
            "status": "Active",
            "start_date": get_datetime().date(),
            "end_date": add_days(get_datetime().date(), 14)
        },
        {
            "campaign_name": "Google Ads - Electronics",
            "utm_source": "google",
            "utm_medium": "cpc",
            "utm_campaign": "electronics_sale",
            "utm_term": "laptop_deals",
            "utm_content": "text_ad",
            "description": "Paid search campaign for electronics",
            "status": "Active",
            "start_date": get_datetime().date(),
            "end_date": add_days(get_datetime().date(), 7)
        }
    ]
    
    for campaign_data in sample_campaigns:
        try:
            if not frappe.db.exists("UTM Campaign", {"utm_campaign": campaign_data["utm_campaign"]}):
                campaign = frappe.get_doc({
                    "doctype": "UTM Campaign",
                    **campaign_data
                })
                campaign.insert()
                campaigns.append(campaign)
        except Exception as e:
            print(f"Error creating campaign: {str(e)}")
    
    return campaigns

def create_sample_templates():
    """Create sample UTM templates"""
    templates = []
    
    sample_templates = [
        {
            "template_name": "Email Newsletter Template",
            "utm_source": "mailchimp",
            "utm_medium": "email",
            "utm_campaign_template": "{campaign_name}_{date}",
            "description": "Standard template for email newsletters",
            "is_active": True
        },
        {
            "template_name": "Social Media Template",
            "utm_source": "{platform}",
            "utm_medium": "social",
            "utm_campaign_template": "{campaign_name}_social",
            "utm_content_template": "{post_type}",
            "description": "Template for social media campaigns",
            "is_active": True
        }
    ]
    
    for template_data in sample_templates:
        try:
            if not frappe.db.exists("UTM Template", {"template_name": template_data["template_name"]}):
                template = frappe.get_doc({
                    "doctype": "UTM Template",
                    **template_data
                })
                template.insert()
                templates.append(template)
        except Exception as e:
            print(f"Error creating template: {str(e)}")
    
    return templates

def create_sample_short_urls(campaigns):
    """Create sample short URLs"""
    short_urls = []
    
    sample_urls = [
        {
            "original_url": "https://example.com/products/summer-collection",
            "custom_alias": "summer25",
            "status": "Active",
            "expiry_date": add_days(get_datetime().date(), 90)
        },
        {
            "original_url": "https://example.com/blog/latest-tech-trends",
            "status": "Active",
            "expiry_date": add_days(get_datetime().date(), 365)
        }
    ]
    
    # Add URLs with campaigns
    if campaigns:
        for campaign in campaigns[:2]:  # Link first 2 campaigns
            sample_urls.append({
                "original_url": f"https://example.com/landing/{campaign.utm_campaign}",
                "utm_campaign": campaign.name,
                "status": "Active",
                "expiry_date": campaign.end_date
            })
    
    for url_data in sample_urls:
        try:
            short_url = frappe.get_doc({
                "doctype": "Short URL",
                **url_data
            })
            short_url.insert()
            short_urls.append(short_url)
        except Exception as e:
            print(f"Error creating short URL: {str(e)}")
    
    return short_urls

def create_sample_click_logs(short_urls):
    """Create sample click logs for analytics"""
    if not short_urls:
        return
    
    devices = ["Desktop", "Mobile", "Tablet"]
    browsers = ["Chrome", "Firefox", "Safari", "Edge"]
    countries = ["United States", "United Kingdom", "Canada", "India", "Germany"]
    
    for short_url in short_urls[:3]:  # Create logs for first 3 URLs
        # Create 5-15 random clicks
        num_clicks = random.randint(5, 15)
        
        for i in range(num_clicks):
            try:
                click_log = frappe.get_doc({
                    "doctype": "URL Click Log",
                    "short_url": short_url.name,
                    "timestamp": add_days(now_datetime(), -random.randint(0, 7)),
                    "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                    "device_type": random.choice(devices),
                    "browser": random.choice(browsers),
                    "country": random.choice(countries),
                    "user_agent": f"Mozilla/5.0 ({random.choice(devices)})"
                })
                click_log.insert()
            except Exception as e:
                print(f"Error creating click log: {str(e)}")

def create_sample_settings():
    """Create UTM Shortener Settings"""
    try:
        if not frappe.db.exists("UTM Shortener Settings", "UTM Shortener Settings"):
            settings = frappe.get_doc({
                "doctype": "UTM Shortener Settings",
                "base_domain": frappe.utils.get_site_name(),
                "use_https": 1,
                "default_expiry_days": 365,
                "rate_limit_per_hour": 100,
                "enable_geolocation": 0
            })
            settings.insert()
    except Exception as e:
        print(f"Error creating settings: {str(e)}")

@frappe.whitelist()
def install():
    """Wrapper function for installing sample data"""
    return install_sample_data()
