# Copyright (c) 2025, jfids and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


import frappe
from frappe.model.document import Document

class MachineCluster(Document):
    def validate(self):
        """Validate before save"""
        self.validate_machine_details()
        self.update_total_machines()
    
    def validate_machine_details(self):
        """Check machine details"""
        if not self.machine_details:
            frappe.throw("Please add at least 1 machine to the details")
        
        # Check duplicate machine codes
        machine_codes = [d.machine_code for d in self.machine_details]
        if len(machine_codes) != len(set(machine_codes)):
            frappe.throw("Duplicate machine codes found in details")
    
    def update_total_machines(self):
        """Update total machines count"""
        self.total_machines = len(self.machine_details)
    
    def on_submit(self):
        """Process on submit"""
        self.status = "Active"
        frappe.msgprint(f"Machine Cluster {self.name} submitted successfully")
    
    def on_cancel(self):
        """Process on cancel"""
        self.status = "Inactive"
        
        # Check if there are active sub clusters
        sub_clusters = frappe.get_all("Sub Cluster", 
            filters={"parent_cluster": self.name, "docstatus": 1})
        
        if sub_clusters:
            frappe.throw("Cannot cancel because active sub clusters exist")

# Whitelist methods to call from client
@frappe.whitelist()
def get_sub_cluster_count(parent_cluster):
    """Get sub cluster count"""
    count = frappe.db.count("Sub Cluster", 
        filters={"parent_cluster": parent_cluster})
    return count

@frappe.whitelist()
def create_sub_cluster_quick(parent_cluster, sub_cluster_name):
    """Quick create sub cluster from parent"""
    doc = frappe.get_doc({
        "doctype": "Sub Cluster",
        "parent_cluster": parent_cluster,
        "sub_cluster_name": sub_cluster_name
    })
    doc.insert()
    return doc.name