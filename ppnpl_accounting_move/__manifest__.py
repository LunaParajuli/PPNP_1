{ 
    'name': 'PPNPL_Account_Custom',
    'version': '19.0.1.0.0',
    'summary': 'Customization for Accounting module ',
    'description':'Not allowed to edit or change already existed contact by normal users but certain groups are allowed with warnings....',
    'author': 'Luna',
    'category': 'Custom',
    'depends': ['base','account','contacts'],
  'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}