# Changelog

All notable changes to the UTM Link Shortener project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-06-06

### Added
- Automatic UTM URL generation with base URL field in UTM Campaign
- One-click copy to clipboard functionality for generated URLs
- Real-time URL preview as you type
- Client-side form enhancements for better user experience
- Functional short URL redirects with pattern `/s/[SHORT_CODE]`
- Click tracking and analytics logging for all short URLs
- Sample data with 5 UTM campaigns and 7 short URLs
- Comprehensive API documentation
- Database patches for smooth upgrades

### Changed
- Short code field now auto-generates and shows as read-only
- Improved form validation and user feedback
- Enhanced URL display with visual alert boxes
- Updated field descriptions for better clarity

### Fixed
- Syntax error in install_sample_data.py
- Short URL form validation issues
- Website routing configuration
- Field visibility and requirement issues

### Technical
- Added website_route_rules in hooks.py
- Implemented redirect handlers for short URLs
- Created client scripts for both UTM Campaign and Short URL forms
- Added two database migration patches

## [1.0.0] - 2025-06-04

### Added
- Initial release of UTM Link Shortener
- Core URL shortening functionality
- UTM parameter generation and management
- Basic click tracking and analytics
- DocTypes: UTM Campaign, Short URL, URL Click Log, UTM Template
- API endpoints for URL creation and analytics
- Rate limiting support
- Custom alias support
- URL expiration management
- Basic permission system

### Technical
- Frappe v15 compatibility
- ERPNext v15 compatibility (optional)
- Python 3.8+ support

---

For detailed release information, see [RELEASE_NOTES.md](RELEASE_NOTES.md)