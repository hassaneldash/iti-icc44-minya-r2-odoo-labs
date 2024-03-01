# -*- coding: utf-8 -*-
{
    'name': "Custom Todo App",
    'summary': "Custom Todo App to manage tasks",
    'description': "Lab 1 - Odoo",
    'aurthor': 'Hassan Mohamed ELDash',
    'category': "Productivity",
    'version': "17.0.0.1.0",
    'depends': ['base'],
    'application': True,
    'installable': True,
    'data': [
        'views/ticket.xml',
        'security/ir.model.access.csv',
        'views/base_menus.xml'
    ]
}