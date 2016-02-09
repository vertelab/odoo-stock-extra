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

local_server = 'localhost'
local_user = 'anders.wallenquist@vertel.se'
local_passwd = 'odoo8dermanord'
local_database = 'stable_migrated12okt15'
local_port = 9069



# Prepare the connection to the server
#odoo = odoorpc.ODOO(local_server, protocol='xmlrpc', port=local_port)
odoo = odoorpc.ODOO(local_server, port=local_port)

# Check available databases
print(odoo.db.list())

# Login (the object returned is a browsable record)
odoo.login(local_database,local_user, local_passwd)
user = odoo.env.user
print(user.name)            # name of the user connected
print(user.company_id.name) # the name of its company

#for template in oerp.get('product.template').browse(oerp.get('product.template').search([('','','')])):
#for template in oerp.get('product.template').browse(oerp.get('product.template').search([])):
for template in odoo.env['product.template'].search([])[:50]:
    print(template)
    record = odoo.env['product.template'].read(template,['name'])
    #products = [line.product_id.name for line in order.order_line]
    #print(products)

# Update data through a browsable record
#user.name = "Brian Jones"
#oerp.write_record(user)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
