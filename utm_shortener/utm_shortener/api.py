import frappe
from frappe import _
import json
import re
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def redirect_short_url(short_code=None):
    """Handle short URL redirects"""
    try:
        # Get short_code from path if not provided
        if not short_code:
            path = frappe.local.request.path
            if '/s/' in path:
                short_code = path.split('/s/')[-1].strip('/')
        
        if not short_code:
            frappe.throw(_("Short code not provided"))
        
        # Find the short URL document
        short_url_name = frappe.db.get_value("Short URL", {"short_code": short_code}, "name")
        
        if not short_url_name:
            frappe.throw(_("Short URL not found"), frappe.DoesNotExistError)
        
        # Get the document
        short_url_doc = frappe.get_doc("Short URL", short_url_name)
        
        # Prepare request data
        request_data = {
            "ip_address": frappe.local.request.environ.get('REMOTE_ADDR', ''),
            "user_agent": frappe.local.request.environ.get('HTTP_USER_AGENT', ''),
            "referrer": frappe.local.request.environ.get('HTTP_REFERER', '')
        }
        
        # Track the click and get redirect URL
        redirect_url = short_url_doc.track_click(request_data)
        
        # Return redirect response
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = redirect_url
        
    except Exception as e:
        frappe.log_error(f"Error in redirect_short_url: {str(e)}")
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/404"

