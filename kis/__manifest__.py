# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'КИС',
    'version' : '1.0',
    'summary': 'КИС',
    'sequence': 10,
    'description': """""",
    'category': 'Manufacturing/Repair',
    'depends': ['base_setup', 'uom'],
    'data': [
        'security/ir.model.access.csv',
        'views/operation_views.xml',
        'views/product_views.xml',
        'views/operation_type_views.xml',
        'views/work_center_views.xml',
        'views/menus.xml',
        'data/servet_action.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web._assets_primary_variables': [
        ],
        'web.assets_backend': [
        ],
        'web.assets_frontend': [
        ],
    },
    'license': 'LGPL-3',
}
