# Copyright (c) 2025, Chinmay Bhat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import string
import random

class UTMTemplate(Document):
    def before_insert(self):
        """Generate template code before insert"""
        if not self.template_code:
            self.template_code = self.generate_template_code()
    
    def generate_template_code(self):
        """Generate unique template code"""
        prefix = "TMPL-"
        for _ in range(100):
            code = prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not frappe.db.exists("UTM Template", {"template_code": code}):
                return code
        
        # Fallback
        return prefix + frappe.utils.now_datetime().strftime("%Y%m%d%H%M%S")
    
    def create_campaign_from_template(self, campaign_name, base_url=None):
        """Create a new UTM Campaign from this template"""
        campaign = frappe.new_doc("UTM Campaign")
        campaign.campaign_name = campaign_name
        campaign.utm_source = self.utm_source
        campaign.utm_medium = self.utm_medium
        campaign.utm_campaign = self.utm_campaign_template.format(
            template_name=self.template_name,
            date=frappe.utils.today(),
            timestamp=frappe.utils.now_datetime().strftime("%Y%m%d")
        )
        
        if self.utm_term_template:
            campaign.utm_term = self.utm_term_template
        
        if self.utm_content_template:
            campaign.utm_content = self.utm_content_template
        
        if base_url:
            campaign.base_url = base_url
        
        campaign.description = f"Created from template: {self.template_name}\n{self.description or ''}"
        
        return campaign
