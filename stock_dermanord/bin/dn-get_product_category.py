#!/usr/bin/python
# -*- coding: utf-8 -*-

import odoorpc
params = odoorpc.session.get('test')
#~ params = odoorpc.session.get('dermanord')
odoo = odoorpc.ODOO(params.get('host'),port=params.get('port'))
odoo.login(params.get('database'),params.get('user'),params.get('passwd'))

for product in odoo.env['product.product'].read(odoo.env['product.product'].search([]), ['id', 'name', 'product_tmpl_id']):
    product_template = odoo.env['product.template'].read(odoo.env['product.product'].search([('id', '=', product['product_tmpl_id'][0])]), ['id', 'name', 'categ_id'])
    if len(product_template) > 0:
        print 'Write product: %s\t[category: %s]' %(product['name'], product_template[0]['categ_id'][1])
        odoo.env['product.product'].write(product['id'],{'categ_id': product_template[0]['categ_id'][0]})
