# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#             <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Project progress measurement',
    'version': '8.0.1.0.0',
    'author': 'Eficent, '
              'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': ['project', 'progress_measurement', 'project_wbs'],
    'data': [
        'project_progress_measurement_view.xml',
        'wizard/progress_measurements_entry_view.xml',
        'project_project_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [

    ],
    'test': [
    ],
    'installable': False,
    'active': False,
    'certificate': '',
    'application': True,
}
