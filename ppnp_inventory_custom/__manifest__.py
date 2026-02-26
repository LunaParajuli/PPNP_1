{ 
    'name': 'PPNP_Inventory_Custom',
    'version': '19.0.1.0',
    'summary': 'Customization for Inventory Module',
    'author': 'Luna',
    'category': 'Custom',
    'depends': ['base','stock'],
   'data': [
    'security/ir.model.access.csv',
    'security/security.xml',
    'views/inventory_detail.xml',
    'views/custom_menu.xml',
],
    'installable': True,
    'application': False,
}