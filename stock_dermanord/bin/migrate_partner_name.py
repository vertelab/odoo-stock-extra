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

#~ local_server = 'localhost'
#~ local_user = 'anders.wallenquist@vertel.se'
#~ local_passwd = ''
#~ local_database = 'dev_migrated12okt15'
#~ local_port = 9070

local_server = 'localhost'
local_user = 'admin'
local_passwd = 'admin'
local_database = 'dermanord'
local_port = 8069



# Prepare the connection to the server
#odoo = odoorpc.ODOO(local_server, protocol='xmlrpc', port=local_port)
odoo = odoorpc.ODOO(local_server, port=local_port)

# Check available databases
print(odoo.db.list())

# Login (the object returned is a browsable record)
odoo.login(local_database,local_user, local_passwd)
#user = odoo.env.user
#print(user.name)            # name of the user connected
#print(user.company_id.name) # the name of its company

#for template in oerp.get('product.template').browse(oerp.get('product.template').search([('','','')])):
#for template in oerp.get('product.template').browse(oerp.get('product.template').search([])):

for p in odoo.env['res.partner'].search([]):
    for c in p.child_ids.search([('name', 'like', 'PARTNER WITH NO NAME')]):
        if(c.type == ''):
            record = c.write({'name': 'default'})
        else:
            record = c.write({'name': c.type})


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
