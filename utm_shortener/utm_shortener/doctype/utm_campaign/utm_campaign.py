import frappe
from frappe.model.document import Document
from urllib.parse import urlencode
import re
import string
import random

class UTMCampaign(Document):
    def before_save(self):
        """Generate campaign code before saving"""
        if not self.campaign_code:
            self.campaign_code = self.generate_campaign_code()
        self.validate_utm_parameters()
    
    def generate_campaign_code(self):
        """Generate unique campaign code"""
        # Create code from campaign name + random string
        base = re.sub(r'[^a-zA-Z0-9]', '', self.campaign_name[:10]).upper()
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        
        code = f"{base}-{random_part}"
        
        # Ensure uniqueness
        counter = 1
        original_code = code
        while frappe.db.exists("UTM Campaign", {"campaign_code": code}):
            code = f"{original_code}-{counter:02d}"
            counter += 1
            
        return code
    
    def generate_utm_url(self, base_url):
        """Generate complete URL with UTM parameters"""
        if not base_url:
            return ""
            
        params = {}
        if self.utm_source:
            params['utm_source'] = self.utm_source
        if self.utm_medium:
            params['utm_medium'] = self.utm_medium
        if self.utm_campaign:
            params['utm_campaign'] = self.utm_campaign
        if self.utm_term:
            params['utm_term'] = self.utm_term
        if self.utm_content:
            params['utm_content'] = self.utm_content
        
        if params:
            separator = '&' if '?' in base_url else '?'
            return f"{base_url}{separator}{urlencode(params)}"
        
        return base_url
    
    def validate_utm_parameters(self):
        """Validate UTM parameter format and values"""
        # Validate required fields
        if not self.utm_source:
            frappe.throw("UTM Source is required")
        if not self.utm_medium:
            frappe.throw("UTM Medium is required")
        if not self.utm_campaign:
            frappe.throw("UTM Campaign is required")
        
        # Validate format (alphanumeric, hyphens, underscores only)
        utm_pattern = r'^[a-zA-Z0-9_-]+$'
        
        for field, value in [
            ('utm_source', self.utm_source),
            ('utm_campaign', self.utm_campaign),
            ('utm_term', self.utm_term),
            ('utm_content', self.utm_content)
        ]:
            if value and not re.match(utm_pattern, value):
                frappe.throw(f"{field} can only contain letters, numbers, hyphens, and underscores")
    
    def get_campaign_analytics(self):
        """Get click analytics for this campaign"""
        # Get all short URLs for this campaign
        short_urls = frappe.get_all("Short URL", 
            filters={"utm_campaign": self.name},
            fields=["name", "short_code", "clicks", "original_url", "status"]
        )
        
        total_clicks = sum([url.get('clicks', 0) for url in short_urls])
        
        # Get click details from logs
        click_logs = frappe.db.sql("""
            SELECT 
                COUNT(*) as total_clicks,
                COUNT(DISTINCT ip_address) as unique_visitors,
                device_type,
                country,
                DATE(timestamp) as click_date
            FROM `tabURL Click Log` ucl
            INNER JOIN `tabShort URL` su ON ucl.short_url = su.name
            WHERE su.utm_campaign = %s
            GROUP BY device_type, country, DATE(timestamp)
            ORDER BY click_date DESC
        """, (self.name,), as_dict=True)
        
        return {
            "total_urls": len(short_urls),
            "total_clicks": total_clicks,
            "urls": short_urls,
            "click_details": click_logs
        }

# Whitelisted API methods
@frappe.whitelist()
def get_campaign_analytics(campaign_name):
    """API method to get campaign analytics"""
    campaign = frappe.get_doc("UTM Campaign", campaign_name)
    return campaign.get_campaign_analytics()

@frappe.whitelist()
def generate_utm_url(campaign_name, base_url):
    """API method to generate UTM URL"""
    campaign = frappe.get_doc("UTM Campaign", campaign_name)
    return campaign.generate_utm_url(base_url)

def validate_utm_parameters(doc, method):
    """Hook for validating UTM parameters"""
    doc.validate_utm_parameters()

def get_permission_query_conditions(user):
    """Permission query conditions for UTM Campaign"""
    if not user:
        user = frappe.session.user
    
    if "System Manager" in frappe.get_roles(user):
        return ""
    
    return """(`tabUTM Campaign`.owner = '{user}' or `tabUTM Campaign`.owner in (
        select parent from `tabHas Role` where role in (
            select parent from `tabHas Role` where parenttype = 'User' and parent = '{user}'
        ) and parenttype = 'User'
    ))""".format(user=frappe.db.escape(user))