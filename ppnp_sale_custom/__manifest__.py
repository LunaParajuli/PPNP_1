{ 
    'name': 'PPNP_Sale_Custom',
    'version': '19.0.1.0',
    'summary': 'Customization for Sale Module',
    'author': 'ABC',
    'category': 'Custom',
    'depends': ['base','sale','report_xlsx'],
    'data': [  
        'security/security.xml',
        'security/ir.model.access.csv',
        'reports/report.xml',
        'reports/report_template.xml',
         'views/sale_menu_views.xml',
    ],
    'installable': True,
    'application': False,
}