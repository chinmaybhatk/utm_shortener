import frappe

def execute():
    """Fix existing Short URLs that have null short_url field"""
    
    # Get all Short URLs with null short_url
    short_urls = frappe.get_all("Short URL", 
        filters={"short_url": ["is", "null"]},
        fields=["name", "short_code"]
    )
    
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
