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

template_ids = odoo.env['product.template'].search([('product_variant_count', '>', 1)])
for t_id in template_ids:
    template = odoo.env['product.template'].read(t_id, ['name', 'product_variant_ids'])
    attributes = {}
    products = odoo.env['product.product'].browse(template['product_variant_ids'])
    ok = True
    for product in products:
        for value in product.attribute_value_ids:
            l = attributes.get(value.attribute_id.id, [])
            l.append(value.id)
            attributes[value.attribute_id.id] = l
    for product in products:
        if set(attributes.keys()) - set([v.attribute_id.id for v in product.attribute_value_ids]) != set():
            ok = False
    if not ok:
        print "Problem with attributes for product.template %s, %s" % (template['id'], template['name'])
    else:
        odoo.env['product.template'].write(t_id, {
            'attribute_line_ids': [(0, 0, {
                'attribute_id': id,
                'value_ids': [(6, 0, attributes[id])]
            }) for id in attributes]
        })
