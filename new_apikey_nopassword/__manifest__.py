{
    'name': 'New API Key No Password',
    'version': '1.0',
    'summary': 'Remove password check for new API keys',
    'description': 'This module removes the password check when a user generates a new API key.',
    'author': 'Ernad Husremović hernad@bring.out.ba',
    'company': 'bring.out doo Sarajevo',
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