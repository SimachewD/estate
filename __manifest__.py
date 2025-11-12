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
    'depends': ['base'],
    'data': [
        'security/res_group.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menu.xml',
    ],
    'demo': [
        'data/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