@frappe.whitelist()
def create_short_url(original_url, utm_campaign=None, custom_alias=None, expiry_date=None):
    """Create new short URL"""
    try:
        # Rate limiting check
        if not check_rate_limit():
            frappe.throw(_("Rate limit exceeded. Please try again later."))
        
        # Validate custom alias if provided
        if custom_alias:
            if frappe.db.exists("Short URL", {"short_code": custom_alias}):
                frappe.throw(_("Custom alias already exists"))
            
            # Validate alias format
            if not re.match(r'^[a-zA-Z0-9_-]+$', custom_alias):
                frappe.throw(_("Custom alias can only contain letters, numbers, hyphens, and underscores"))
            
            if len(custom_alias) < 3 or len(custom_alias) > 20:
                frappe.throw(_("Custom alias must be between 3 and 20 characters"))
        
        # Create short URL document
        short_url_doc = frappe.get_doc({
            "doctype": "Short URL",
            "original_url": original_url,
            "utm_campaign": utm_campaign,
            "custom_alias": custom_alias,
            "expiry_date": expiry_date,
            "status": "Active"
        })
        
        short_url_doc.insert()
        
        return {
            "success": True,
            "short_code": short_url_doc.short_code,
            "short_url": short_url_doc.short_url,
            "original_url": short_url_doc.original_url,
            "utm_url": short_url_doc.generated_utm_url,
            "expires": short_url_doc.expiry_date
        }
        
    except Exception as e:
        frappe.log_error(f"Error creating short URL: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@frappe.whitelist()
def get_url_analytics(short_code):
    """Get analytics for specific short URL"""
    try:
        short_url = frappe.get_doc("Short URL", {"short_code": short_code})
        
        if not short_url:
            frappe.throw(_("Short URL not found"))
        
        # Check permissions
        if not frappe.has_permission("Short URL", "read", short_url.name):
            frappe.throw(_("Insufficient permissions"))
        
        # Get click logs
        click_logs = frappe.get_all("URL Click Log",
            filters={"short_url": short_url.name},
            fields=["timestamp", "country", "device_type", "browser", "ip_address"],
            order_by="timestamp desc",
            limit=100
        )
        
        # Get analytics summary
        analytics = frappe.db.sql("""
            SELECT 
                COUNT(*) as total_clicks,
                COUNT(DISTINCT ip_address) as unique_visitors,
                DATE(timestamp) as date,
                device_type,
                country,
                browser
            FROM `tabURL Click Log`
            WHERE short_url = %s
            GROUP BY DATE(timestamp), device_type, country, browser
            ORDER BY date DESC
            LIMIT 30
        """, (short_url.name,), as_dict=True)
        
        return {
            "success": True,
            "short_url": {
                "code": short_url.short_code,
                "original_url": short_url.original_url,
                "created": short_url.creation,
                "total_clicks": short_url.clicks,
                "status": short_url.status,
                "expires": short_url.expiry_date
            },
            "recent_clicks": click_logs,
            "analytics": analytics
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting URL analytics: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@frappe.whitelist()
def bulk_create_utm_urls(campaign, url_list):
    """Create multiple short URLs for a campaign"""
    try:
        if isinstance(url_list, str):
            url_list = json.loads(url_list)
        
        if not check_rate_limit(len(url_list)):
            frappe.throw(_("Rate limit exceeded for bulk creation"))
        
        results = []
        errors = []
        
        for i, url_data in enumerate(url_list):
            try:
                if isinstance(url_data, str):
                    url_data = {"url": url_data}
                
                short_url_doc = frappe.get_doc({
                    "doctype": "Short URL",
                    "original_url": url_data.get("url"),
                    "utm_campaign": campaign,
                    "custom_alias": url_data.get("alias"),
                    "status": "Active"
                })
                
                short_url_doc.insert()
                
                results.append({
                    "index": i,
                    "original_url": short_url_doc.original_url,
                    "short_code": short_url_doc.short_code,
                    "short_url": short_url_doc.short_url,
                    "utm_url": short_url_doc.generated_utm_url
                })
                
            except Exception as e:
                errors.append({
                    "index": i,
                    "url": url_data.get("url", ""),
                    "error": str(e)
                })
        
        return {
            "success": True,
            "created_count": len(results),
            "error_count": len(errors),
            "urls": results,
            "errors": errors
        }
        
    except Exception as e:
        frappe.log_error(f"Error in bulk URL creation: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@frappe.whitelist()
def create_utm_campaign(campaign_name, utm_source, utm_medium, utm_campaign, utm_term=None, utm_content=None, description=None):
    """Create a new UTM campaign"""
    try:
        # Check if campaign already exists
        if frappe.db.exists("UTM Campaign", {"utm_campaign": utm_campaign}):
            frappe.throw(_("Campaign with this UTM campaign code already exists"))
        
        # Create UTM Campaign document
        campaign_doc = frappe.get_doc({
            "doctype": "UTM Campaign",
            "campaign_name": campaign_name,
            "utm_source": utm_source,
            "utm_medium": utm_medium,
            "utm_campaign": utm_campaign,
            "utm_term": utm_term,
            "utm_content": utm_content,
            "description": description,
            "status": "Active"
        })
        
        campaign_doc.insert()
        
        return {
            "success": True,
            "campaign_id": campaign_doc.name,
            "campaign_name": campaign_doc.campaign_name,
            "utm_campaign": campaign_doc.utm_campaign,
            "message": _("UTM Campaign created successfully")
        }
        
    except Exception as e:
        frappe.log_error(f"Error creating UTM campaign: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@frappe.whitelist()
def get_campaign_analytics(campaign_id):
    """Get analytics data for a specific UTM campaign"""
    try:
        # Get the campaign
        campaign = frappe.get_doc("UTM Campaign", campaign_id)
        
        if not campaign:
            frappe.throw(_("Campaign not found"))
        
        # Check permissions
        if not frappe.has_permission("UTM Campaign", "read", campaign.name):
            frappe.throw(_("Insufficient permissions"))
        
        # Get all short URLs for this campaign
        short_urls = frappe.get_all("Short URL",
            filters={"utm_campaign": campaign.name},
            fields=["name", "short_code", "original_url", "clicks", "status", "creation"]
        )
        
        # Get aggregated analytics
        total_clicks = 0
        total_unique_visitors = 0
        
        for url in short_urls:
            # Get analytics for each short URL
            click_data = frappe.db.sql("""
                SELECT 
                    COUNT(*) as clicks,
                    COUNT(DISTINCT ip_address) as unique_visitors
                FROM `tabURL Click Log`
                WHERE short_url = %s
            """, (url.name,), as_dict=True)[0]
            
            total_clicks += click_data.clicks
            total_unique_visitors += click_data.unique_visitors
        
        # Get conversion source breakdown
        source_analytics = frappe.db.sql("""
            SELECT 
                ucl.referrer_source as source,
                COUNT(*) as clicks,
                COUNT(DISTINCT ucl.ip_address) as unique_visitors
            FROM `tabURL Click Log` ucl
            INNER JOIN `tabShort URL` su ON ucl.short_url = su.name
            WHERE su.utm_campaign = %s
            GROUP BY ucl.referrer_source
            ORDER BY clicks DESC
        """, (campaign.name,), as_dict=True)
        
        return {
            "success": True,
            "campaign": {
                "id": campaign.name,
                "name": campaign.campaign_name,
                "utm_campaign": campaign.utm_campaign,
                "status": campaign.status,
                "created": campaign.creation
            },
            "analytics": {
                "total_clicks": total_clicks,
                "unique_visitors": total_unique_visitors,
                "total_urls": len(short_urls),
                "active_urls": len([u for u in short_urls if u.status == "Active"])
            },
            "urls": short_urls,
            "source_breakdown": source_analytics
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting campaign analytics: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def check_rate_limit(count=1):
    """Check if user is within rate limits"""
    try:
        settings = frappe.get_single("UTM Shortener Settings")
        rate_limit = settings.rate_limit_per_hour or 100
        
        # Count URLs created by user in last hour
        one_hour_ago = datetime.now() - frappe.utils.datetime.timedelta(hours=1)
        
        existing_count = frappe.db.count("Short URL", {
            "owner": frappe.session.user,
            "creation": [">", one_hour_ago]
        })
        
        return (existing_count + count) <= rate_limit
        
    except:
        return True  # Allow if settings not configured
