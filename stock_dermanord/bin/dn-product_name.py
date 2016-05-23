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
#~ params = odoorpc.session.get('test')
params = odoorpc.session.get('dermanord')
odoo = odoorpc.ODOO(params.get('host'),port=params.get('port'))
odoo.login(params.get('database'),params.get('user'),params.get('passwd'))


# Correct product.template (name has comma-form and are translated without comma)
for t in odoo.env['ir.translation'].read(odoo.env['ir.translation'].search(['&','&',('name','=','product.template,name'),('lang','=','sv_SE'),('source','like','%,%')]),['id','source','value']):
    product = odoo.env['product.template'].search([('name','=',t['source'])])[0]
    odoo.env['product.template'].write(product,{'name': t['value']})

# Correct ir.translation
odoo.env['ir.translation'].unlink(odoo.env['ir.translation'].search([('name','=','product.template,name')]))


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
