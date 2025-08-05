import frappe
from frappe.model.document import Document
from frappe.utils import cstr, now_datetime, get_datetime
import string
import random
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import qrcode
import io
import base64

class ShortURL(Document):
    def before_insert(self):
        """Generate short code and URL before insert"""
        # Generate short code if not provided
        if not self.short_code:
            if self.custom_alias:
                self.short_code = self.custom_alias
            else:
                self.short_code = self.generate_short_code()
        
        # Generate the short URL using configured domain
        self.short_url = self.get_short_url()
        
        # Generate UTM URL if campaign is selected
        if self.utm_campaign:
            self.generated_utm_url = self.generate_utm_url()
    
    def get_short_url(self):
        """Generate the complete short URL using configured domain"""
        settings = frappe.get_single("UTM Shortener Settings")
        
        # Get domain configuration
        if settings.custom_domain_enabled and settings.short_domain:
            domain = settings.short_domain
        else:
            # Fallback to site URL
            domain = frappe.utils.get_url()
            # Remove protocol from domain
            domain = domain.replace("https://", "").replace("http://", "")
        
        # Determine protocol
        protocol = "https" if settings.use_https else "http"
        
        # Generate the short URL
        return f"{protocol}://{domain}/s/{self.short_code}"
    
    def generate_short_code(self):
        """Generate unique short code"""
        length = 6
        characters = string.ascii_lowercase + string.digits
        
        while True:
            code = ''.join(random.choice(characters) for _ in range(length))
            if not frappe.db.exists("Short URL", {"short_code": code}):
                return code
    
    def generate_utm_url(self):
        """Generate URL with UTM parameters"""
        if not self.utm_campaign:
            return self.original_url
        
        # Get UTM campaign details
        campaign = frappe.get_doc("UTM Campaign", self.utm_campaign)
        
        # Parse the original URL
        parsed = urlparse(self.original_url)
        params = parse_qs(parsed.query)
        
        # Add UTM parameters
        utm_params = {
            'utm_source': campaign.utm_source,
            'utm_medium': campaign.utm_medium,
            'utm_campaign': campaign.utm_campaign
        }
        
        if campaign.utm_term:
            utm_params['utm_term'] = campaign.utm_term
        
        if campaign.utm_content:
            utm_params['utm_content'] = campaign.utm_content
        
        # Merge with existing parameters
        params.update(utm_params)
        
        # Rebuild the URL
        new_query = urlencode(params, doseq=True)
        new_parsed = parsed._replace(query=new_query)
        
        return urlunparse(new_parsed)
    
    def generate_qr_code(self):
        """Generate QR code for the short URL"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        qr.add_data(self.short_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        self.qr_code = f"data:image/png;base64,{img_str}"
    
    def track_click(self, request_data=None):
        """Track click and return redirect URL"""
        # Increment click counter
        self.clicks = (self.clicks or 0) + 1
        self.last_clicked = now_datetime()
        self.save(ignore_permissions=True)
        
        # Create click log entry
        if request_data:
            self.create_click_log(request_data)
        
        # Return the appropriate URL
        if self.generated_utm_url:
            return self.generated_utm_url
        return self.original_url
    
    def create_click_log(self, request_data):
        """Create a click log entry"""
        try:
            # Parse user agent for device and browser info
            user_agent = request_data.get('user_agent', '')
            device_info = self.parse_user_agent(user_agent)
            
            # Parse referrer for source tracking
            referrer = request_data.get('referrer', '')
            referrer_source = self.get_referrer_source(referrer)
            
            # Create log entry
            click_log = frappe.get_doc({
                'doctype': 'URL Click Log',
                'short_url': self.name,
                'timestamp': now_datetime(),
                'ip_address': request_data.get('ip_address', ''),
                'user_agent': user_agent,
                'referrer': referrer,
                'referrer_source': referrer_source,
                'device_type': device_info.get('device_type', 'Unknown'),
                'browser': device_info.get('browser', 'Unknown'),
                'operating_system': device_info.get('os', 'Unknown'),
                'country': self.get_country_from_ip(request_data.get('ip_address'))
            })
            
            click_log.insert(ignore_permissions=True)
            
        except Exception as e:
            frappe.log_error(f"Error creating click log: {str(e)}")
    
    def parse_user_agent(self, user_agent):
        """Parse user agent string to extract device and browser info"""
        # Simple parsing - in production, use a proper user agent parser
        device_type = 'Desktop'
        browser = 'Unknown'
        os = 'Unknown'
        
        ua_lower = user_agent.lower()
        
        # Detect device type
        if 'mobile' in ua_lower or 'android' in ua_lower:
            device_type = 'Mobile'
        elif 'tablet' in ua_lower or 'ipad' in ua_lower:
            device_type = 'Tablet'
        
        # Detect browser
        if 'chrome' in ua_lower:
            browser = 'Chrome'
        elif 'firefox' in ua_lower:
            browser = 'Firefox'
        elif 'safari' in ua_lower:
            browser = 'Safari'
        elif 'edge' in ua_lower:
            browser = 'Edge'
        
        # Detect OS
        if 'windows' in ua_lower:
            os = 'Windows'
        elif 'mac' in ua_lower:
            os = 'macOS'
        elif 'linux' in ua_lower:
            os = 'Linux'
        elif 'android' in ua_lower:
            os = 'Android'
        elif 'ios' in ua_lower or 'iphone' in ua_lower:
            os = 'iOS'
        
        return {
            'device_type': device_type,
            'browser': browser,
            'os': os
        }
    
    def get_referrer_source(self, referrer):
        """Determine the source from referrer URL"""
        if not referrer:
            return 'Direct'
        
        referrer_lower = referrer.lower()
        
        # Social media sources
        social_sources = {
            'facebook.com': 'Facebook',
            'twitter.com': 'Twitter',
            'x.com': 'Twitter',
            'linkedin.com': 'LinkedIn',
            'instagram.com': 'Instagram',
            'youtube.com': 'YouTube',
            'pinterest.com': 'Pinterest',
            'reddit.com': 'Reddit',
            'tiktok.com': 'TikTok'
        }
        
        for domain, source in social_sources.items():
            if domain in referrer_lower:
                return source
        
        # Search engines
        search_engines = {
            'google.': 'Google',
            'bing.': 'Bing',
            'yahoo.': 'Yahoo',
            'duckduckgo.': 'DuckDuckGo',
            'baidu.': 'Baidu'
        }
        
        for domain, source in search_engines.items():
            if domain in referrer_lower:
                return f"{source} Search"
        
        # Email clients
        if 'mail.' in referrer_lower or 'outlook.' in referrer_lower:
            return 'Email'
        
        # Extract domain from referrer
        try:
            parsed = urlparse(referrer)
            domain = parsed.netloc
            if domain:
                return domain
        except:
            pass
        
        return 'Other'
    
    def get_country_from_ip(self, ip_address):
        """Get country from IP address"""
        # This is a placeholder - integrate with GeoIP service
        # For now, return Unknown
        return 'Unknown'
    
    def is_expired(self):
        """Check if URL has expired"""
        if not self.expiry_date:
            return False
        
        return get_datetime(self.expiry_date) < now_datetime()
    
    def validate(self):
        """Validate the document"""
        # Validate URL format
        if not self.original_url.startswith(('http://', 'https://')):
            frappe.throw(_("URL must start with http:// or https://"))
        
        # Validate custom alias if provided
        if self.custom_alias:
            if frappe.db.exists("Short URL", {"short_code": self.custom_alias, "name": ["!=", self.name]}):
                frappe.throw(_("This custom alias is already in use"))
        
        # Check expiry date
        if self.expiry_date and get_datetime(self.expiry_date) < now_datetime():
            frappe.throw(_("Expiry date cannot be in the past"))

def get_permission_query_conditions(user):
    """Return conditions for list queries"""
    if not user:
        user = frappe.session.user
    
    if "System Manager" in frappe.get_roles(user):
        return None
    
    return f"(`tabShort URL`.owner = {frappe.db.escape(user)})"
