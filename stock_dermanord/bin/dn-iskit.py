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

try:
    import odoorpc
except ImportError:
    raise Warning('odoorpc library missing, pip install odoorpc')

params = odoorpc.session.get('dermanord')
odoo = odoorpc.ODOO(params.get('host'),port=params.get('port'))
odoo.login(params.get('database'),params.get('user'),params.get('passwd'))

#Find all products with x_iskit == True
ids = odoo.env['product.product'].search([('x_iskit','=',True)])
print "Found %s products" % len(ids)
for id in ids:
    # sök template via tmpl-fältet
    print "id %s" % id
    product = odoo.env['product.product'].read(id,['product_tmpl_id'])
    print "Updating product.template %s " % product['product_tmpl_id'][0]
    odoo.env['product.template'].write(product['product_tmpl_id'][0], {'iskit': True})
