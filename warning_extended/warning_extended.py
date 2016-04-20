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


from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

#~ class stock_picking(models.Model):
    #~ _inherit = "stock.picking"


class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.model
    @api.onchange('user_id')
    def onchange_warning_extended(self):
        #raise Warning(self)
        if self.partner_id.sale_warn != 'no-message':
            warning = {
                    'title': _("Warning for %s") % self.partner_id.name,
                    'message': self.partner_id.sale_warn_msg,
            }
            if self.partner_id.sale_warn == 'warning':
                return {'value': {}, 'warning': warning}
            if self.partner_id.sale_warn == 'block':
                return {'value': {'partner_id': False,'user_id': False,}, 'warning': warning} # Does not block really

#~ class purchase_order(osv.osv):
    #~ _inherit = 'purchase.order'
    #~ def onchange_partner_id(self, cr, uid, ids, part, context=None):
        #~ if not part:
            #~ return {'value':{'partner_address_id': False}}
        #~ warning = {}
        #~ title = False
        #~ message = False
        #~ partner = self.pool.get('res.partner').browse(cr, uid, part, context=context)
        #~ if partner.purchase_warn != 'no-message':
            #~ title = _("Warning for %s") % partner.name
            #~ message = partner.purchase_warn_msg
            #~ warning = {
                #~ 'title': title,
                #~ 'message': message
                #~ }
            #~ if partner.purchase_warn == 'block':
                #~ return {'value': {'partner_id': False}, 'warning': warning}

        #~ result =  super(purchase_order, self).onchange_partner_id(cr, uid, ids, part, context=context)

        #~ if result.get('warning',False):
            #~ warning['title'] = title and title +' & '+ result['warning']['title'] or result['warning']['title']
            #~ warning['message'] = message and message + ' ' + result['warning']['message'] or result['warning']['message']

        #~ if warning:
            #~ result['warning'] = warning
        #~ return result



#~ class account_invoice(osv.osv):
    #~ _inherit = 'account.invoice'
    #~ def onchange_partner_id(self, cr, uid, ids, type, partner_id,
                            #~ date_invoice=False, payment_term=False,
                            #~ partner_bank_id=False, company_id=False,
                            #~ context=None):
        #~ if not partner_id:
            #~ return {'value': {
            #~ 'account_id': False,
            #~ 'payment_term': False,
            #~ }
        #~ }
        #~ warning = {}
        #~ title = False
        #~ message = False
        #~ partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
        #~ if partner.invoice_warn != 'no-message':
            #~ title = _("Warning for %s") % partner.name
            #~ message = partner.invoice_warn_msg
            #~ warning = {
                #~ 'title': title,
                #~ 'message': message
                #~ }

            #~ if partner.invoice_warn == 'block':
                #~ return {'value': {'partner_id': False}, 'warning': warning}

        #~ result =  super(account_invoice, self).onchange_partner_id(cr, uid, ids, type, partner_id,
            #~ date_invoice=date_invoice, payment_term=payment_term,
            #~ partner_bank_id=partner_bank_id, company_id=company_id, context=context)

        #~ if result.get('warning',False):
            #~ warning['title'] = title and title +' & '+ result['warning']['title'] or result['warning']['title']
            #~ warning['message'] = message and message + ' ' + result['warning']['message'] or result['warning']['message']

        #~ if warning:
            #~ result['warning'] = warning
        #~ return result


class stock_picking(models.Model):
    _inherit = 'stock.picking'

    @api.one
    def _picking_warn_msg(self):
        if not self.partner_id.parent_id:
            self.picking_warn_msg = self.partner_id.picking_warn_msg
        else:
            self.picking_warn_msg = self.partner_id.parent_id.picking_warn_msg

    @api.one
    def _picking_warn(self):
        if not self.partner_id.parent_id:
            self.picking_warn = self.partner_id.picking_warn
        else:
            self.picking_warn = self.partner_id.parent_id.picking_warn

    picking_warn_msg = fields.Text(compute='_picking_warn_msg')
    picking_warn = fields.Char(compute='_picking_warn')



    #~ @api.multi
    #~ @api.onchange('state')
    #~ def onchange_warning(self):
        #~ raise Warning('Hejsan')
        #~ for s in self:
            #~ if self.partner_id.picking_warn != 'no-message':
                #~ warning = {
                        #~ 'title': _("Warning for %s") % self.partner_id.name,
                        #~ 'message': self.partner_id.picking_warn_msg,
                #~ }
                #~ if self.partner_id.sale_warn == 'block':
                    #~ return {'value': {'partner_id': False}, 'warning': warning}
    #~
    @api.multi
    @api.onchange('employee_id')
    def onchange_employee_id(self):
        warning = {'title': 'Warning for %s' % self.partner_id.name, 'message': self.picking_warn_msg}
        if self.picking_warn == 'warning':
            return {'value': {}, 'warning': warning}
        if self.picking_warn == 'block':
            return {'value': {'partner_id' : False}, 'warning': warning}



    @api.multi
