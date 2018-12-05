# -*- coding: utf-8 -*-
{
    'name': "Odoo Academy",

    'summary': "Create a course and add it session with a limit of attendees to invite a group of people to get it.",

    'description': "Create a course and add it session with a limit of attendees to invite a group of people to get it.",

    'author': "Prodigia",
    'website': "http://www.prodigia.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Academy',
    'version': '0.1.2',


    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'l10n_mx_edi', 'mail'],

    # always loaded
    'data': [

        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'views/test.xml',
        'views/partner.xml',
        'reports.xml',
        'views/quotation.xml',
        'views/email_template.xml',
        'reports.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ]
}
