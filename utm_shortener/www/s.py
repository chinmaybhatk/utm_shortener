import frappe
from frappe import _

def redirect_short_url(short_code):
    """Handle short URL redirects via website route"""
    try:
        # Clean the short code
        short_code = short_code.strip()
        
        # Find the short URL document by short_code
        short_url_name = frappe.db.get_value("Short URL", {"short_code": short_code}, "name")
        
        if not short_url_name:
            frappe.throw(_("Short URL not found"), frappe.DoesNotExistError)
        
        # Get the document
        short_url_doc = frappe.get_doc("Short URL", short_url_name)
        
        # Check if URL is active and not expired
        if short_url_doc.status != "Active":
            frappe.throw(_("This short URL is not active"))
        
        if short_url_doc.is_expired():
            frappe.throw(_("This short URL has expired"))
        
        # Prepare request data for tracking
        request_data = {
            "ip_address": frappe.local.request.remote_addr or "",
            "user_agent": frappe.local.request.headers.get('User-Agent', ''),
            "referrer": frappe.local.request.headers.get('Referer', '')
        }
        
        # Track the click and get redirect URL
        redirect_url = short_url_doc.track_click(request_data)
        
        # Perform the redirect
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = redirect_url
        
    except frappe.DoesNotExistError:
        # Redirect to 404 page
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/404"
        
    except Exception as e:
        frappe.log_error(f"Error in redirect_short_url: {str(e)}", "Short URL Redirect Error")
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/404"
