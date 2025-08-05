# Copyright (c) 2025, Chinmay Bhat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class UTMShortenerSettings(Document):
    def validate(self):
        """Validate settings"""
        # Ensure base domain is set
        if not self.base_domain:
            self.base_domain = frappe.utils.get_site_name()
        
        # Validate rate limit
        if self.rate_limit_per_hour and self.rate_limit_per_hour < 1:
            frappe.throw("Rate limit must be at least 1 per hour")
        
        # Clean blocked domains
        if self.blocked_domains:
            # Remove duplicates and clean up
            domains = set([d.strip().lower() for d in self.blocked_domains.split(',') if d.strip()])
            self.blocked_domains = ','.join(sorted(domains))
