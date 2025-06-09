import frappe
from frappe.model.document import Document
import shortuuid
from datetime import datetime, timedelta

class UTMLink(Document):
    def before_insert(self):
        # Generate unique short code
        self.short_code = self._generate_short_code()
        
        # Set default expiry if not specified
        if not self.expiry_date:
            self.expiry_date = datetime.now() + timedelta(days=90)
    
    def _generate_short_code(self):
        """
        Generate a unique short code
        """
        while True:
            code = shortuuid.uuid()[:8]
            # Ensure unique code
            if not frappe.db.exists('UTM Link', {'short_code': code}):
                return code
    
    def is_expired(self):
        """
        Check if link is expired
        """
        return (
            self.expiry_date and 
            frappe.utils.getdate(self.expiry_date) < frappe.utils.getdate()
        )
    
    def track_click(self, request):
        """
        Track individual link click
        """
        # Create click tracking entry
        frappe.get_doc({
            'doctype': 'UTM Click Tracking',
            'utm_link': self.name,
            'clicked_at': frappe.utils.now(),
            'ip_address': request.remote_addr,
            'user_agent': str(request.user_agent),
            'referrer': request.referrer or ''
        }).insert()
        
        # Update total clicks
        self.total_clicks = (self.total_clicks or 0) + 1
        self.last_clicked = frappe.utils.now()
        self.save()
        
        return self.original_url