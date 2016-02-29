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
import re

local_server = 'localhost'
local_user = 'anders.wallenquist@vertel.se'
local_passwd = 'foobar'
local_database = 'dermanord1'
local_port = 8069



# Prepare the connection to the server
#odoo = odoorpc.ODOO(local_server, protocol='xmlrpc', port=local_port)
odoo = odoorpc.ODOO(local_server, port=local_port)

# Check available databases
#~ print(odoo.db.list())

# Login (the object returned is a browsable record)
odoo.login(local_database, local_user, local_passwd)
#user = odoo.env.user
#print(user.name)            # name of the user connected
#print(user.company_id.name) # the name of its company

#for template in oerp.get('product.template').browse(oerp.get('product.template').search([('','','')])):
#for template in oerp.get('product.template').browse(oerp.get('product.template').search([])):

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

#Fetch the id of a volume attribute value. Create a new record if none exists.
def get_attr_value_id(name):
    val_name = ''
    for c in name:
        if c.isdigit():
            val_name += c
    val_name += ' ml'
    for attr_value in attr_values:
        if attr_value['name'] == val_name:
            return attr_value['id']
    id = odoo.env['product.attribute.value'].create({'name': val_name, 'attribute_id': volume_id})
    attr_values.append(odoo.env['product.attribute.value'].read(id, ['name']))
    return id

handled_products = []

for id in odoo.env['product.template'].search([('name', 'like', ',')])[:20]:
    record = odoo.env['product.template'].read(id,['name'])
    i = record['name'].rfind(',')
    name = record['name'][:i]
    variant = record['name'][i + 2:]
    attr_lines = []
    if not name in handled_products and is_volume_variant(variant):
        for prod_id in odoo.env['product.product'].search([('name', 'like', name)]):
            r = odoo.env['product.product'].read(prod_id,['name', 'product_tmpl_id', 'attribute_value_ids'])
            v = r['name'][r['name'].rfind(',') + 2:]
            if (is_volume_variant(v)):
                v_id = get_attr_value_id(v)
                attr_lines.append(v_id)
                r['name'] = r['name'][:r['name'].rfind(',')]
                r['product_tmpl_id'] = id
                r['attribute_value_ids'].append(v_id)
                odoo.env['product.product'].write(r['id'], r)
                #TODO: Remove template
        handled_products.append(name)
        odoo.env['product.template'].write(id, {'name': name})
        print name
            
        
        #product.attribute.line: attribute_id, value_ids, product_tmpl_id
        #~ variants.append(record['name'])
    #~ else:
        #~ products[name] = [variant]
#~ for key in products:
    #~ print('Product name: |%s|\nVariants: |%s|\n' % (key, products[key]))
    #products = [line.product_id.name for line in order.order_line]
    #print(products)
    
#~ import codecs
#~ import sys 
#~ UTF8Writer = codecs.getwriter('utf8')
#~ sys.stdout = UTF8Writer(sys.stdout)
#~ for v in variants:
    #~ print(v)
# Update data through a browsable record
#user.name = "Brian Jones"
#oerp.write_record(user)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
