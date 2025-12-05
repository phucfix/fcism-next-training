// Copyright (c) 2025, jfids and contributors
// For license information, please see license.txt

frappe.ui.form.on('Machine Cluster', {
    refresh: function(frm) {
        // Show buttons only when saved and submitted
        if (!frm.is_new() && frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Create Sub Cluster'), function() {
                frappe.new_doc('Sub Cluster', {
                    parent_cluster: frm.doc.name
                });
            }, __('Create'));
            
            // Button to view sub clusters
            frm.add_custom_button(__('View Sub Clusters'), function() {
                frappe.set_route('List', 'Sub Cluster', {
                    parent_cluster: frm.doc.name
                });
            }, __('View'));
        }
        
        // Calculate total machines from details
        if (frm.doc.machine_details) {
            frm.set_value('total_machines', frm.doc.machine_details.length);
        }
    },
    
    // Validate before submit
    validate: function(frm) {
        if (!frm.doc.machine_details || frm.doc.machine_details.length === 0) {
            frappe.msgprint(__('Please add at least 1 machine to the details'));
            frappe.validated = false;
        }
    },
    
    // Auto update total machines
    machine_details_add: function(frm) {
        frm.set_value('total_machines', frm.doc.machine_details.length);
    },
    
    machine_details_remove: function(frm) {
        frm.set_value('total_machines', frm.doc.machine_details.length);
    }
});

// Child table validation
frappe.ui.form.on('Machine Cluster Detail', {
    machine_code: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        // Check duplicate machine code
        let duplicate = frm.doc.machine_details.find(d => 
            d.name !== cdn && d.machine_code === row.machine_code
        );
        
        if (duplicate) {
            frappe.msgprint(__('Machine code already exists!'));
            frappe.model.set_value(cdt, cdn, 'machine_code', '');
        }
    }
});
