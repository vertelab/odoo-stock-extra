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

#Find all top level customers without customer numbers
ids = odoo.env['res.partner'].search([('customer_no', '=', False), ('parent_id', '=', False)])
print "Found %s partners" % len(ids)
for id in ids:
    print "Updating res.partner with id %s" % id
    partner = odoo.env['res.partner'].read(id, ['ref'])
    odoo.env['res.partner'].write(id, partner)
    
ids = odoo.env['res.partner'].search([('customer_no', '=', False)])
if not ids:
    print "All partners have customer numbers!"
else:
    print "%s partners are missing customer number!" % len(ids)
    print ids

ids = odoo.env['res.partner'].search([('customer_no', '=', False), ('parent_id', '=', False)])
if ids:
    print "Found %s top level partners without customer numbers." % len(ids)
    print ids

ids = odoo.env['res.partner'].search([('customer_no', '=', False), ('parent_id', '!=', False)])
ids = odoo.env['res.partner'].search([('customer_no', '!=', False), ('child_ids', 'in', ids)])
if ids:
    print "Found %s partners without customer number, but with parents that have customer number." %len(ids)
    print ids

ids = odoo.env['res.partner'].search([('customer_no', '=', False), ('ref', '!=', False)])
if ids:
    print "Found %s partners that have ref, but have parents without customer numbers!" % len(ids)
    print ids
