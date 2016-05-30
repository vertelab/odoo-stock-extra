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

import re

try:
    import odoorpc
except ImportError:
    raise Warning('odoorpc library missing, pip install odoorpc')

params = odoorpc.session.get('dermanord')
odoo = odoorpc.ODOO(params.get('host'),port=params.get('port'))
odoo.login(params.get('database'),params.get('user'),params.get('passwd'))
line_id = 0
for line in odoo.env['product.attribute.line'].read(odoo.env['product.attribute.line'].search([]), []):
    if line['id'] > line_id:
        line_id = line['id']
template_ids = odoo.env['product.template'].search([('product_variant_count', '>', 1)])
for tmpl_id in template_ids:
    line_id += 1
    template = odoo.env['product.template'].read(tmpl_id, ['name', 'product_variant_ids'])
    products = odoo.env['product.product'].browse(template['product_variant_ids'])
    attr_ids = set()
    value_ids = set()
    for product in products:
        for value in product.attribute_value_ids:
            attr_ids.add(value.attribute_id.id)
            value_ids.add(value.id)
    for attr_id in attr_ids:
        print "INSERT INTO product_attribute_line (product_tmpl_id, attribute_id) VALUES (%s, %s);" % (tmpl_id,attr_id)
    for value_id in value_ids:
        print "INSERT INTO product_attribute_line_product_attribute_value_rel (line_id, val_id) VALUES (%s, %s);" % (line_id, value_id)
