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
    """Create sample