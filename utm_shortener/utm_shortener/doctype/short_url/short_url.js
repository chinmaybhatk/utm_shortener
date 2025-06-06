frappe.ui.form.on('Short URL', {
    refresh: function(frm) {
        // Add custom buttons
        if (frm.doc.short_url) {
            frm.add_custom_button(__('Copy Short URL'), function() {
                copy_to_clipboard(frm.doc.short_url);
            });
            
            // Show the short URL prominently
            frm.set_df_property('short_url', 'description', 
                `<div class="alert alert-success">
                    <strong>Short URL:</strong><br>
                    <code style="font-size: 14px;">${frm.doc.short_url}</code>
                </div>`
            );
        }
        
        // If new document, show that short code will be auto-generated
        if (frm.is_new()) {
            frm.set_df_property('short_code', 'description', 
                '<span class="text-muted">Will be auto-generated on save</span>'
            );
        }
        
        // Make short_code visible but read-only
        frm.set_df_property('short_code', 'hidden', 0);
        frm.set_df_property('short_code', 'read_only', 1);
        
        // Update generated UTM URL when campaign is selected
        if (frm.doc.utm_campaign && frm.doc.generated_utm_url) {
            frm.set_df_property('generated_utm_url', 'description', 
                `<div class="alert alert-info">
                    <strong>URL with UTM Parameters:</strong><br>
                    <code style="word-break: break-all;">${frm.doc.generated_utm_url}</code>
                </div>`
            );
        }
    },
    
    before_save: function(frm) {
        // For new documents, temporarily set a placeholder short code
        // The actual code will be generated on the server side
        if (frm.is_new() && !frm.doc.short_code) {
            frm.doc.short_code = "TEMP-" + Math.random().toString(36).substring(7);
        }
    },
    
    utm_campaign: function(frm) {
        // When UTM campaign is selected, show preview of what URL will be generated
        if (frm.doc.utm_campaign && frm.doc.original_url) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'UTM Campaign',
                    name: frm.doc.utm_campaign
                },
                callback: function(r) {
                    if (r.message) {
                        let campaign = r.message;
                        let preview_url = build_utm_url(frm.doc.original_url, campaign);
                        frm.set_df_property('generated_utm_url', 'description', 
                            `<div class="alert alert-info">
                                <strong>Preview - URL with UTM Parameters:</strong><br>
                                <code style="word-break: break-all;">${preview_url}</code>
                            </div>`
                        );
                    }
                }
            });
        }
    },
    
    custom_alias: function(frm) {
        // Validate custom alias format
        if (frm.doc.custom_alias) {
            let alias = frm.doc.custom_alias;
            if (!/^[a-zA-Z0-9_-]+$/.test(alias)) {
                frappe.msgprint(__('Custom alias can only contain letters, numbers, hyphens, and underscores'));
                frm.set_value('custom_alias', '');
            } else if (alias.length < 3 || alias.length > 20) {
                frappe.msgprint(__('Custom alias must be between 3 and 20 characters'));
                frm.set_value('custom_alias', '');
            }
        }
    }
});

function build_utm_url(base_url, campaign) {
    let params = [];
    if (campaign.utm_source) params.push(`utm_source=${encodeURIComponent(campaign.utm_source)}`);
    if (campaign.utm_medium) params.push(`utm_medium=${encodeURIComponent(campaign.utm_medium)}`);
    if (campaign.utm_campaign) params.push(`utm_campaign=${encodeURIComponent(campaign.utm_campaign)}`);
    if (campaign.utm_term) params.push(`utm_term=${encodeURIComponent(campaign.utm_term)}`);
    if (campaign.utm_content) params.push(`utm_content=${encodeURIComponent(campaign.utm_content)}`);
    
    if (params.length > 0) {
        const separator = base_url.includes('?') ? '&' : '?';
        return `${base_url}${separator}${params.join('&')}`;
    }
    return base_url;
}

function copy_to_clipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function() {
            frappe.show_alert({
                message: 'Short URL copied to clipboard!',
                indicator: 'green'
            });
        }).catch(function(err) {
            fallback_copy_to_clipboard(text);
        });
    } else {
        fallback_copy_to_clipboard(text);
    }
}

function fallback_copy_to_clipboard(text) {
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
            message: 'Short URL copied to clipboard!',
            indicator: 'green'
        });
    } catch (err) {
        frappe.msgprint('Failed to copy to clipboard. Please copy manually.');
    }
    
    document.body.removeChild(textArea);
}