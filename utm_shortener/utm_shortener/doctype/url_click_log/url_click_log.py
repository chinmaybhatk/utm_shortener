# Copyright (c) 2025, Chinmay Bhat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class URLClickLog(Document):
    def after_insert(self):
        """Process analytics data after insert"""
        # Update unique visitor count if needed
        self.update_unique_visitors()
        
    def update_unique_visitors(self):
        """Update unique visitor count based on IP"""
        # Check if this IP has visited this URL before
        existing = frappe.db.exists("URL Click Log", {
            "short_url": self.short_url,
            "ip_address": self.ip_address,
            "name": ["!=", self.name]
        })
        
        if not existing:
            # This is a unique visitor
            short_url_doc = frappe.get_doc("Short URL", self.short_url)
            short_url_doc.unique_visitors = (short_url_doc.unique_visitors or 0) + 1
            short_url_doc.save(ignore_permissions=True)
