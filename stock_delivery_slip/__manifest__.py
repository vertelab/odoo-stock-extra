# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
'name': 'stock_delivery_slip',
'version': '14.1.0.0.1',
'summary': '',
'category': 'stock',
'description': """Extended stock picking report with warehouse place.

New field quant_source_location (reserved_quant_ids stock.quant) to be used
in picking reports and views


Report financed by Dermanord-Svensk Hudvård AB""",
'author': 'Vertel AB',
    'license': 'AGPL-3',
'website': 'http://www.vertel.se',
'depends': ['stock'], #'stock_dermanord', 'stock_multiple_picker'],
'data': [ 
    'data/stock_delivery_slip_report.xml'
    ],
'installable': True,
}
