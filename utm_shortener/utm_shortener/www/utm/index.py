import frappe

def get_context(context):
    """
    Handle UTM link redirection
    """
    short_code = frappe.local.request.path.split('/')[-1]
    
    try:
        # Find the UTM link
        utm_link = frappe.get_doc('UTM Link', {'short_code': short_code})
        
        # Check expiration
        if utm_link.is_expired():
            frappe.throw("Link has expired")
        
        # Check click limit
        if utm_link.max_clicks_allowed and utm_link.total_clicks >= utm_link.max_clicks_allowed:
            frappe.throw("Maximum click limit reached")
        
        # Track and redirect
        redirect_url = utm_link.track_click(frappe.local.request)
        frappe.local.flags.redirect_location = redirect_url
        raise frappe.Redirect
    
    except Exception as e:
        frappe.log_error(f"UTM Redirect Error: {e}")
        frappe.throw("Invalid or expired link")