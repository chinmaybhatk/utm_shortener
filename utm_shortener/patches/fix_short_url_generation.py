import frappe

def execute():
    """Fix existing Short URLs that have null short_url field"""
    
    # Get all Short URLs where short_url is null or empty
    short_urls = frappe.db.sql("""
        SELECT name, short_code 
        FROM `tabShort URL` 
        WHERE short_url IS NULL OR short_url = ''
    """, as_dict=True)
    
    if short_urls:
        print(f"Found {len(short_urls)} Short URLs to fix")
        
        for url in short_urls:
            try:
                doc = frappe.get_doc("Short URL", url.name)
                # Regenerate the short URL
                doc.short_url = doc.get_short_url()
                doc.save(ignore_permissions=True)
                print(f"Fixed Short URL: {url.name} - {doc.short_url}")
                
            except Exception as e:
                print(f"Error fixing Short URL {url.name}: {str(e)}")
        
        frappe.db.commit()
        print("Migration completed successfully")
    else:
        print("No Short URLs need fixing")
