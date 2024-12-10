{
    'name': "Klevia Database Manager",
    'category': "Services/Technical",
    'version': "18.0.1.0.0",
    'installable': True,

    'license': "AGPL-3",
    'author': "OneSolutions Klevia SA - Gautier Casabona",
    'website': "https://www.onesolutions.ch",

    'depends': ['mail'],
    'assets': {
        'web.assets_backend': [
            'klevia_database_manager/static/src/**/*',
        ],
    },

    'data': [
        # Security
        'security/res_groups.xml',
        'security/ir.model.access.csv',

        # Views
        'views/dbm_category.xml',
        'views/dbm_server.xml',
        'views/dbm_database.xml',

        # Reports

        # Menus
        'data/ir_ui_menu.xml',
    ],

    'qweb': [],
}
