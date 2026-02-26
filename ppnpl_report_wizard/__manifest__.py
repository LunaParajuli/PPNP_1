{ 
    'name': 'PPNPL_Report_Wizard',
    'version': '19.0.1.0.0',
    'summary': 'Customization for Wizard  and Salesperson total sales PDF Report',
    'author': 'Luna',
    'category': 'Custom',
    'depends': ['base','sale'],
  'data': [
        'security/ir.model.access.csv',
        'reports/report.xml',            
        'reports/report_template.xml',  
        'views/salesperson_report_wizard_views.xml', 
    ],
    'installable': True,
    'application': False,
}