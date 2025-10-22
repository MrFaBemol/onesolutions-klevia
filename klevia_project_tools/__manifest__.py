{
    'name': "Klevia Project Tools",
    'category': "Services/Project",
    'version': "18.0.1.0.0",
    'installable': True,

    'license': "AGPL-3",
    'author': "OneSolutions - Gautier Casabona",
    'website': "https://www.onesolutions.ch",

    'depends': ['project'],
    # 'external_dependencies': {
    #     'python': ['pandas']
    # },
    "assets": {
        "web.assets_backend": [],
    },

    'data': [
        # Security
        'security/res_groups.xml',
        'security/ir.model.access.csv',

        # Wizards
        'wizards/project_tools_wizard.xml',
        # 'wizards/project_tools_coa_converter_wizard.xml',


        # Views
        # 'views/sale_order.xml',

        # Data
        'data/ir_ui_menu.xml',
    ],

    'qweb': [],
}
