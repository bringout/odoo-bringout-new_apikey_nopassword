# Copyright 2026 bring.out doo Sarajevo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'New API Key No Password',
    'version': '16.0.1.0.0',
    'summary': 'Remove password check for new API keys',
    'description': 'This module removes the password check when a user generates a new API key.',
    'author': 'bring.out doo Sarajevo',
    'website': 'https://bring.out.ba',
    'license': 'AGPL-3',
    'depends': ['base'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'new_apikey_nopassword/static/src/js/new_apikey_service.js',
        ],
    },
    'installable': True,
    'application': False,
}