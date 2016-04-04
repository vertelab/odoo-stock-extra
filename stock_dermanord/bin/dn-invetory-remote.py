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
db_new = erppeek.Client.from_config('test')
#db_new = erppeek.Client.from_config('eightzero')
db_old = erppeek.Client.from_config('sixone')

# Null qty in new database
for prod_o in db_old.model('product.product').browse(db_old.model('product.product').search([])):
    prod_n = db_new.model('product.product').browse(db_old.model('product.product').search([('default_code','=',prod_o.default_code)]))[0]
    #print "to check %s" % prod_o.default_code
    print 'Null qty',prod_o.name
    stock = db_new.model('stock.change.product.qty').create({
            'product_id' : prod_n.id,
            'new_quantity': 0.0,
    })
    stock.change_product_qty()

# Create stock.quant  in new database
for prod_o in db_old.model('product.product').browse(db_old.model('product.product').search([])):
    prod_n = db_new.model('product.product').browse(db_old.model('product.product').search([('default_code','=',prod_o.default_code)]))[0]
    #print "to check %s" % prod_o.default_code

    move = db_old.model('stock.move').browse([db_old.model('stock.move').search([('product_id','=',prod_o.id)],order='date desc')[0]])[0]
    #print move.name,move.location_id.name,move.location_id.location_id.name,move.location_id.location_id.id
    parent_id = db_new.model('stock.location').search([('name','=',move.location_id.location_id.name)])[0]
    #print 'parent',parent_id
    location_id = db_new.model('stock.location').search(['&',('name','=',move.location_id.name),('location_id','=',parent_id)])[0]
    print 'New qty',prod_o.name,prod_o.qty_available,location_id
    stock = db_new.model('stock.quant').create({
            'product_id' : prod_n.id,
            'qty': prod_o.qty_available,
            'location_id': location_id,
    })
# Check 
for prod_o in db_old.model('product.product').browse(db_old.model('product.product').search([])):
    prod_n = db_new.model('product.product').browse(db_old.model('product.product').search([('default_code','=',prod_o.default_code)]))[0]
    #print "to check %s" % prod_o.default_code
    if not prod_o.qty_available == prod_n.qty_available:
        print 'Check error',prod_o.name,prod_o.qty_available,prod_n.qty_available

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
