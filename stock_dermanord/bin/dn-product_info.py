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

#pip install odoorpc
import odoorpc
params = odoorpc.session.get('dermanord_oden')
odoo = odoorpc.ODOO(params.get('host'),port=params.get('port'))
odoo.login(params.get('database'),params.get('user'),params.get('passwd'))

def update_user(product_id, original, dest, login):
    user_id = odoo.env['res.users'].search([('login', '=', login)])
    if len(user_id) == 0:
        user_id = odoo.env['res.users'].create({'name': 'Missing User %s' % login, 'login': login})
    else:
        user_id = user_id[0]
    odoo.env['product.product'].write(product_id, {dest: user_id})
    print 'updated product %s: %s' % (product_id, dest)

for p in odoo.env['product.product'].search([]):
    product = odoo.env['product.product'].read(p, ['ingredients_changed_by', 'public_desc_changed_by', 'reseller_desc_changed_by', 'shelf_label_desc_changed_by', 'use_desc_changed_by'])
    if product.get('ingredients_changed_by'):
        update_user(p, 'ingredients_changed_by', 'ingredients_changed_by_uid', product['ingredients_changed_by'])
    if product.get('public_desc_changed_by'):
        update_user(p, 'public_desc_changed_by', 'public_desc_changed_by_uid', product['public_desc_changed_by'])
    if product.get('reseller_desc_changed_by'):
        update_user(p, 'reseller_desc_changed_by', 'reseller_desc_changed_by_uid', product['reseller_desc_changed_by'])
    if product.get('shelf_label_desc_changed_by'):
        update_user(p, 'shelf_label_desc_changed_by', 'shelf_label_desc_changed_by_uid', product['shelf_label_desc_changed_by'])
    if product.get('use_desc_changed_by'):
        update_user(p, 'use_desc_changed_by', 'use_desc_changed_by_uid', product['use_desc_changed_by'])

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
