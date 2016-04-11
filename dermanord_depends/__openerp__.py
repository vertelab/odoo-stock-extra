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
'name': 'Dermanord Depends',
'version': '0.1',
'summary': '',
'category': '',
'description': """Test for all installed modules for Dermanord""",
'author': 'Vertel AB',
'website': 'http://www.vertel.se',
'depends': [
#odoo-stock-extra
'stock_delivery_slip',
'stock_dermanord',
'stock_picking_reports',
'warning_extended',
'product_dermanord',
#odoo-website-sale-extra
'sale_customer_no',
'sale_delivery_address',
#odoo-account-extra
'account_customer_no',
'account_dermanord',
#odoo-mrp
'mrp_dermanord',
#odoo-website-sale-extra
'product_ean_sequence',
'serveraction_temporary',
],
'data': [],
'installable': True,
}
