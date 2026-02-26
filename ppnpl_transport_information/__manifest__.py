{ 
    'name': 'PPNPL_Transport_Information',
    'version': '19.0.1.0.0',
    'summary': 'Customization for Transport Information Module',
    'author': 'Luna',
    'category': 'Custom',
    'depends': ['base','stock','sale','account'],
   'data': [
       'views/transfer_detail.xml',
       'views/sale_invoice.xml',
       'views/account_invoice.xml',    
],
    'installable': True,
    'application': False,
}