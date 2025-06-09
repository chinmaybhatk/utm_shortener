__version__ = "0.1.0"

# Ensure module-level imports and initializations
import frappe

def get_context(context):
    """
    Global context setup for the app
    """
    context.utm_shortener_version = __version__

def on_session_creation(login_manager):
    """
    Hook for session creation logging
    """
    try:
        frappe.log_error(f"UTM Shortener: Session created for user {login_manager.user}")
    except Exception as e:
        frappe.log_error(f"UTM Shortener Session Log Error: {str(e)}")