# -*- coding: utf-8 -*-
{
    'name': "Hopital Management System",
    'summary': "Hopital Management System to manage Patients",
    'description': "Lab 2 - Odoo",
    'aurthor': 'Hassan Mohamed ELDash',
    'category': "Administration",
    'version': "17.0.0.1.0",
    'depends': ['base'],
    'application': True,
    'installable': True,
    'data': [
        'views/patient.xml',
        'security/ir.model.access.csv',
        'views/base_menus.xml',
        'views/department.xml',
        'views/doctor.xml',
    ]
}