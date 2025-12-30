{
    'name': "Klevia Database Manager",
    'category': "Services/Technical",
    'version': "19.0.1.0.1",
    'installable': True,

    'license': "OPL-1",
    'author': "OneSolutions Klevia SA - Gautier Casabona",
    'website': "https://www.onesolutions.ch",

    'depends': ['mail'],
    'assets': {
        'web.assets_backend': [
            'klevia_dbm_base/static/src/**/*',
        ],
    },

    'data': [
        # Security
        'security/res_groups.xml',
        'security/ir.model.access.csv',

        # Views
        'views/dbm_category.xml',
        'views/dbm_hosting.xml',
        'views/dbm_instance.xml',
        'views/dbm_instance_stage.xml',
        'views/dbm_request.xml',
        'views/dbm_server.xml',
        'views/dbm_tag.xml',
        'views/dbm_version.xml',

        # Reports

        # Data
        'data/dbm_category.xml',
        'data/dbm_hosting.xml',
        'data/dbm_instance_stage.xml',
        'data/dbm_request_stage.xml',
        'data/dbm_version.xml',

        # Menus
        'data/ir_ui_menu.xml',
    ],

    'qweb': [],
}
