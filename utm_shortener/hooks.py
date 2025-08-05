from . import __version__ as app_version

app_name = "utm_shortener"
app_title = "UTM Shortener"
app_publisher = "Chinmay Bhat"
app_description = "Advanced UTM Link Tracking Solution"
app_version = app_version
app_email = "chinmaybhatk@gmail.com"
app_license = "MIT"

# Included Apps
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/utm_shortener/css/utm_shortener.css"
app_include_js = "/assets/utm_shortener/js/quick_url_shortener.js"

# include js, css files in header of web template
# web_include_css = "/assets/utm_shortener/css/utm_shortener.css"
# web_include_js = "/assets/utm_shortener/js/utm_shortener.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "utm_shortener/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Short URL" : "public/js/short_url.js",
    "UTM Campaign" : "public/js/utm_campaign.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "utm_shortener.utils.jinja_methods",
#	"filters": "utm_shortener.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "utm_shortener.install.before_install"
# after_install = "utm_shortener.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "utm_shortener.uninstall.before_uninstall"
# after_uninstall = "utm_shortener.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "utm_shortener.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
    "Short URL": "utm_shortener.utm_shortener.doctype.short_url.short_url.get_permission_query_conditions",
    "UTM Campaign": "utm_shortener.utm_shortener.doctype.utm_campaign.utm_campaign.get_permission_query_conditions",
}

# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    "daily": [
        "utm_shortener.tasks.cleanup_expired_urls"
    ],
    "hourly": [
        "utm_shortener.tasks.reset_rate_limits"
    ]
}

# Testing
# -------

# before_tests = "utm_shortener.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "utm_shortener.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "utm_shortener.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Request Events
# ----------------
# before_request = ["utm_shortener.utils.before_request"]
# after_request = ["utm_shortener.utils.after_request"]

# Job Events
# ----------
# before_job = ["utm_shortener.utils.before_job"]
# after_job = ["utm_shortener.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"utm_shortener.auth.validate"
# ]

# Additional Website Route Rules
website_route_rules = [
    {"from_route": "/s/<path:short_code>", "to_route": "utm_shortener.www.s.redirect_short_url"},
    {"from_route": "/shorten", "to_route": "utm_shortener.www.shorten"},
]

# Fixtures
fixtures = [
    {
        "dt": "DocType",
        "filters": [
            ["name", "in", ["Short URL", "UTM Campaign", "URL Click Log", "UTM Template", "UTM Shortener Settings"]]
        ]
    },
    {
        "dt": "Custom Field",
        "filters": [
            ["dt", "in", ["Short URL", "UTM Campaign"]]
        ]
    }
]

# Additional app configuration
app_icon = "octicon octicon-link"
app_color = "#4CAF50"
app_email = "chinmaybhatk@gmail.com"
app_license = "MIT"

# Add to global search
global_search_doctypes = {
    "Default": [
        {"doctype": "Short URL", "index": 0},
        {"doctype": "UTM Campaign", "index": 1}
    ]
}

# Website context
website_context = {
    "favicon": "/assets/utm_shortener/images/favicon.png",
    "app_name": "UTM Shortener"
}
