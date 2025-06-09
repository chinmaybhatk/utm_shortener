from . import __version__ as app_version

app_name = "utm_shortener"
app_title = "UTM Shortener"
app_publisher = "Chinmay Bhat"
app_description = "Advanced UTM Link Tracking Solution"
app_version = app_version
app_email = "chinmaybhatk@gmail.com"
app_license = "MIT"

# Logging and Installation Hooks
before_install = "utm_shortener.utils.install.before_install"
after_install = "utm_shortener.utils.install.after_install"

# Fixtures for consistent DocType installation
fixtures = [
    {
        "dt": "DocType", 
        "filters": [
            ["name", "in", ["UTM Link", "UTM Click Tracking"]]
        ]
    }
]

# Web routing for UTM links
web_routes = [
    {"name": "utm", "page_name": "utm", "generator": "UTM Link"}
]

# Permissions
permission_query_conditions = {
    "UTM Link": "utm_shortener.utils.permissions.get_permission_query_conditions",
    "UTM Click Tracking": "utm_shortener.utils.permissions.get_permission_query_conditions"
}

# Dashboard configuration
dashboards = {
    "UTM Link": "utm_shortener/doctype/utm_link/utm_link_dashboard.py"
}

# Add these settings to help with troubleshooting and performance
app_include_js = ["/assets/utm_shortener/js/utm_shortener.js"]
app_include_css = ["/assets/utm_shortener/css/utm_shortener.css"]