#    def do_enter_transfer_details(self, cr,uid,ids,picking,context=None):
    def action_assign(self,picking, context=None):
        #raise Warning('%s | %s' % (ids,picking))
        if self.picking_warn in ['warning', 'block']:
            #~ partner_id = self.partner_id.parent_id.id
            compose_form = self.env.ref('warning_extended.view_stock_picking_form', False)
            #~ raise Warning('%s' % compose_form)
            return {
                'name': _('Warning'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'stock.picking',
                'views': [(compose_form.id, 'form')],
                'view_id': compose_form.id,
                'target': 'new',
                'context': None,
                'res_id': self.id,
            }
        else:
            return super(stock_picking, self).action_assign()


    @api.multi
    def action_assign_super(self):
        return super(stock_picking, self[0]).action_assign()

#~ class product_product(osv.osv):
    #~ _inherit = 'product.template'
    #~ _columns = {
         #~ 'sale_line_warn' : fields.selection(WARNING_MESSAGE,'Sales Order Line', help=WARNING_HELP, required=True),
         #~ 'sale_line_warn_msg' : fields.text('Message for Sales Order Line'),
         #~ 'purchase_line_warn' : fields.selection(WARNING_MESSAGE,'Purchase Order Line', help=WARNING_HELP, required=True),
         #~ 'purchase_line_warn_msg' : fields.text('Message for Purchase Order Line'),
     #~ }

    #~ _defaults = {
         #~ 'sale_line_warn' : 'no-message',
         #~ 'purchase_line_warn' : 'no-message',
    #~ }


#~ class sale_order_line(osv.osv):
    #~ _inherit = 'sale.order.line'
    #~ def product_id_change_with_wh(self, cr, uid, ids, pricelist, product, qty=0,
            #~ uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            #~ lang=False, update_tax=True, date_order=False, packaging=False,
            #~ fiscal_position=False, flag=False, warehouse_id=False, context=None):
        #~ warning = {}
        #~ if not product:
            #~ return {'value': {'th_weight' : 0, 'product_packaging': False,
                #~ 'product_uos_qty': qty}, 'domain': {'product_uom': [],
                   #~ 'product_uos': []}}
        #~ product_obj = self.pool.get('product.product')
        #~ product_info = product_obj.browse(cr, uid, product)
        #~ title = False
        #~ message = False

        #~ if product_info.sale_line_warn != 'no-message':
            #~ title = _("Warning for %s") % product_info.name
            #~ message = product_info.sale_line_warn_msg
            #~ warning['title'] = title
            #~ warning['message'] = message
            #~ if product_info.sale_line_warn == 'block':
                #~ return {'value': {'product_id': False}, 'warning': warning}

        #~ result =  super(sale_order_line, self).product_id_change_with_wh( cr, uid, ids, pricelist, product, qty,
            #~ uom, qty_uos, uos, name, partner_id,
            #~ lang, update_tax, date_order, packaging, fiscal_position, flag, warehouse_id=warehouse_id, context=context)

        #~ if result.get('warning',False):
            #~ warning['title'] = title and title +' & '+result['warning']['title'] or result['warning']['title']
            #~ warning['message'] = message and message +'\n\n'+result['warning']['message'] or result['warning']['message']

        #~ if warning:
            #~ result['warning'] = warning
        #~ return result


#~ class purchase_order_line(osv.osv):
    #~ _inherit = 'purchase.order.line'
    #~ def onchange_product_id(self,cr, uid, ids, pricelist, product, qty, uom,
            #~ partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            #~ name=False, price_unit=False, state='draft', context=None):
        #~ warning = {}
        #~ if not product:
            #~ return {'value': {'price_unit': price_unit or 0.0, 'name': name or '', 'product_uom' : uom or False}, 'domain':{'product_uom':[]}}
        #~ product_obj = self.pool.get('product.product')
        #~ product_info = product_obj.browse(cr, uid, product)
        #~ title = False
        #~ message = False

        #~ if product_info.purchase_line_warn != 'no-message':
            #~ title = _("Warning for %s") % product_info.name
            #~ message = product_info.purchase_line_warn_msg
            #~ warning['title'] = title
            #~ warning['message'] = message
            #~ if product_info.purchase_line_warn == 'block':
                #~ return {'value': {'product_id': False}, 'warning': warning}

        #~ result =  super(purchase_order_line, self).onchange_product_id(cr, uid, ids, pricelist, product, qty, uom,
            #~ partner_id, date_order=date_order, fiscal_position_id=fiscal_position_id, date_planned=date_planned, name=name, price_unit=price_unit, state=state, context=context)

        #~ if result.get('warning',False):
            #~ warning['title'] = title and title +' & '+result['warning']['title'] or result['warning']['title']
            #~ warning['message'] = message and message +'\n\n'+result['warning']['message'] or result['warning']['message']

        #~ if warning:
            #~ result['warning'] = warning
        #~ return result



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
