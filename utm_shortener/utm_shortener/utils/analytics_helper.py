import frappe

class UTMAnalytics:
    @staticmethod
    def get_performance_overview(filters=None):
        """
        Comprehensive UTM link performance analytics
        """
        performance_query = """
            SELECT 
                utm.short_code,
                utm.original_url,
                utm.utm_campaign,
                COUNT(clicks.name) as total_clicks,
                MAX(clicks.clicked_at) as last_clicked
            FROM `tabUTM Link` utm
            LEFT JOIN `tabUTM Click Tracking` clicks 
                ON utm.name = clicks.utm_link
            GROUP BY utm.name
        """
        return frappe.db.sql(performance_query, as_dict=True)
    
    @staticmethod
    def get_device_analytics(filters=None):
        """
        Device and platform analytics
        """
        device_query = """
            SELECT 
                CASE 
                    WHEN user_agent LIKE '%Windows%' THEN 'Windows'
                    WHEN user_agent LIKE '%Macintosh%' THEN 'Mac'
                    WHEN user_agent LIKE '%Linux%' THEN 'Linux'
                    ELSE 'Other'
                END as platform,
                COUNT(*) as platform_count
            FROM `tabUTM Click Tracking`
            GROUP BY platform
        """
        return frappe.db.sql(device_query, as_dict=True)
    
    @staticmethod
    def get_time_series_clicks(filters=None):
        """
        Time-based click analysis
        """
        time_series_query = """
            SELECT 
                DATE(clicked_at) as click_date,
                COUNT(*) as daily_clicks
            FROM `tabUTM Click Tracking`
            GROUP BY click_date
            ORDER BY click_date
        """
        return frappe.db.sql(time_series_query, as_dict=True)