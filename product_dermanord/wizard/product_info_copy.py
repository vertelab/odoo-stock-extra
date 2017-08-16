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

class product_info_copy_wizard(models.TransientModel):
    _name = 'product.info.copy.wizard'

    def get_name(self):
        obj = self.env['product.product'].browse(self._context.get('active_id'))
        attributes = obj.attribute_value_ids.mapped('name')
        return str(obj.name) + ((', ' + ','.join(attributes)) if len(attributes) > 0 else '')
    name = fields.Char(string='Name', default=get_name)
    def get_ingredients(self):
        return self.env['product.product'].browse(self._context.get('active_id')).ingredients
    ingredients = fields.Text(string='Ingredients', default=get_ingredients)
    ingredients_copy = fields.Boolean(string='Copy Ingredients')
    def get_public_desc(self):
        return self.env['product.product'].browse(self._context.get('active_id')).public_desc
    public_desc = fields.Text(string='Public Description', default=get_public_desc)
    public_desc_copy = fields.Boolean(string='Copy Public Description')
    def get_reseller_desc(self):
        return self.env['product.product'].browse(self._context.get('active_id')).reseller_desc
    reseller_desc = fields.Text(string='Reseller Description', default=get_reseller_desc)
    reseller_desc_copy = fields.Boolean(string='Copy Reseller Description')
    def get_shelf_label_desc(self):
        return self.env['product.product'].browse(self._context.get('active_id')).shelf_label_desc
    shelf_label_desc = fields.Text(string='Shelf Label Description', default=get_shelf_label_desc)
    shelf_label_desc_copy = fields.Boolean(string='Copy Shelf Label Description')
    def get_use_desc(self):
        return self.env['product.product'].browse(self._context.get('active_id')).use_desc
    use_desc = fields.Text(string='Use Description', default=get_use_desc)
    use_desc_copy = fields.Boolean(string='Copy Use Description')

    def get_variants(self):
        return self.env['product.product'].browse(self._context.get('active_id')).product_tmpl_id.product_variant_ids - self.env['product.product'].browse(self._context.get('active_id'))
    product_variants = fields.Many2many(comodel_name='product.product', string='Variants', default=get_variants)

    @api.one
    def copy_info(self):
        source = self.env['product.product'].browse(self._context.get('active_id'))
        for v in product_variants:
            if self.public_desc_copy:
                v.public_desc = source.public_desc
                v.public_desc_changed_by = source.public_desc_changed_by
                v.public_desc_last_changed = source.public_desc_last_changed
            if self.reseller_desc_copy:
                v.reseller_desc = source.reseller_desc
                v.reseller_desc_changed_by = source.reseller_desc_changed_by
                v.reseller_desc_last_changed = source.reseller_desc_last_changed
            if self.shelf_label_desc_copy:
                v.shelf_label_desc = source.shelf_label_desc
                v.shelf_label_desc_changed_by = source.shelf_label_desc_changed_by
                v.shelf_label_desc_last_changed = source.shelf_label_desc_last_changed
            if self.use_desc_copy:
                v.use_desc = source.use_desc
                v.use_desc_changed_by = source.use_desc_changed_by
                v.use_desc_last_changed = source.use_desc_last_changed
            if self.ingredients_copy:
                v.ingredients = source.ingredients
                v.ingredients_changed_by = source.ingredients_changed_by
                v.ingredients_last_changed = source.ingredients_last_changed

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
