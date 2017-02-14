# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, Open Source Management Solution, third party addon
# Copyright (C) 2017- Vertel AB (<http://vertel.se>).
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
from openerp.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)

class product_price_print_wizard(models.TransientModel):
    _name = 'product.price.print.wizard'

    @api.model
    def _product_ids(self):
        return self.env['product.product'].browse(self._context.get('active_ids', []))
    product_ids = fields.Many2many(comodel_name='product.product', default=_product_ids)
    pricelist= fields.Many2one(comodel_name='product.pricelist', string='Price List', required=True)

    @api.model
    def _glabel_template(self):
        return [
            (self.env.ref('product_dermanord.action_shelf_talker_report_522_254_pricelist').id, self.env.ref('product_dermanord.action_shelf_talker_report_522_254_pricelist').name),
            (self.env.ref('product_dermanord.action_shelf_talker_report_70_254_pricelist').id, self.env.ref('product_dermanord.action_shelf_talker_report_70_254_pricelist').name),
            (self.env.ref('product_dermanord.action_shelf_talker_report_105_254_pricelist').id, self.env.ref('product_dermanord.action_shelf_talker_report_105_254_pricelist').name),
        ]
    glabels_template = fields.Selection(string='Glabel Template', selection=_glabel_template, required=True)

    @api.multi
    def print_price(self):
        product_price_label = self.env['product.price.label'].browse([])
        for product in self.product_ids:
            vals = {
                'name': product.name,
                'default_code': product.default_code,
                'pricelist_price': round(self.pricelist.price_get(product.id, 1, None)[self.pricelist.price_get(product.id, 1, None).keys()[0]], 2),
                'ean13': product.ean13,
                'currency_name': product.currency_name,
                'attribute_value_names': ','.join(a.name for a in product.attribute_value_ids),
                'shelf_label_desc': product.shelf_label_desc,
            }
            product_price_label |= self.env['product.price.label'].create(vals)
        return self.env['report'].get_action(product_price_label, self.env['ir.actions.report.xml'].browse(int(self.glabels_template)).report_name)

class product_price_label(models.TransientModel):
    _name = 'product.price.label'

    name = fields.Char(string='Name')
    default_code = fields.Char(string='Internal Reference')
    pricelist_price = fields.Float(sting='Pricelist Price')
    ean13 = fields.Char(string='EAN13 Barcode', size=13)
    currency_name = fields.Char(string='Currency')
    attribute_value_names = fields.Char(string='Attribute Names')
    shelf_label_desc = fields.Text(string='Shelf Label Description')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
