# UTM Link Shortener - Release Notes v1.1.0

**Release Date:** June 6, 2025  
**Version:** 1.1.0  
**App Name:** UTM Link Shortener  
**Compatible with:** Frappe v15+, ERPNext v15+ (optional)

---

## 🎉 Overview

This release introduces automatic URL generation with UTM parameters, enhanced user experience features, and improved short URL management capabilities. The UTM Link Shortener now provides a complete solution for marketing campaign tracking with seamless URL generation and one-click sharing functionality.

---

## 🚀 New Features

### 1. **Automatic UTM URL Generation**
- **Description:** URLs with UTM parameters are now automatically generated when you provide a base URL in UTM Campaign
- **Benefit:** Eliminates manual URL construction, reducing errors and saving time
- **How it works:**
  - Enter your base URL in the UTM Campaign form
  - The system automatically combines it with UTM parameters
  - Full URL is generated and stored in real-time

### 2. **One-Click URL Copying**
- **Description:** Copy generated URLs to clipboard with a single click
- **Benefit:** Faster workflow for sharing campaign URLs across channels
- **Available in:**
  - UTM Campaign form: "Copy Full URL" button
  - Short URL form: "Copy Short URL" button

### 3. **Real-Time URL Preview**
- **Description:** See live preview of URLs as you type or modify parameters
- **Benefit:** Immediate feedback ensures URLs are correct before saving
- **Features:**
  - Visual preview in alert boxes
  - Automatic updates when parameters change
  - Shows both full URL and shortened versions

### 4. **Enhanced Short URL Management**
- **Description:** Improved form interface with auto-generated short codes
- **Benefit:** Simpler URL creation process with better visual feedback
- **Improvements:**
  - Short code field now shows as "auto-generated"
  - Better field descriptions and help text
  - Visual indicators for URL status

### 5. **Functional URL Redirects**
- **Description:** Short URLs now properly redirect to target destinations
- **Benefit:** Complete end-to-end functionality for URL shortening
- **Route Pattern:** `/s/[SHORT_CODE]`
- **Features:**
  - Automatic click tracking
  - Analytics logging
  - Expiry date checking
  - Status validation

---

## 🔧 Technical Improvements

### Backend Enhancements
1. **URL Generation Logic**
   - Added `generate_utm_url()` method to UTM Campaign
   - Automatic URL construction in `before_save` hook
   - Proper URL encoding for special characters

2. **Routing System**
   - Implemented website route rules for `/s/` pattern
   - Added redirect handlers in multiple formats for compatibility
   - Guest access enabled for public URL redirects

3. **Field Management**
   - New fields: `base_url` and `full_url` in UTM Campaign
   - Updated field properties for better UX
   - Database patches for smooth migration

### Frontend Enhancements
1. **Client Scripts**
   - Real-time URL generation on form
   - Advanced clipboard functionality with fallback
   - Form validation and user feedback

2. **UI/UX Improvements**
   - Alert boxes for URL display
   - Descriptive help text
   - Responsive button placement

---

## 📊 Sample Data Updates

The release includes comprehensive sample data for testing:

### Sample UTM Campaigns
1. **Black Friday Sale 2025**
   - Email marketing campaign
   - Base URL: `https://shop.example.com/black-friday-deals`

2. **Summer Collection Launch**
   - Instagram social campaign
   - Includes UTM term: "beachwear"

3. **Google Ads - Electronics**
   - Paid search campaign
   - Includes all UTM parameters

4. **LinkedIn B2B Outreach**
   - B2B software demo campaign
   - Professional targeting

5. **Newsletter - Monthly Digest**
   - Email newsletter campaign
   - Mailchimp integration ready

### Sample Short URLs
- 7 pre-configured short URLs with various click counts
- Examples: BF2025, SUMMER25, TECH01, B2BDEMO, NEWS06
- Mix of campaign-linked and standalone URLs

---

## 🔄 Migration Guide

### For Existing Installations

1. **Backup your data**
   ```bash
   bench --site your-site.local backup
   ```

2. **Pull the latest updates**
   ```bash
   cd frappe-bench/apps/utm_shortener
   git pull origin main
   ```

3. **Run migrations**
   ```bash
   bench --site your-site.local migrate
   bench --site your-site.local clear-cache
   ```

4. **Restart services**
   ```bash
   bench restart
   ```

### For New Installations

1. **Clone the repository**
   ```bash
   cd frappe-bench/apps
   git clone https://github.com/chinmaybhatk/utm_shortener.git
   ```

2. **Install the app**
   ```bash
   bench --site your-site.local install-app utm_shortener
   ```

3. **Run initial setup**
   ```bash
   bench --site your-site.local migrate
   ```

---

## 💻 API Endpoints

### New/Updated Endpoints

1. **Generate UTM URL**
   ```
   POST /api/method/utm_shortener.utm_shortener.doctype.utm_campaign.utm_campaign.generate_utm_url
   ```
   - Parameters: `campaign_name`, `base_url`
   - Returns: Generated URL with UTM parameters

2. **Copy UTM URL**
   ```
   GET /api/method/utm_shortener.utm_shortener.doctype.utm_campaign.utm_campaign.copy_utm_url
   ```
   - Parameters: `campaign_name`
   - Returns: Full URL for copying

3. **Redirect Short URL**
   ```
   GET /s/[SHORT_CODE]
   ```
   - Guest access enabled
   - Tracks click and redirects to target URL

---

## 🐛 Bug Fixes

1. **Fixed syntax error in install_sample_data.py**
   - Resolved unterminated string literal issue
   - Improved error handling in sample data creation

2. **Fixed Short URL form validation**
   - Short code field now properly auto-generates
   - Removed mandatory validation on form level

3. **Fixed routing configuration**
   - Added proper website route rules
   - Implemented multiple redirect handlers for compatibility

---

## 📝 Known Issues

1. **UTM Shortener Settings DocType**
   - Currently needs manual creation
   - Will be automated in next release

2. **Geolocation Features**
   - Placeholder implementation
   - Requires external service integration

---

## 🔒 Security Considerations

1. **Guest Access**
   - Short URL redirects allow guest access by design
   - Rate limiting should be configured in settings

2. **URL Validation**
   - Basic URL format validation implemented
   - Domain blocking feature available but requires settings

3. **Click Tracking**
   - IP addresses are logged (truncated to 15 chars)
   - User agents stored for analytics

---

## 📈 Performance Impact

- **Minimal overhead** for URL generation
- **Fast redirects** with single database query
- **Efficient click tracking** with async logging
- **Caching** implemented for frequently accessed URLs

---

## 🤝 Acknowledgments

Special thanks to the Frappe community for their support and feedback. This release was developed to enhance marketing campaign management and provide a seamless URL shortening experience.

---

## 📞 Support

- **GitHub Issues:** [Report bugs or request features](https://github.com/chinmaybhatk/utm_shortener/issues)
- **Documentation:** [Full documentation](https://github.com/chinmaybhatk/utm_shortener/blob/main/README.md)
- **Community:** [Frappe Forum](https://discuss.frappe.io)

---

## 🚀 What's Next (Roadmap)

### v1.2.0 (Planned)
- QR code generation for short URLs
- Advanced analytics dashboard
- Bulk URL import/export
- API rate limiting improvements
- Custom domain support

### v1.3.0 (Future)
- A/B testing for URLs
- Integration with Google Analytics
- Scheduled URL activation/deactivation
- Team collaboration features

---

**Thank you for using UTM Link Shortener!** 🎉

*Made with ❤️ for the Frappe community*