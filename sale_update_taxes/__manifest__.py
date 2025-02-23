{
    'name': 'Update taxes on sale order lines',
    'category': "Sales",
    'version': "18.0.1.0.2",
    'license': "OPL-1",
    'author': "OneSolutions - Najoua Chaouch",
    'depends': [
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'wizard/update_line_taxes_wizard.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
