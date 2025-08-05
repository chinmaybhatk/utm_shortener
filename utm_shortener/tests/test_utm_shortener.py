#!/usr/bin/env python
"""
UTM Shortener Testing Script
Run this to test your UTM shortener setup and verify everything is working correctly.
"""

import frappe
import requests
import json
from datetime import datetime, timedelta

def test_utm_shortener():
    """Run comprehensive tests for UTM shortener"""
    print("=" * 60)
    print("UTM SHORTENER TESTING SCRIPT")
    print("=" * 60)
    
    results = {
        "passed": 0,
        "failed": 0,
        "tests": []
    }
    
    # Test 1: Check Settings
    print("\n1. Testing UTM Shortener Settings...")
    try:
        settings = frappe.get_single("UTM Shortener Settings")
        print(f"   ✓ Settings found")
        print(f"   - Domain: {settings.short_domain}")
        print(f"   - HTTPS: {'Yes' if settings.use_https else 'No'}")
        print(f"   - Rate Limit: {settings.rate_limit_per_hour}/hour")
        results["passed"] += 1
        results["tests"].append({"name": "Settings Check", "status": "PASSED"})
    except Exception as e:
        print(f"   ✗ Settings Error: {str(e)}")
        results["failed"] += 1
        results["tests"].append({"name": "Settings Check", "status": "FAILED", "error": str(e)})
    
    # Test 2: Create Campaign
    print("\n2. Testing Campaign Creation...")
    try:
        campaign_name = f"Test Campaign {datetime.now().strftime('%Y%m%d%H%M%S')}"
        campaign = frappe.get_doc({
            "doctype": "UTM Campaign",
            "campaign_name": campaign_name,
            "utm_source": "test",
            "utm_medium": "script",
            "utm_campaign": "test-campaign",
            "utm_term": "testing",
            "utm_content": "test-content",
            "description": "Automated test campaign"
        })
        campaign.insert()
        print(f"   ✓ Campaign created: {campaign.name}")
        results["passed"] += 1
        results["tests"].append({"name": "Campaign Creation", "status": "PASSED", "campaign_id": campaign.name})
    except Exception as e:
        print(f"   ✗ Campaign Error: {str(e)}")
        results["failed"] += 1
        results["tests"].append({"name": "Campaign Creation", "status": "FAILED", "error": str(e)})
        return results
    
    # Test 3: Create Short URL
    print("\n3. Testing Short URL Creation...")
    try:
        short_url = frappe.get_doc({
            "doctype": "Short URL",
            "original_url": "https://example.com/test-page",
            "utm_campaign": campaign.name,
            "custom_alias": f"test-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "expiry_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        })
        short_url.insert()
        print(f"   ✓ Short URL created: {short_url.short_url}")
        print(f"   - Short Code: {short_url.short_code}")
        print(f"   - UTM URL: {short_url.generated_utm_url}")
        results["passed"] += 1
        results["tests"].append({
            "name": "Short URL Creation", 
            "status": "PASSED", 
            "short_url": short_url.short_url,
            "short_code": short_url.short_code
        })
    except Exception as e:
        print(f"   ✗ Short URL Error: {str(e)}")
        results["failed"] += 1
        results["tests"].append({"name": "Short URL Creation", "status": "FAILED", "error": str(e)})
        return results
    
    # Test 4: Test Click Tracking
    print("\n4. Testing Click Tracking...")
    try:
        request_data = {
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0",
            "referrer": "https://facebook.com"
        }
        
        # Simulate a click
        redirect_url = short_url.track_click(request_data)
        print(f"   ✓ Click tracked successfully")
        print(f"   - Redirect URL: {redirect_url}")
        print(f"   - Total Clicks: {short_url.clicks}")
        
        # Check if click log was created
        click_logs = frappe.get_all("URL Click Log", 
            filters={"short_url": short_url.name},
            fields=["name", "timestamp", "referrer_source", "device_type"]
        )
        
        if click_logs:
            print(f"   ✓ Click log created: {len(click_logs)} entries")
            print(f"   - Source: {click_logs[0].referrer_source}")
            print(f"   - Device: {click_logs[0].device_type}")
        
        results["passed"] += 1
        results["tests"].append({"name": "Click Tracking", "status": "PASSED"})
    except Exception as e:
        print(f"   ✗ Click Tracking Error: {str(e)}")
        results["failed"] += 1
        results["tests"].append({"name": "Click Tracking", "status": "FAILED", "error": str(e)})
    
    # Test 5: Analytics API
    print("\n5. Testing Analytics APIs...")
    try:
        # Test URL analytics
        url_analytics = frappe.call(
            'utm_shortener.utm_shortener.api.get_url_analytics',
            short_code=short_url.short_code
        )
        print(f"   ✓ URL Analytics API working")
        print(f"   - Total Clicks: {url_analytics['short_url']['total_clicks']}")
        
        # Test campaign analytics
        campaign_analytics = frappe.call(
            'utm_shortener.utm_shortener.api.get_campaign_analytics',
            campaign_id=campaign.name
        )
        print(f"   ✓ Campaign Analytics API working")
        print(f"   - Total URLs: {campaign_analytics['analytics']['total_urls']}")
        print(f"   - Total Clicks: {campaign_analytics['analytics']['total_clicks']}")
        
        results["passed"] += 1
        results["tests"].append({"name": "Analytics APIs", "status": "PASSED"})
    except Exception as e:
        print(f"   ✗ Analytics API Error: {str(e)}")
        results["failed"] += 1
        results["tests"].append({"name": "Analytics APIs", "status": "FAILED", "error": str(e)})
    
    # Test 6: Bulk Creation
    print("\n6. Testing Bulk URL Creation...")
    try:
        bulk_urls = [
            {"url": "https://example.com/page1", "alias": f"bulk1-{datetime.now().strftime('%H%M%S')}"},
            {"url": "https://example.com/page2", "alias": f"bulk2-{datetime.now().strftime('%H%M%S')}"},
            {"url": "https://example.com/page3"}  # Auto-generated alias
        ]
        
        bulk_result = frappe.call(
            'utm_shortener.utm_shortener.api.bulk_create_utm_urls',
            campaign=campaign.name,
            url_list=bulk_urls
        )
        
        print(f"   ✓ Bulk creation successful")
        print(f"   - Created: {bulk_result['created_count']} URLs")
        print(f"   - Errors: {bulk_result['error_count']}")
        
        results["passed"] += 1
        results["tests"].append({"name": "Bulk URL Creation", "status": "PASSED"})
    except Exception as e:
        print(f"   ✗ Bulk Creation Error: {str(e)}")
        results["failed"] += 1
        results["tests"].append({"name": "Bulk URL Creation", "status": "FAILED", "error": str(e)})
    
    # Test 7: URL Expiration
    print("\n7. Testing URL Expiration...")
    try:
        # Create an expired URL
        expired_url = frappe.get_doc({
            "doctype": "Short URL",
            "original_url": "https://example.com/expired",
            "utm_campaign": campaign.name,
            "custom_alias": f"expired-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "expiry_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        })
        # This should fail validation
        try:
            expired_url.insert()
            print(f"   ✗ Expiration validation failed - expired URL was created")
            results["failed"] += 1
            results["tests"].append({"name": "URL Expiration", "status": "FAILED", "error": "Expired URL was created"})
        except frappe.ValidationError:
            print(f"   ✓ Expiration validation working correctly")
            results["passed"] += 1
            results["tests"].append({"name": "URL Expiration", "status": "PASSED"})
    except Exception as e:
        print(f"   ✗ Expiration Test Error: {str(e)}")
        results["failed"] += 1
        results["tests"].append({"name": "URL Expiration", "status": "FAILED", "error": str(e)})
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {results['passed'] + results['failed']}")
    print(f"Passed: {results['passed']} ✓")
    print(f"Failed: {results['failed']} ✗")
    print(f"Success Rate: {(results['passed'] / (results['passed'] + results['failed']) * 100):.1f}%")
    
    # Cleanup option
    print("\n" + "=" * 60)
    cleanup = input("Do you want to clean up test data? (y/n): ")
    if cleanup.lower() == 'y':
        cleanup_test_data(campaign.name if 'campaign' in locals() else None)
    
    return results

def cleanup_test_data(campaign_name=None):
    """Clean up test data created during testing"""
    print("\nCleaning up test data...")
    
    try:
        # Delete test URLs
        if campaign_name:
            test_urls = frappe.get_all("Short URL", 
                filters={"utm_campaign": campaign_name},
                fields=["name"]
            )
            for url in test_urls:
                frappe.delete_doc("Short URL", url.name, ignore_permissions=True)
            print(f"   ✓ Deleted {len(test_urls)} test URLs")
            
            # Delete test campaign
            frappe.delete_doc("UTM Campaign", campaign_name, ignore_permissions=True)
            print(f"   ✓ Deleted test campaign")
        
        # Delete test click logs
        test_logs = frappe.get_all("URL Click Log",
            filters={"ip_address": "192.168.1.1"},
            fields=["name"]
        )
        for log in test_logs:
            frappe.delete_doc("URL Click Log", log.name, ignore_permissions=True)
        print(f"   ✓ Deleted {len(test_logs)} test click logs")
        
        frappe.db.commit()
        print("   ✓ Cleanup completed")
        
    except Exception as e:
        print(f"   ✗ Cleanup Error: {str(e)}")

if __name__ == "__main__":
    # Run the tests
    test_utm_shortener()
