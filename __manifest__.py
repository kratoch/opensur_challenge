{
    'name': 'OpenSur Challenge',
    'version': '17.0.1.0.0',
    'category': 'Account',
    'summary': '',
    'author': 'Kratochvil Claudio',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'security/account_security.xml',
        'views/account_move_views.xml',
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': True,
}
