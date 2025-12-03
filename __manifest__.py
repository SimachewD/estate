{
    'name': 'Real Estate Management',
    'version': '1.0',
    'summary': 'Manage real estate properties, their details and sales',
    'description': """
        Real Estate Management Module
        - Track properties
        - Record details such as price, bedrooms, garden, garage, etc.
        - Plan availability and sales
        """,
    'author': 'odoo-16-training',
    'category': 'Real Estate',
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/res_group.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_accounting_views.xml',
        'views/res_users_views.xml',
        'views/estate_menu.xml',
    ],
    'demo': [
        'data/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'estate/static/src/css/custom.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
