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


class stock_picking_wizard(models.TransientModel):
    _name = 'stock.picking.wizard'
    _description = 'Get the first available stock picking'

    def _default_picking_type(self):
        return self.env.ref('stock.picking_type_out', False)
    picking_type_id = fields.Many2one(comodel_name='stock.picking.type', string='Picking Type', default=_default_picking_type)
    def _default_employee_id(self):
        hr = self.env['hr.employee'].search([('user_id', '=', self.env.uid if self.env.uid else '')])
        return hr[0].id if len(hr) > 0 else None
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Picking User', default=_default_employee_id)

    @api.multi
    def get_first_available_picking(self):
        picking = self.env['stock.picking'].search([('picking_type_id', '=', self.picking_type_id.id), ('employee_id', '=', None), ('state', '=', 'assigned')])
        if len(picking) > 0:
            picking[0].write({ 'employee_id': self.employee_id.id })
            picking_form = self.env.ref('stock.view_picking_form', False)
            ctx = dict(
                default_model='stock.picking',
                default_res_id=picking[0].id,
            )
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'stock.picking',
                'views': [(picking_form.id, 'form')],
                'view_id': picking_form.id,
                'res_id': picking[0].id if picking else None,
                'context': ctx,
            }
        else:
            raise Warning(_('No available pickings'))

