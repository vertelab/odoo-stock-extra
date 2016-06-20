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

#Find all vouchers without customer numbers
ids = odoo.env['account.voucher'].search([('customer_no', '=', False)])
print "Found %s vouchers" % len(ids)
partners = []
for id in ids:
    print "Updating voucher with id %s" % id
    voucher = odoo.env['account.voucher'].read(id, ['partner_id'])
    partner = odoo.env['res.partner'].read(voucher['partner_id'][0], ['customer_no'])
    if not partner['customer_no'] and not voucher['partner_id'] in partners:
        partners.append(voucher['partner_id'])
    else:
        odoo.env['account.voucher'].write(id, {'customer_no': partner['customer_no']})

if len(partners) > 0:
    print 'Found %s partners without customer number' % len(partners)
    for partner in partners:
        print '%s\t%s' % (partner[0], partner[1])
