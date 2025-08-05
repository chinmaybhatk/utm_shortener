# Copyright (c) 2025, Chinmay Bhat and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import now_datetime, add_days

def cleanup_expired_urls():
    """Mark expired URLs as inactive"""
    expired_urls = frappe.db.sql("""
        SELECT name 
        FROM `tabShort URL`
        WHERE status = 'Active'
        AND expiry_date IS NOT NULL
        AND expiry_date < CURDATE()
    """, as_dict=True)
    
    for url in expired_urls:
        doc = frappe.get_doc("Short URL", url.name)
        doc.status = "Expired"
        doc.save(ignore_permissions=True)
    
    if expired_urls:
        frappe.db.commit()
        return f"Marked {len(expired_urls)} URLs as expired"
    
    return "No expired URLs found"

def reset_rate_limits():
    """Reset hourly rate limits (if implemented)"""
    # This is a placeholder for rate limit reset logic
    # You can implement rate limiting using frappe.cache()
    # or a custom DocType to track usage
    pass

def update_geolocation_data():
    """Update missing geolocation data for recent clicks"""
    try:
        settings = frappe.get_single("UTM Shortener Settings")
        if not settings.enable_geolocation or not settings.geolocation_api_key:
            return "Geolocation is not enabled"
        
        # Get clicks without geolocation data from the last 24 hours
        clicks = frappe.db.sql("""
            SELECT name, ip_address
            FROM `tabURL Click Log`
            WHERE country = 'Unknown'
            AND ip_address IS NOT NULL
            AND ip_address != ''
            AND timestamp > DATE_SUB(NOW(), INTERVAL 24 HOUR)
            LIMIT 100
        """, as_dict=True)
        
        # Implement geolocation API call here
        # This is a placeholder - you would integrate with a service like:
        # - MaxMind GeoIP2
        # - IPStack
        # - IP-API
        
        return f"Processed {len(clicks)} clicks for geolocation"
        
    except Exception as e:
        frappe.log_error(f"Error updating geolocation: {str(e)}", "Geolocation Update Error")
        return f"Error: {str(e)}"
