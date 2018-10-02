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

#stock_quant_move_rel.move_id

class stock_move(models.Model):
    _inherit = "stock.move"
    
    # Queries on procurement_id take a lot of time when confirming a sale order (~2.5 s per line)
    procurement_id = fields.Many2one(index=True)

class procurement_order(models.Model):
    _inherit = "procurement.order"

    # Queries on sale_line_id and group_id take a lot of time when confirming a sale order (~1.5 s per line)
    sale_line_id = fields.Many2one(index=True)
    group_id = fields.Many2one(index=True)

class stock_move_operation_link(models.Model):
    _inherit = "stock.move.operation.link"
    
    # Queries on operation_id and move_id take a lot of time when moving a picking order
    operation_id = fields.Many2one(index=True)
    move_id = fields.Many2one(index=True)

class stock_pack_operation(models.Model):
    _inherit = "stock.pack.operation"
    
    # Queries on picking_id take a lot of time when moving a picking order
    picking_id = fields.Many2one(index=True)
    
class stock_picking(models.Model):
    _inherit = "stock.picking"

    creditcard = fields.Boolean('Credit card',oldname='x_creditcard')
    expected_delivery_date = fields.Date('Expected Delivery Date',oldname='x_expected_delivery_date')
    claim = fields.Boolean('Claim')
    #export_shipping = fields.Boolean('Foreign shipping',oldname='x_export_shipping')
    picking_user = fields.Char('Old picking user',oldname='x_pickin_user')
    #~ user_id = fields.Many2one(string='Picking user', comodel_name='res.users')

