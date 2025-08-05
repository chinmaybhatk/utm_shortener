import frappe
from frappe import _

def execute():
    """
    Migration script to update existing Short URLs with proper domain configuration
    """
    # Check if UTM Shortener Settings exists
    if not frappe.db.exists("UTM Shortener Settings", "UTM Shortener Settings"):
        # Create default settings
        settings = frappe.get_doc({
            "doctype": "UTM Shortener Settings",
            "short_domain": frappe.utils.get_url().replace("https://", "").replace("http://", ""),
            "use_https": 1,
            "custom_domain_enabled": 0,
            "fallback_to_site_url": 1,
            "rate_limit_per_hour": 100,
            "bulk_create_limit": 50,
            "analytics_retention_days": 365,
            "enable_geo_tracking": 1
        })
        settings.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Created UTM Shortener Settings with default values")
    
    # Update all existing Short URLs with proper domain
    short_urls = frappe.get_all("Short URL", fields=["name", "short_code"])
    
    for url in short_urls:
        try:
            doc = frappe.get_doc("Short URL", url.name)
            # Regenerate the short URL with current domain settings
            old_url = doc.short_url
            doc.short_url = doc.get_short_url()
            doc.save(ignore_permissions=True)
            print(f"Updated {url.name}: {old_url} -> {doc.short_url}")
        except Exception as e:
            print(f"Error updating {url.name}: {str(e)}")
    
    frappe.db.commit()
    print(f"Migration completed. Updated {len(short_urls)} short URLs.")
