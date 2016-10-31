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

import openerp.exceptions
from openerp.exceptions import except_orm, Warning, RedirectWarning,MissingError
from openerp import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class stock_picking(models.Model):
    _inherit = "stock.picking"

    creditcard = fields.Boolean('Credit card',oldname='x_creditcard')
    expected_delivery_date = fields.Date('Expected Delivery Date',oldname='x_expected_delivery_date')
    claim = fields.Boolean('Claim')
    #export_shipping = fields.Boolean('Foreign shipping',oldname='x_export_shipping')
    picking_user = fields.Char('Old picking user',oldname='x_pickin_user')
    #~ user_id = fields.Many2one(string='Picking user', comodel_name='res.users')
    employee_id = fields.Many2one(string='Picking employee', comodel_name='hr.employee')
    qc_id = fields.Many2one(string='Controlled by', comodel_name='hr.employee')
    qc_user = fields.Char(string='Old controlled by', oldname='x_qc')
    pickup_time = fields.Datetime('Pickup time',oldname='x_pickup_time')
    prio = fields.Boolean('Prio',oldname='x_prio')
    pure_cell = fields.Boolean('Cell',oldname='x_pure_cell')
    ready4picking = fields.Boolean('Ready for picking',oldname='x_ready4picking')
    #~ invoice_type = fields.Selection(string='Invoice Type', [('invoice_in_package','Invoice in package'),('invoice_in_letter','Invoice in letter')])
    #~ invoice_control = fields.Selection(string='Invoice Control', [('2_b_invoiced','To be invoiced')])
    address_id = fields.Many2one(comodel_name='res.partner', related='sale_id.partner_shipping_id')

    #~ @api.multi
    #~ def write(self, vals):
        #~ raise Warning(vals, self[0].write_date)
        #~ org_rec = self[0]
        #~ if org_rec.employee_id and vals.get('employee_id'):
            #~ action = self.env.ref('stock.do_view_pickings')
            #~ action = action.with_context({'active_id': self[0].id})
            #~ action.domain = [('group_id', '=', self[0].id)]
            #~ raise RedirectWarning('Hejsan hopsan %s' %action.domain, action.id, 'go on')
        #~ _logger.warn('%s, %s' %(org_rec.employee_id.id, vals.get('employee_id')))
        #~ res = super(stock_picking, self[0]).write(vals)
        #~ return res

    #~ @api.v7
    #~ def read(self, cr, user, ids, fields=None, context=None, load='_classic_read'):
        #~ context['record_date'] = 'Haojun7'
        #~ _logger.warn('v7')
        #~ return super(stock_picking, self).read(cr, user, ids, fields, context, load)

    #~ @api.v8
    #~ def read(self, fields=None, load='_classic_read'):
        #~ context = dict(self.env.context)
        #~ context['record_date'] = 'Haojun'
        #~ self.env.context = context
        #~ result = super(stock_picking, self).read(fields, load)
        #~ _logger.warn('v8')
        #~ _logger.warn(result)
        #~ return result

class res_users(models.Model):
   _inherit="res.users"
   def Xname_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if context.get('show_short_name_only'):
            if isinstance(ids, (int, long)):
                ids = [ids]
            return [(r.id,'%s,%s' % (r.street,r.city)) for r in self.browse(cr, uid, ids, context=context)]
        else:
            return super(res_users, self).name_get(cr, uid, ids, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
