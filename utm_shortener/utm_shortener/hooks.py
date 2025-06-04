app_name = "utm_shortener"
app_title = "UTM Link Shortener"
app_publisher = "Chinmay Bhatk"
app_description = "UTM parameter generation and URL shortening"
app_version = "1.0.0"
app_color = "blue"
app_email = "chinmay@example.com"
app_license = "MIT"

# Apps
required_apps = ["frappe"]

# Website routes for short URL redirects
website_route_rules = [
    {"from_route": "/<path:short_code>", "to_route": "utm_shortener.utm_shortener.api.redirect_short_url"}
]

# Scheduled tasks
scheduler_events = {
    "daily": [
        "utm_shortener.utm_shortener.tasks.cleanup_expired_urls",
        "utm_shortener.utm_shortener.tasks.update_geolocation_data"
    ],
    "hourly": [
        "utm_shortener.utm_shortener.tasks.reset_rate_limits"
    ]
}

# Document Events
doc_events = {
    "UTM Campaign": {
        "before_save": "utm_shortener.utm_shortener.doctype.utm_campaign.utm_campaign.validate_utm_parameters"
    },
    "Short URL": {
        "before_save": "utm_shortener.utm_shortener.doctype.short_url.short_url.generate_short_code"
    }
}

# Permissions
permission_query_conditions = {
    "UTM Campaign": "utm_shortener.utm_shortener.doctype.utm_campaign.utm_campaign.get_permission_query_conditions",
}

# Web form integration
webform_list_context = "utm_shortener.utm_shortener.utils.get_webform_list_context"

# Boot session
boot_session = "utm_shortener.utm_shortener.utils.boot_session"