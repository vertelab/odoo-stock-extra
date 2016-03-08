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
# ~/.odoorpc
#[dermanord]
#host = localhost
#protocol = xmlrpc
#user = admin
#timeout = 120
#database = <database>
#passwd = <password>
#type = ODOO
#port = 8069

#pip install odoorpc
import re
import odoorpc
params = odoorpc.session.get('dermanord')
odoo = odoorpc.ODOO(params.get('host'),port=params.get('port'))

# Check available databases
#print(odoo.db.list())

# Login (the object returned is a browsable record)
#odoo.login(local_database,local_user, local_passwd)
odoo.login(params.get('database'),params.get('user'),params.get('passwd'))


#Fetch id of Volume attribute. Create the attribute if it doesn't exist.
volume_id = odoo.env['product.attribute'].search([('name', '=', 'Volume')])
if len(volume_id) < 1:
    volume_id = odoo.env['product.attribute'].create({'name': 'Volume'})
else:
    volume_id = volume_id[0]

print 'Volume attribute id: %s' % volume_id

#Fetch all Volume attribute values
attr_values = []
for id in odoo.env['product.attribute.value'].search([('attribute_id', '=', volume_id)]):
    attr_values.append(odoo.env['product.attribute.value'].read(id, ['name']))

print 'Volume attribute values: %s' % attr_values

#Check if the string describes a volume attribute value
def is_volume_variant(variant):
    pattern = re.compile('\\ *[0-9]+\\ *ml')
    return pattern.match(variant)

# Get attr value, if missing create both product.attribute and product.attribute.value. Change product.attribute afterwards.
def get_attr_value_id(name):
    value_id = odoo.env['product.attribute.value'].search([('name','=',name)])
    if not value_id:
        #attribute_id = odoo.env['product.attribute'].create({'name': name, })
        #value_id = odoo.env['product.attribute.value'].create({'name': name, 'attribute_id': attribute_id})
        print "Created new attribute %s" % name
    return value_id


handled_templates = []
#for template_id in odoo.env['product.template'].search([('name', 'like', '%,%')])[:20]:
for template_id in odoo.env['product.template'].search([('name', 'like', '%,%')]):
    record = odoo.env['product.template'].read(template_id,['name'])
    attr_name = [x.strip() for x in record['name'].split(',')]
    template_name = attr_name[0]  # Template name are the first sentence before coma
  
    if not template_name in handled_templates:
        for prod_id in odoo.env['product.product'].search([('name', 'like', '%s%%' % template_name)]):
            r = odoo.env['product.product'].read(prod_id,['name', 'product_tmpl_id', 'attribute_value_ids'])
            for attr in [x.strip() for x in r['name'].split(',')]:
                r['name'] = template_name
                r['product_tmpl_id'] = template_id
                r['attribute_value_ids'].append(get_attr_value_id(attr))
                #odoo.env['product.product'].write(r['id'], r)
        handled_templates.append(template_name)
    #odoo.env['product.template'].write(template_id, {'name': template_name})
    print "Template %s -> %s" % (record['name'],template_name)
            

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
