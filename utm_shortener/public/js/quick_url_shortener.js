frappe.ui.form.on('Short URL', {
    refresh: function(frm) {
        // Add custom buttons
        if (frm.doc.short_url) {
            frm.add_custom_button(__('Copy Short URL'), function() {
                frappe.utils.copy_to_clipboard(frm.doc.short_url);
                frappe.show_alert({
                    message: __('Short URL copied to clipboard'),
                    indicator: 'green'
                });
            });
            
            frm.add_custom_button(__('View Analytics'), function() {
                frappe.set_route('query-report', 'URL Click Analytics', {
                    short_url: frm.doc.name
                });
            });
            
            frm.add_custom_button(__('Download QR Code'), function() {
                if (frm.doc.qr_code) {
                    const link = document.createElement('a');
                    link.download = `qr-${frm.doc.short_code}.png`;
                    link.href = frm.doc.qr_code;
                    link.click();
                }
            });
        }
        
        // Show URL preview
        if (frm.doc.short_url) {
            frm.set_df_property('short_url', 'description', 
                `<div style="padding: 10px; background: #e3f2fd; border-radius: 4px; margin-top: 10px;">
                    <strong>Your short URL:</strong><br>
                    <a href="${frm.doc.short_url}" target="_blank" style="font-size: 16px; color: #1976d2;">
                        ${frm.doc.short_url}
                    </a>
                    <button class="btn btn-xs btn-default" style="margin-left: 10px;" 
                        onclick="frappe.utils.copy_to_clipboard('${frm.doc.short_url}'); 
                        frappe.show_alert('Copied!', 3);">
                        Copy
                    </button>
                </div>`
            );
        }
        
        // Show click stats
        if (frm.doc.clicks > 0) {
            frm.dashboard.add_indicator(__('Total Clicks: {0}', [frm.doc.clicks]), 'blue');
            if (frm.doc.last_clicked) {
                frm.dashboard.add_indicator(__('Last Click: {0}', [frappe.datetime.prettyDate(frm.doc.last_clicked)]), 'green');
            }
        }
    },
    
    onload: function(frm) {
        // Set default expiry date to 1 year from now
        if (frm.is_new() && !frm.doc.expiry_date) {
            frm.set_value('expiry_date', frappe.datetime.add_months(frappe.datetime.get_today(), 12));
        }
    },
    
    original_url: function(frm) {
        // Auto-generate alias suggestion based on URL
        if (frm.doc.original_url && !frm.doc.custom_alias) {
            try {
                const url = new URL(frm.doc.original_url);
                const pathname = url.pathname.replace(/\/$/, '');
                const lastPart = pathname.split('/').pop();
                
                if (lastPart && lastPart.length > 3) {
                    // Clean and suggest alias
                    const suggestion = lastPart
                        .toLowerCase()
                        .replace(/[^a-z0-9-]/g, '-')
                        .replace(/-+/g, '-')
                        .replace(/^-|-$/g, '')
                        .substring(0, 20);
                    
                    frm.set_value('custom_alias', suggestion);
                }
            } catch (e) {
                // Invalid URL, ignore
            }
        }
    }
});

// Add keyboard shortcut
frappe.ui.keys.add_shortcut({
    shortcut: 'ctrl+shift+u',
    action: () => {
        frappe.new_doc('Short URL');
    },
    description: __('Create new Short URL'),
    page: frappe.get_route()[0]
});

// Add quick action to navbar
$(document).ready(function() {
    if (!$('#navbar-quick-url-shortener').length) {
        $('.navbar-right').prepend(`
            <li id="navbar-quick-url-shortener">
                <a class="btn btn-default btn-sm" 
                   style="margin-top: 8px; margin-right: 10px;"
                   onclick="frappe.ui.toolbar.quick_shorten_url()">
                    🔗 Shorten URL
                </a>
            </li>
        `);
    }
});

