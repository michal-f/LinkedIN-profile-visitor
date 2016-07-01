# -*- coding: utf-8 -*-

CONSTANCE_ADDITIONAL_FIELDS = {
    'yes_no_null_select': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': (("-----", None), ("yes", "Yes"), ("no", "No"))
    }],
    'yes_no_select': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': (("yes", "Yes"), ("no", "No"))
    }],
}

CONSTANCE_CONFIG = {
    'MIN_INTERVAL': (30, 'Minimum time interval between requests (in seconds)'),
    'MAX_INTERVAL': (180, 'Maximum time interval between requests (in seconds)'),
    'DEBUG_CONSOLE_LOGS': ('yes', 'select yes or no', 'yes_no_select'),
}