# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import SUPERUSER_ID
from openerp import api, models, fields, _


class purchase_order(models.Model):
    _inherit = "purchase.order"

    def _get_default_partner_id(self, cr, uid, context=None):
        """ Gives default partner_id """
        if context is None:
            context = {}
        if context.get('portal'):
            user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
            # Special case for portal users, as they are not allowed to call name_get on res.partner
            # We save this call for the web client by returning it in default get
            return self.pool['res.partner'].name_get(cr, SUPERUSER_ID, [user.partner_id.id], context=context)[0]
        return False

    _defaults = {
        'partner_id': lambda s, cr, uid, c: s._get_default_partner_id(cr, uid, c),
    }
    
    #TODO: Move edi_gs1 support into its own module.
    @api.one
    def _get_sale_order_id(self):
        order = self.env['sale.order'].browse()
        
        for procurement in self.env['procurement.order'].search([('purchase_id', '=', self.id)]):
            order |= procurement.sale_line_id.order_id
        if len(order) == 1:
            if order.dtm_delivery:
                self.delivery_date = order.dtm_delivery
            else:
                self.delivery_datetime = order.date_order
    delivery_date = fields.Date('Delivery Date', compute='_get_sale_order_id')
    delivery_datetime = fields.Datetime('Delivery Time', compute='_get_sale_order_id')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