# stock_multiple_users
    employee_id = fields.Many2one(string='Picking employee', comodel_name='hr.employee')
    employee_id_readonly = fields.Boolean(compute='_get_employee_id_readonly')
    qc_id = fields.Many2one(string='Controlled by', comodel_name='hr.employee')
    qc_user = fields.Char(string='Old controlled by', oldname='x_qc')
    pickup_time = fields.Datetime('Pickup time',oldname='x_pickup_time')
    prio = fields.Boolean('Prio',oldname='x_prio')
    pure_cell = fields.Boolean('Cell',oldname='x_pure_cell')
    ready4picking = fields.Boolean('Ready for picking',oldname='x_ready4picking')
    #~ invoice_type = fields.Selection(string='Invoice Type', [('invoice_in_package','Invoice in package'),('invoice_in_letter','Invoice in letter')])
    #~ invoice_control = fields.Selection(string='Invoice Control', [('2_b_invoiced','To be invoiced')])
    address_id = fields.Many2one(comodel_name='res.partner', related='sale_id.partner_shipping_id')

    @api.one
    def _get_employee_id_readonly(self):
        self.employee_id_readonly = self.env.user not in self.env.ref('stock.group_stock_manager').users

    #~ @api.model
    #~ def _prepare_pack_ops(self, picking, quants, forced_qties):
        #~ """ returns a list of dict, ready to be used in create() of stock.pack.operation.

        #~ :param picking: browse record (stock.picking)
        #~ :param quants: browse record list (stock.quant). List of quants associated to the picking
        #~ :param forced_qties: dictionary showing for each product (keys) its corresponding quantity (value) that is not covered by the quants associated to the picking
        #~ """
        #~ cr, uid, context = self._cr, self._uid, self._context
        #~ _logger.warn('quants: %s' % quants)
        #~ def _picking_putaway_apply(product):
            #~ location = False
            #~ # Search putaway strategy
            #~ if product_putaway_strats.get(product.id):
                #~ location = product_putaway_strats[product.id]
            #~ else:
                #~ location = self.pool.get('stock.location').get_putaway_strategy(cr, uid, picking.location_dest_id, product, context=context)
                #~ product_putaway_strats[product.id] = location
            #~ return location or picking.location_dest_id.id

        #~ # If we encounter an UoM that is smaller than the default UoM or the one already chosen, use the new one instead.
        #~ product_uom = {} # Determines UoM used in pack operations
        #~ location_dest_id = None
        #~ location_id = None
        #~ for move in [x for x in picking.move_lines if x.state not in ('done', 'cancel')]:
            #~ if not product_uom.get(move.product_id.id):
                #~ product_uom[move.product_id.id] = move.product_id.uom_id
            #~ if move.product_uom.id != move.product_id.uom_id.id and move.product_uom.factor > product_uom[move.product_id.id].factor:
                #~ product_uom[move.product_id.id] = move.product_uom
            #~ if not (move.scrapped or picking.picking_type_id.code in ('incoming', 'internal')) :
                #~ if location_dest_id and move.location_dest_id.id != location_dest_id:
                    #~ raise Warning(_('The destination location must be the same for all the moves of the picking.'))
                #~ location_dest_id = move.location_dest_id.id
                #~ if location_id and move.location_id.id != location_id:
                    #~ raise Warning(_('The source location must be the same for all the moves of the picking.'))
                #~ location_id = move.location_id.id

        #~ pack_obj = self.pool.get("stock.quant.package")
        #~ quant_obj = self.pool.get("stock.quant")
        #~ vals = []
        #~ qtys_grouped = {}
        #~ #for each quant of the picking, find the suggested location
        #~ quants_suggested_locations = {}
        #~ product_putaway_strats = {}
        #~ for quant in quants:
            #~ if quant.qty <= 0:
                #~ continue
            #~ suggested_location_id = _picking_putaway_apply(quant.product_id)
            #~ quants_suggested_locations[quant] = suggested_location_id

        #~ #find the packages we can movei as a whole
        #~ top_lvl_packages = self._get_top_level_packages(quants_suggested_locations)
        #~ # and then create pack operations for the top-level packages found
        #~ for pack in top_lvl_packages:
            #~ pack_quant_ids = pack_obj.get_content(cr, uid, [pack.id], context=context)
            #~ pack_quants = quant_obj.browse(cr, uid, pack_quant_ids, context=context)
            #~ vals.append({
                    #~ 'picking_id': picking.id,
                    #~ 'package_id': pack.id,
                    #~ 'product_qty': 1.0,
                    #~ 'location_id': pack.location_id.id,
                    #~ 'location_dest_id': quants_suggested_locations[pack_quants[0]],
                    #~ 'owner_id': pack.owner_id.id,
                #~ })
            #~ #remove the quants inside the package so that they are excluded from the rest of the computation
            #~ for quant in pack_quants:
                #~ del quants_suggested_locations[quant]

        #~ # Go through all remaining reserved quants and group by product, package, lot, owner, source location and dest location
        #~ for quant, dest_location_id in quants_suggested_locations.items():
            #~ key = (quant.product_id.id, quant.package_id.id, quant.lot_id.id, quant.owner_id.id, quant.location_id.id, dest_location_id)
            #~ if qtys_grouped.get(key):
                #~ qtys_grouped[key] += quant.qty
            #~ else:
                #~ qtys_grouped[key] = quant.qty

        #~ # Do the same for the forced quantities (in cases of force_assign or incomming shipment for example)
        #~ for product, qty in forced_qties.items():
            #~ if qty <= 0:
                #~ continue
            #~ suggested_location_id = _picking_putaway_apply(product)
            #~ key = (product.id, False, False, picking.owner_id.id, picking.location_id.id, suggested_location_id)
            #~ if qtys_grouped.get(key):
                #~ qtys_grouped[key] += qty
            #~ else:
                #~ qtys_grouped[key] = qty

        #~ # Create the necessary operations for the grouped quants and remaining qtys
        #~ uom_obj = self.pool.get('product.uom')
        #~ prevals = {}
        #~ for key, qty in qtys_grouped.items():
            #~ product = self.pool.get("product.product").browse(cr, uid, key[0], context=context)
            #~ uom_id = product.uom_id.id
            #~ qty_uom = qty
            #~ if product_uom.get(key[0]):
                #~ uom_id = product_uom[key[0]].id
                #~ qty_uom = uom_obj._compute_qty(cr, uid, product.uom_id.id, qty, uom_id)
            #~ val_dict = {
                #~ 'picking_id': picking.id,
                #~ 'product_qty': qty_uom,
                #~ 'product_id': key[0],
                #~ 'package_id': key[1],
                #~ 'lot_id': key[2],
                #~ 'owner_id': key[3],
                #~ 'location_id': key[4],
                #~ 'location_dest_id': key[5],
                #~ 'product_uom_id': uom_id,
            #~ }
            #~ if key[0] in prevals:
                #~ prevals[key[0]].append(val_dict)
            #~ else:
                #~ prevals[key[0]] = [val_dict]
        #~ # prevals var holds the operations in order to create them in the same order than the picking stock moves if possible
        #~ processed_products = set()
        #~ for move in [x for x in picking.move_lines if x.state not in ('done', 'cancel')]:
            #~ if move.product_id.id not in processed_products:
                #~ vals += prevals.get(move.product_id.id, [])
                #~ processed_products.add(move.product_id.id)
        #~ _logger.warn('vals: %s' % vals)
        #~ return vals

class purchase_order(models.Model):
    _inherit = "purchase.order"

    @api.one
    def action_picking_create(self):
        picking_id = super(purchase_order, self).action_picking_create()
        self.env['stock.picking'].browse(picking_id).expected_delivery_date = self.minimum_planned_date

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
