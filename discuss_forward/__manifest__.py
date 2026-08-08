# -*- coding: utf-8 -*-

{
    'name': 'Discuss Message Forward',
    'version': '18.0.1.0.0',
    'category': 'Discuss',
    'summary': 'Forward messages in Discuss',
    'author': 'Erfan Meraati',
    'website': 'https://meraati.net',
    'license': 'OPL-1',

    'depends': [
        'mail',
    ],

    'data': [
        'security/ir.model.access.csv',
    ],

    'assets': {
        'web.assets_backend': [
            'discuss_forward/static/src/js/**/*.js',
            'discuss_forward/static/src/xml/**/*.xml',
            'discuss_forward/static/src/scss/**/*.scss',
        ],
    },

    'images': [
        'static/description/cover.png',
        'static/description/sc1.png',
        'static/description/sc2.png',
        'static/description/sc3.png',
    ],
    'price': 19.99,
    'currency': 'EUR',

    'support': 'erfan@meraati.net',

    'installable': True,
    'application': False,
    'auto_install': False,
}

