# -*- coding: utf-8 -*-
#__author__ = 'Koufana'
{
    'name': 'Appacheur Fleet Management Project',
    'version': '1.0',
    'author': 'Koufana Crepin Sosthene, APPACHEUR',
    'sequence': '10',
    'category': 'Managing vehicles',
    'website': 'www.appacheur.org',
    'summary': 'Appacheur, Vehicles fleet, project, analytic accounting',
    'description': """
    """,
    'depends': ['base', 'fleet_appacheur'],
    'qweb': ['static/src/xml/*.xml'],
    'data': [
        'fleet_appacheur_project_view.xml',
    ],
    'instalable': 'true',
}
