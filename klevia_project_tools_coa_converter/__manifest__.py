{
    'name': "Klevia Project Tools - CoA Converter",
    'category': "Services/Project",
    'version': "19.0.1.0.0",
    'installable': True,

    'license': "AGPL-3",
    'author': "OneSolutions - Gautier Casabona",
    'website': "https://www.onesolutions.ch",

    'depends': ['klevia_project_tools'],
    'external_dependencies': {
        'python': ['pandas']
    },
    'auto_install': True,
    "assets": {
        "web.assets_backend": [],
    },

    'data': [
        # Security
        'security/ir.model.access.csv',

        # Wizards
        'wizards/project_tools_wizard.xml',
        'wizards/project_tools_coa_converter_wizard.xml',


        # Views
        # 'views/sale_order.xml',

        # Data
        'data/ir_ui_menu.xml',
    ],

    'qweb': [],
}
