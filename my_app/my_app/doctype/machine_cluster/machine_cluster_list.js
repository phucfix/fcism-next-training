// File: [app]/[module]/doctype/machine_cluster/machine_cluster_list.js

frappe.listview_settings['Machine Cluster'] = {
    // Add color indicators
    get_indicator: function(doc) {
        if (doc.workflow_state === "Approved") {
            return [__("Approved"), "green", "workflow_state,=,Approved"];
        } else if (doc.workflow_state === "Pending Approval") {
            return [__("Pending"), "orange", "workflow_state,=,Pending Approval"];
        } else if (doc.workflow_state === "Rejected") {
            return [__("Rejected"), "red", "workflow_state,=,Rejected"];
        } else {
            return [__("Draft"), "blue", "workflow_state,=,Draft"];
        }
    },
    
    // Custom buttons on list view
    onload: function(listview) {
        // Create new button
        listview.page.add_inner_button(__('Create New Cluster'), function() {
            frappe.new_doc('Machine Cluster');
        });
        
        // Bulk action button
        listview.page.add_action_item(__('Export to Excel'), function() {
            frappe.call({
                method: 'frappe.desk.reportview.export_query',
                args: {
                    doctype: 'Machine Cluster',
                    file_format_type: 'Excel'
                }
            });
        });
    },
    
    // Format display
    formatters: {
        total_machines: function(value) {
            return `<span class="badge badge-primary">${value} machines</span>`;
        }
    },
    
    // Refresh when needed
    refresh: function(listview) {
        // Custom logic on refresh
    }
};