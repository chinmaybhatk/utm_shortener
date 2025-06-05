frappe.ui.form.on('UTM Campaign', {
    refresh: function(frm) {
        // Add custom buttons
        if (frm.doc.full_url) {
            frm.add_custom_button(__('Copy Full URL'), function() {
                copy_to_clipboard(frm.doc.full_url, 'Full URL');
            });
        }
        
        if (frm.doc.base_url) {
            frm.add_custom_button(__('Regenerate URL'), function() {
                regenerate_utm_url(frm);
            });
        }
        
        // Show URL preview
        if (frm.doc.full_url) {
            frm.set_df_property('full_url', 'description', 
                `<div class="alert alert-info">
                    <strong>Full URL:</strong><br>
                    <code style="word-break: break-all;">${frm.doc.full_url}</code>
                </div>`
            );
        }
    },
    
    base_url: function(frm) {
        // Auto-generate full URL when base URL is changed
        if (frm.doc.base_url) {
            generate_full_url(frm);
        }
    },
    
    utm_source: function(frm) {
        if (frm.doc.base_url) {
            generate_full_url(frm);
        }
    },
    
    utm_medium: function(frm) {
        if (frm.doc.base_url) {
            generate_full_url(frm);
        }
    },
    
    utm_campaign: function(frm) {
        if (frm.doc.base_url) {
            generate_full_url(frm);
        }
    },
    
    utm_term: function(frm) {
        if (frm.doc.base_url) {
            generate_full_url(frm);
        }
    },
    
    utm_content: function(frm) {
        if (frm.doc.base_url) {
            generate_full_url(frm);
        }
    },
    
    copy_url_button: function(frm) {
        if (frm.doc.full_url) {
            copy_to_clipboard(frm.doc.full_url, 'Full URL');
        }
    }
});

function generate_full_url(frm) {
    // Generate URL on client side for immediate feedback
    if (!frm.doc.base_url) {
        frm.set_value('full_url', '');
        return;
    }
    
    let params = [];
    if (frm.doc.utm_source) params.push(`utm_source=${encodeURIComponent(frm.doc.utm_source)}`);
    if (frm.doc.utm_medium) params.push(`utm_medium=${encodeURIComponent(frm.doc.utm_medium)}`);
    if (frm.doc.utm_campaign) params.push(`utm_campaign=${encodeURIComponent(frm.doc.utm_campaign)}`);
    if (frm.doc.utm_term) params.push(`utm_term=${encodeURIComponent(frm.doc.utm_term)}`);
    if (frm.doc.utm_content) params.push(`utm_content=${encodeURIComponent(frm.doc.utm_content)}`);
    
    if (params.length > 0) {
        const separator = frm.doc.base_url.includes('?') ? '&' : '?';
        const full_url = `${frm.doc.base_url}${separator}${params.join('&')}`;
        frm.set_value('full_url', full_url);
    } else {
        frm.set_value('full_url', frm.doc.base_url);
    }
}

function regenerate_utm_url(frm) {
    frappe.call({
        method: 'utm_shortener.utm_shortener.doctype.utm_campaign.utm_campaign.update_base_url',
        args: {
            campaign_name: frm.doc.name,
            base_url: frm.doc.base_url
        },
        callback: function(r) {
            if (r.message) {
                frm.set_value('full_url', r.message);
                frappe.show_alert({
                    message: 'URL regenerated successfully',
                    indicator: 'green'
                });
            }
        }
    });
}

function copy_to_clipboard(text, label) {
    if (navigator.clipboard && window.isSecureContext) {
        // Use modern clipboard API
        navigator.clipboard.writeText(text).then(function() {
            frappe.show_alert({
                message: `${label} copied to clipboard!`,
                indicator: 'green'
            });
        }).catch(function(err) {
            console.error('Failed to copy: ', err);
            fallback_copy_to_clipboard(text, label);
        });
    } else {
        // Fallback for older browsers
        fallback_copy_to_clipboard(text, label);
    }
}

function fallback_copy_to_clipboard(text, label) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.left = "-999999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        frappe.show_alert({
            message: `${label} copied to clipboard!`,
            indicator: 'green'
        });
    } catch (err) {
        console.error('Failed to copy: ', err);
        frappe.show_alert({
            message: 'Failed to copy to clipboard',
            indicator: 'red'
        });
    }
    
    document.body.removeChild(textArea);
}