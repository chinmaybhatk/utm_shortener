import frappe

def get_permission_query_conditions(user=None):
    """
    Custom permission handling for UTM Link and Click Tracking
    """
    if not user:
        user = frappe.session.user

    # Admin always has full access
    if 'System Manager' in frappe.get_roles(user):
        return None

    # Restrict access based on roles
    return f"""
        (`tabUTM Link`.owner = '{user}' 
        OR 'UTM Analyst' IN (
            SELECT DISTINCT role 
            FROM `tabHas Role` 
            WHERE `tabHas Role`.parent = '{user}'
        ))
    """

def has_permission(doc, user=None, permission_type='read'):
    """
    Additional permission checks
    """
    if not user:
        user = frappe.session.user

    # System Managers always have access
    if 'System Manager' in frappe.get_roles(user):
        return True

    # Owner always has full access to their own documents
    if doc.owner == user:
        return True

    # Check if user has UTM Analyst role
    if 'UTM Analyst' in frappe.get_roles(user):
        return True

    return False