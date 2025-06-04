import frappe
from frappe.model.document import Document
import string
import random
import re
from datetime import datetime
from urllib.parse import urlparse

class ShortURL(Document):
    def before_save(self):
        """Generate short code and URL before saving"""
        if not self.short_code:
            self.short_code = self.custom_alias or self.generate_short_code()
        
        self.short_url = self.generate_short_url()
        self.validate_url()
        
        if self.utm_campaign:
            self.generate_utm_url()
    
    def generate_short_code(self):
        """Generate unique short code (6-8 characters)"""
        characters = string.ascii_letters + string.digits
        
        for length in [6, 7, 8]:  # Try different lengths if needed
            for _ in range(100):  # Max 100 attempts per length
                code = ''.join(random.choices(characters, k=length))
                
                # Check if code already exists
                if not frappe.db.exists("Short URL", {"short_code": code}):
                    return code
        
        # Fallback: use timestamp-based code
        timestamp = str(int(datetime.now().timestamp()))[-8:]
        return f"url{timestamp}"
    
    def generate_short_url(self):
        """Generate complete short URL with /s/ prefix"""
        # Get base domain from system settings or default
        try:
            base_domain = frappe.db.get_single_value("UTM Shortener Settings", "base_domain") or frappe.utils.get_site_name()
            use_https = frappe.db.get_single_value("UTM Shortener Settings", "use_https")
        except:
            base_domain = frappe.utils.get_site_name()
            use_https = True
            
        protocol = "https" if use_https else "http"
        return f"{protocol}://{base_domain}/s/{self.short_code}"
    
    def generate_utm_url(self):
        """Generate UTM-enabled original URL"""
        if not self.utm_campaign:
            return
            
        campaign_doc = frappe.get_doc("UTM Campaign", self.utm_campaign)
        self.generated_utm_url = campaign_doc.generate_utm_url(self.original_url)
    
    def validate_url(self):
        """Validate original URL format"""
        if not self.original_url:
            frappe.throw("Original URL is required")
        
        # Basic URL validation
        try:
            result = urlparse(self.original_url)
            if not all([result.scheme, result.netloc]):
                frappe.throw("Invalid URL format. Please include http:// or https://")
        except Exception:
            frappe.throw("Invalid URL format")
        
        # Check for blocked domains
        try:
            blocked_domains = frappe.db.get_single_value("UTM Shortener Settings", "blocked_domains")
            if blocked_domains:
                blocked_list = [domain.strip() for domain in blocked_domains.split(',')]
                domain = urlparse(self.original_url).netloc.lower()
                if any(blocked in domain for blocked in blocked_list):
                    frappe.throw("This domain is blocked from shortening")
        except:
            pass
    
    def track_click(self, request_data):
        """Record click and update analytics"""
        if self.is_expired():
            frappe.throw("This short URL has expired")
        
        if self.status != "Active":
            frappe.throw("This short URL is not active")
        
        # Create click log entry
        click_log = frappe.get_doc({
            "doctype": "URL Click Log",
            "short_url": self.name,
            "ip_address": request_data.get("ip_address", "")[:15],  # Limit IP length
            "user_agent": request_data.get("user_agent", "")[:500],  # Limit UA length
            "referrer_url": request_data.get("referrer", "")[:500],  # Limit referrer length
            "country": self.get_country_from_ip(request_data.get("ip_address")),
            "device_type": self.detect_device_type(request_data.get("user_agent")),
            "browser": self.detect_browser(request_data.get("user_agent")),
            "operating_system": self.detect_os(request_data.get("user_agent"))
        })
        click_log.insert(ignore_permissions=True)
        
        # Update click count and last accessed
        self.clicks = (self.clicks or 0) + 1
        self.last_accessed = datetime.now()
        self.save(ignore_permissions=True)
        
        return self.generated_utm_url or self.original_url
    
    def is_expired(self):
        """Check if URL has expired"""
        if not self.expiry_date:
            return False
        return datetime.now().date() > self.expiry_date
    
    def get_country_from_ip(self, ip_address):
        """Get country from IP address"""
        if not ip_address:
            return "Unknown"
        
        try:
            # Check if geolocation is enabled
            settings = frappe.get_single("UTM Shortener Settings")
            if not settings.enable_geolocation:
                return "Unknown"
            
            # Placeholder for IP geolocation service integration
            # You can integrate with services like MaxMind, IPStack, etc.
            return "Unknown"
        except:
            return "Unknown"
    
    def detect_device_type(self, user_agent):
        """Detect device type from user agent"""
        if not user_agent:
            return "Unknown"
        
        ua_lower = user_agent.lower()
        if any(mobile in ua_lower for mobile in ['mobile', 'android', 'iphone']):
            return "Mobile"
        elif 'tablet' in ua_lower or 'ipad' in ua_lower:
            return "Tablet"
        else:
            return "Desktop"
    
    def detect_browser(self, user_agent):
        """Detect browser from user agent"""
        if not user_agent:
            return "Unknown"
        
        ua_lower = user_agent.lower()
        if 'chrome' in ua_lower and 'edg' not in ua_lower:
            return "Chrome"
        elif 'firefox' in ua_lower:
            return "Firefox"
        elif 'safari' in ua_lower and 'chrome' not in ua_lower:
            return "Safari"
        elif 'edg' in ua_lower:
            return "Edge"
        elif 'opera' in ua_lower:
            return "Opera"
        else:
            return "Other"
    
    def detect_os(self, user_agent):
        """Detect operating system from user agent"""
        if not user_agent:
            return "Unknown"
        
        ua_lower = user_agent.lower()
        if 'windows nt' in ua_lower:
            return "Windows"
        elif 'mac os x' in ua_lower or 'macos' in ua_lower:
            return "macOS"
        elif 'linux' in ua_lower and 'android' not in ua_lower:
            return "Linux"
        elif 'android' in ua_lower:
            return "Android"
        elif 'iphone os' in ua_lower or 'ios' in ua_lower:
            return "iOS"
        else:
            return "Other"

# Hook functions
def generate_short_code(doc, method):
    """Hook for generating short code"""
    if not doc.short_code:
        doc.short_code = doc.custom_alias or doc.generate_short_code()