# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'sale_update_taxes',
    'depends': [
        'base','web', 'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/update_line_taxes.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'sale_update_taxes/static/src/js/cog_menu.js',
            'sale_update_taxes/static/src/xml/cog_menu.xml',
        ],
    },
    'demo': [

    ],
    'css': [],
    'installable': True,
    'application': True,
    'auto_install': False
}

