```python
# -*- coding: utf-8 -*-

{
    'name': 'Discuss Message Forward',
    'version': '19.0.1.0.0',
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
            'discuss_forward_19/static/src/js/**/*.js',
            'discuss_forward_19/static/src/xml/**/*.xml',
            'discuss_forward_19/static/src/scss/**/*.scss',
        ],
    },

    'price': 49.99,
    'currency': 'EUR',

    'support': 'erfan@meraati.net',

    'installable': True,
    'application': False,
    'auto_install': False,
}
```
