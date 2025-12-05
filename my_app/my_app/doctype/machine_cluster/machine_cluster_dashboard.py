# File: [app]/[module]/doctype/machine_cluster/machine_cluster_dashboard.py

from frappe import _

def get_data():
    return {
        'fieldname': 'parent_cluster',
        'non_standard_fieldnames': {},
        'transactions': [
            {
                'label': _('Sub Clusters'),
                'items': ['Sub Cluster']
            }
        ],
        'reports': [
            {
                'label': _('Reports'),
                'items': ['Machine Cluster Statistics']
            }
        ]
    }

# Create Chart
def get_chart_data():
    """Chart statistics by status"""
    import frappe
    from frappe.utils.dashboard import get_chart_data
    
    return {
        'data': {
            'labels': ['Draft', 'Pending', 'Approved', 'Rejected'],
            'datasets': [
                {
                    'name': 'Count',
                    'values': [
                        frappe.db.count('Machine Cluster', {'workflow_state': 'Draft'}),
                        frappe.db.count('Machine Cluster', {'workflow_state': 'Pending Approval'}),
                        frappe.db.count('Machine Cluster', {'workflow_state': 'Approved'}),
                        frappe.db.count('Machine Cluster', {'workflow_state': 'Rejected'})
                    ]
                }
            ]
        },
        'type': 'bar',
        'colors': ['#5e64ff', '#ffa00a', '#28a745', '#dc3545']
    }