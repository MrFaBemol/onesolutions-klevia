{
    'name': "NextFlow",
    'category': "Services/Accounting",
    'version': "18.0.1.0.0",
    'installable': True,
    'application': True,

    'license': "OPL-1",
    'author': "OneSolutions Klevia SA - Gautier Casabona",
    'website': "https://www.onesolutions.ch",

    'depends': ['mail'],
    'assets': {
        'web.assets_backend': [
            'nextflow/static/src/**/*',
        ],
    },

    'data': [
        # Security
        'security/res_groups.xml',
        'security/ir.model.access.csv',

        # Views
        'views/nextflow_mandate.xml',
        'views/nextflow_mandate_tag.xml',
        'views/res_config_settings.xml',

        # Reports

        # Menus
        'data/ir_ui_menu.xml',
    ],

    'qweb': [],
}