// Quick URL shortener dialog
frappe.ui.toolbar.quick_shorten_url = function() {
    const dialog = new frappe.ui.Dialog({
        title: '🔗 Quick URL Shortener',
        fields: [
            {
                fieldname: 'original_url',
                fieldtype: 'Data',
                label: 'URL to Shorten',
                reqd: 1,
                placeholder: 'https://example.com/long-url',
                description: 'Paste the URL you want to shorten'
            },
            {
                fieldname: 'section_break_1',
                fieldtype: 'Section Break',
                label: 'Optional Settings',
                collapsible: 1,
                collapsible_depends_on: 'eval:false'
            },
            {
                fieldname: 'custom_alias',
                fieldtype: 'Data',
                label: 'Custom Alias',
                placeholder: 'my-custom-link',
                description: 'Leave empty for auto-generated code'
            },
            {
                fieldname: 'utm_campaign',
                fieldtype: 'Link',
                label: 'Campaign',
                options: 'UTM Campaign',
                filters: {
                    'status': 'Active'
                },
                description: 'Select campaign for tracking'
            },
            {
                fieldname: 'expiry_date',
                fieldtype: 'Date',
                label: 'Expiry Date',
                default: frappe.datetime.add_months(frappe.datetime.get_today(), 12)
            }
        ],
        primary_action_label: 'Create Short URL',
        primary_action: function(values) {
            dialog.hide();
            
            frappe.call({
                method: 'utm_shortener.utm_shortener.api.create_short_url',
                args: {
                    original_url: values.original_url,
                    custom_alias: values.custom_alias,
                    utm_campaign: values.utm_campaign,
                    expiry_date: values.expiry_date
                },
                callback: function(r) {
                    if (r.message && r.message.success) {
                        const short_url = r.message.short_url;
                        
                        // Show result dialog
                        const result_dialog = new frappe.ui.Dialog({
                            title: '✅ URL Shortened Successfully!',
                            indicator: 'green',
                            fields: [
                                {
                                    fieldtype: 'HTML',
                                    fieldname: 'result_html',
                                    options: `
                                        <div style="text-align: center; padding: 20px;">
                                            <p style="font-size: 14px; color: #666; margin-bottom: 10px;">
                                                Your shortened URL is ready:
                                            </p>
                                            <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; 
                                                        border: 2px solid #4CAF50; margin: 20px 0;">
                                                <input type="text" value="${short_url}" 
                                                       style="width: 100%; border: none; background: transparent; 
                                                              text-align: center; font-size: 16px; font-weight: 500;"
                                                       readonly id="short-url-input">
                                            </div>
                                            <div style="margin-top: 20px;">
                                                <button class="btn btn-primary" onclick="
                                                    document.getElementById('short-url-input').select();
                                                    document.execCommand('copy');
                                                    frappe.show_alert('Copied to clipboard!', 3);
                                                ">
                                                    📋 Copy to Clipboard
                                                </button>
                                                <button class="btn btn-default" onclick="
                                                    window.open('${short_url}', '_blank');
                                                ">
                                                    🔗 Test URL
                                                </button>
                                            </div>
                                        </div>
                                    `
                                }
                            ]
                        });
                        
                        result_dialog.show();
                        
                        // Also show in notification
                        frappe.show_alert({
                            message: __('Short URL created: {0}', [short_url]),
                            indicator: 'green',
                            actions: [
                                {
                                    action: function() {
                                        frappe.utils.copy_to_clipboard(short_url);
                                        frappe.show_alert('Copied!', 3);
                                    },
                                    label: 'Copy'
                                }
                            ]
                        }, 10);
                        
                    } else {
                        frappe.msgprint({
                            title: __('Error'),
                            indicator: 'red',
                            message: r.message.error || __('Failed to create short URL')
                        });
                    }
                }
            });
        }
    });
    
    dialog.show();
    
    // Focus on URL field
    setTimeout(() => {
        dialog.fields_dict.original_url.$input.focus();
    }, 300);
};

// Add to global search
frappe.search.utils.get_recent_pages = (function() {
    const original = frappe.search.utils.get_recent_pages;
    return function() {
        const pages = original.apply(this, arguments);
        
        // Add URL Shortener to quick access
        pages.unshift({
            title: '🔗 URL Shortener',
            route: '/shorten',
            click: function() {
                window.open('/shorten', '_blank');
            }
        });
        
        return pages;
    };
})();
