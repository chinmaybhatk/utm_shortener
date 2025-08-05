# Copyright (c) 2025, Chinmay Bhat and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def get_context(context):
    """Context for the URL shortener landing page"""
    context.no_cache = 1
    context.title = _("URL Shortener")
    
    # Get settings
    try:
        settings = frappe.get_single("UTM Shortener Settings")
        context.base_domain = settings.base_domain
        context.rate_limit = settings.rate_limit_per_hour
    except:
        context.base_domain = frappe.utils.get_site_name()
        context.rate_limit = 100
    
    # Get user's recent URLs if logged in
    if frappe.session.user != "Guest":
        context.recent_urls = frappe.get_all("Short URL",
            filters={"owner": frappe.session.user},
            fields=["name", "short_code", "short_url", "original_url", "clicks", "creation"],
            order_by="creation desc",
            limit=10
        )
    else:
        context.recent_urls = []
    
    return context
