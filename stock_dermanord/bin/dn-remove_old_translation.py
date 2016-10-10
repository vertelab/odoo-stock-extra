#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2016- Vertel AB (<http://vertel.se>).
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

import odoorpc
params = odoorpc.session.get('dermanord')
odoo = odoorpc.ODOO(params.get('host'),port=params.get('port'))
odoo.login(params.get('database'),params.get('user'),params.get('passwd'))

for t in odoo.env['ir.translation'].read(odoo.env['ir.translation'].search([('name', 'ilike', 'product.product')]),['id','name']):
    if t['name'].find(',x_ingredients') != -1 or t['name'].find(',x_use_desc') != -1 or t['name'].find(',x_public_desc') != -1 or t['name'].find(',x_reseller_desc') != -1 or t['name'].find(',x_shelf_label_desc') != -1:
        odoo.env['ir.translation'].unlink([t['id']])
        print "%s: translation removed" % t['name']

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
