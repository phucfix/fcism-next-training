# File: [app]/[module]/report/machine_cluster_statistics/machine_cluster_statistics.py

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data)
    
    return columns, data, None, chart

def get_columns():
    return [
        {
            "fieldname": "name",
            "label": _("Cluster ID"),
            "fieldtype": "Link",
            "options": "Machine Cluster",
            "width": 120
        },
        {
            "fieldname": "cluster_name",
            "label": _("Cluster Name"),
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "total_machines",
            "label": _("Total Machines"),
            "fieldtype": "Int",
            "width": 100
        },
        {
            "fieldname": "sub_cluster_count",
            "label": _("Sub Cluster Count"),
            "fieldtype": "Int",
            "width": 120
        },
        {
            "fieldname": "workflow_state",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "location",
            "label": _("Location"),
            "fieldtype": "Data",
            "width": 150
        }
    ]

def get_data(filters):
    conditions = ""
    
    if filters.get("workflow_state"):
        conditions += f" AND workflow_state = '{filters.get('workflow_state')}'"
    
    if filters.get("from_date"):
        conditions += f" AND creation >= '{filters.get('from_date')}'"
    
    if filters.get("to_date"):
        conditions += f" AND creation <= '{filters.get('to_date')}'"
    
    data = frappe.db.sql(f"""
        SELECT 
            mc.name,
            mc.cluster_name,
            mc.total_machines,
            (SELECT COUNT(*) FROM `tabSub Cluster` 
             WHERE parent_cluster = mc.name) as sub_cluster_count,
            mc.workflow_state,
            mc.location
        FROM 
            `tabMachine Cluster` mc
        WHERE 
            mc.docstatus < 2
            {conditions}
        ORDER BY 
            mc.creation DESC
    """, as_dict=1)
    
    return data

def get_chart_data(data):
    labels = []
    values = []
    
    for row in data:
        labels.append(row.get('cluster_name'))
        values.append(row.get('total_machines'))
    
    return {
        'data': {
            'labels': labels[:10],  # Top 10
            'datasets': [
                {
                    'name': 'Machine Count',
                    'values': values[:10]
                }
            ]
        },
        'type': 'bar',
        'colors': ['#5e64ff']
    }