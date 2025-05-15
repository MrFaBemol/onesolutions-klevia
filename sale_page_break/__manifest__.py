{
    'name': 'Page break',
    'category': "Sales",
    'version': "18.0.1.0.3",
    'license': "OPL-1",
    'author': "OneSolutions - Najoua Chaouch",
    'depends': [
        'sale','account'
    ],
    'assets': {
        'web.assets_backend': [
            'sale_page_break/static/src/js/custom_sale_order_line_renderer.js'

        ],
    },
    'data': [
        'views/sale_order.xml',
        'report/sale_order_templates.xml',
    ],
    'installable': True,
    'application': True,

}

