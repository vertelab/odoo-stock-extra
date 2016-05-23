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

# sudo pip install -U erppeek
# http://wirtel.be/posts/2014/06/13/using_erppeek_to_discuss_with_openerp/
# http://erppeek.readthedocs.org/

import erppeek

#db_new = erppeek.Client.from_config('local')
#db_new = erppeek.Client.from_config('eightzero')
db_old = erppeek.Client.from_config('sixone')


# Create stock.quant  in new database
for prod_o in db_old.model('product.product').browse(db_old.model('product.product').search([('default_code','=','1002-00030')])):
    for move in db_old.model('stock.move').browse(db_old.model('stock.move').search([('product_id','=',prod_o.id)])):
        print move.name,move.location_id.name




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
