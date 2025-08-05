# UTM Shortener - Frappe Cloud Setup Guide

This guide explains how to set up UTM Shortener on Frappe Cloud without requiring nginx configuration.

## How It Works on Frappe Cloud

When installed from the Frappe Cloud marketplace, the UTM Shortener works within your existing site URL structure. No separate nginx configuration is needed!

### Default URL Structure

Your short URLs will follow this pattern:
```
https://your-site.frappe.cloud/s/your-short-code
```

### Custom Domain (Frappe Cloud Pro)

If you have a custom domain on Frappe Cloud:
```
https://yourdomain.com/s/your-short-code
```

## Setup Steps for Frappe Cloud

### Step 1: Install from Marketplace

1. Go to your Frappe Cloud dashboard
2. Navigate to Apps → Marketplace
3. Search for "UTM Shortener"
4. Click "Install" on your site

### Step 2: Configure Settings

1. After installation, go to your site
2. Search for "UTM Shortener Settings"
3. Configure as follows:

```
For Standard Frappe Cloud Sites:
- Short Domain: your-site.frappe.cloud
- Use HTTPS: ✓ (Always checked)
- Custom Domain Enabled: ☐ (Unchecked)
- Fallback to Site URL: ✓ (Checked)

For Custom Domain Sites:
- Short Domain: yourdomain.com
- Use HTTPS: ✓ (Always checked)
- Custom Domain Enabled: ☐ (Unchecked)
- Fallback to Site URL: ✓ (Checked)
```

### Step 3: No Additional Configuration Needed!

The app automatically uses Frappe's built-in routing system. The `/s/` path is handled by the app's routing configuration in `hooks.py`.

## Advanced Setup: Using a Separate Short Domain

If you want to use a completely different domain for short URLs (e.g., `short.link`), you have two options:

### Option 1: External Redirect Service (Recommended)

Use a service like Cloudflare Workers or Vercel to redirect:

1. **Set up Cloudflare Worker:**

```javascript
// Cloudflare Worker Script
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  
  // Extract the short code
  const shortCode = url.pathname.substring(1)
  
  // Redirect to your Frappe Cloud site
  if (shortCode) {
    return Response.redirect(
      `https://your-site.frappe.cloud/s/${shortCode}`,
      301
    )
  }
  
  // Handle root domain
  return new Response('Short URL Service', { status: 200 })
}
```

2. **Configure DNS:**
   - Point your short domain to Cloudflare
   - Deploy the worker
   - Route your domain through the worker

3. **Update UTM Shortener Settings:**
   ```
   Short Domain: short.link
   Use HTTPS: ✓
   Custom Domain Enabled: ✓
   ```

### Option 2: Frappe Cloud Custom Routes (Enterprise)

For enterprise customers, Frappe Cloud support can set up custom routing rules. Contact support with:

1. Your short domain
2. SSL certificate (or use Let's Encrypt)
3. Routing requirements

## How Short URLs Work Without Nginx

The app uses Frappe's built-in routing system:

1. **Route Registration**: The `hooks.py` file registers the `/s/<short_code>` route
2. **Request Handling**: Frappe automatically routes requests to the handler
3. **No Nginx Needed**: Works within Frappe's existing web server configuration

### Technical Details

In `hooks.py`:
```python
website_route_rules = [
    {
        "from_route": "/s/<path:short_code>", 
        "to_route": "utm_shortener.www.s.redirect_short_url"
    }
]
```

This tells Frappe to handle all `/s/*` URLs with our redirect function.

## Testing Your Setup

### 1. Create a Test Campaign

```python
# In Frappe Console
campaign = frappe.get_doc({
    "doctype": "UTM Campaign",
    "campaign_name": "Test Campaign",
    "utm_source": "test",
    "utm_medium": "test",
    "utm_campaign": "test"
}).insert()

print(f"Campaign created: {campaign.name}")
```

### 2. Create a Test URL

```python
short_url = frappe.get_doc({
    "doctype": "Short URL",
    "original_url": "https://example.com",
    "utm_campaign": campaign.name,
    "custom_alias": "test123"
}).insert()

print(f"Short URL: {short_url.short_url}")
```

### 3. Test the Redirect

Visit: `https://your-site.frappe.cloud/s/test123`

You should be redirected to `https://example.com` with UTM parameters.

## URL Examples

### Standard Frappe Cloud Site
```
Original: https://example.com/products
Short URL: https://acme.frappe.cloud/s/prod2024
Final URL: https://example.com/products?utm_source=email&utm_medium=newsletter&utm_campaign=spring2024
```

### Custom Domain on Frappe Cloud
```
Original: https://example.com/services  
Short URL: https://acme.com/s/svc-offer
Final URL: https://example.com/services?utm_source=social&utm_medium=post&utm_campaign=q1-promo
```

## Limitations and Workarounds

### Current Limitations

1. **URL Structure**: Must use `/s/` prefix
2. **Same Domain**: Short URLs share the main site domain
3. **No Root Level**: Can't use `short.link/code` format directly

### Workarounds

1. **Marketing Materials**: 
   - Use QR codes that hide the full URL
   - Use link shorteners that redirect to your short URLs

2. **Social Media**:
   - Most platforms hide the full URL anyway
   - Focus on the tracking rather than aesthetics

3. **Email Campaigns**:
   - Use descriptive link text
   - Track effectiveness through analytics

## Performance on Frappe Cloud

The app is optimized for Frappe Cloud's infrastructure:

1. **Caching**: Utilizes Frappe Cloud's Redis cache
2. **CDN**: Static assets served through Frappe Cloud CDN
3. **Auto-scaling**: Handles traffic spikes automatically
4. **Monitoring**: Built-in monitoring and alerts

## Support

For Frappe Cloud specific issues:

1. **App Issues**: [GitHub Issues](https://github.com/chinmaybhatk/utm_shortener/issues)
2. **Frappe Cloud Issues**: support@frappe.cloud
3. **Custom Domain Setup**: Contact Frappe Cloud support

## Best Practices for Frappe Cloud

1. **Use Descriptive Aliases**: Since URLs are longer, make aliases meaningful
2. **Leverage QR Codes**: Great for print materials
3. **Focus on Analytics**: The tracking is more important than URL length
4. **Use Templates**: Create reusable UTM templates for consistency

## FAQ

**Q: Can I use a completely different domain like short.link?**
A: Not directly on Frappe Cloud, but you can use Cloudflare Workers or similar services to redirect.

**Q: Will the /s/ prefix affect tracking?**
A: No, tracking works exactly the same regardless of URL structure.

**Q: Can I remove the /s/ prefix?**
A: Not on Frappe Cloud, as it's needed to distinguish short URLs from other routes.

**Q: Is the app slower on Frappe Cloud?**
A: No, it's actually optimized for Frappe Cloud's infrastructure and performs very well.
