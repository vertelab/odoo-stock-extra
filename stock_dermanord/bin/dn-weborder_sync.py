#!/usr/bin/python
# -*- coding: utf-8 -*-

import xmlrpclib
import MySQLdb
import time
import string
import datetime
import re
from collections import defaultdict
from openerp.tools import config
start = time.time()

#Load config file
config.parse_config(['-c', '/etc/odoo/openerp-server.conf'])

username = config.get('weborder_user', False)     #the user
pwd = config.get('weborder_pwd', False)           #the password
dbname = config.get('weborder_db', False)         #the database

cnx = MySQLdb.connect(
    user = config.get('joomla_user', False),
    passwd = config.get('joomla_pwd', False),
    host = config.get('joomla_host', False),
    port = config.get('joomla_port', False),
    db = config.get('joomla_db', False),
    )

cursor = cnx.cursor()
cursor2 = cnx.cursor()
cursor3 = cnx.cursor()

cursor.execute("""SELECT a.order_id, a.customer_note, b.company, b.first_name, b.last_name, b.vm_kundnummer, c.customer_number, a.cdate FROM jos_vm_orders as a, jos_vm_user_info as b, jos_vm_shopper_vendor_xref as c WHERE a.user_id = b.user_id AND b.address_type='BT' AND b.user_id = c.user_id AND a.synced = 0 GROUP BY a.order_id""")

# Get the uid
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/common')

uid = sock.login(dbname, username, pwd)
#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

rows = cursor.fetchall()

if not rows:
    print 'NO ORDERS'
    quit() 

for row in rows:
    args = [('ref', '=', row[5])] #query clause
    #print "%s %s --> %s, %s" % (row[0], row[2], row[5], row[6])
    partner_id = sock.execute(dbname, uid, pwd, 'res.partner', 'search', args)
    if not partner_id:
        args = [('ref', '=', row[5]), ('active', '=', False)] #query clause
        partner_id = sock.execute(dbname, uid, pwd, 'res.partner', 'search', args)
    if not partner_id:
        print "Partner with reference %s. Order id %s." % (row[5], row[0])
        continue
    else:
        # Get Partner data.
        fields = ['address', 'property_product_pricelist', 'property_invoice_type', 'property_account_position', 'property_payment_term', 'property_delivery_carrier']
        partner = sock.execute(dbname, uid, pwd, 'res.partner', 'read', partner_id, fields)[0]

        if partner['property_product_pricelist'][0] == 1:
            rab = 1.00
        elif partner['property_product_pricelist'][0] == 6:
            rab = 0.80
        elif partner['property_product_pricelist'][0] == 3:
            rab = 0.55
        elif partner['property_product_pricelist'][0] == 11:
            rab = 0.45
        elif partner['property_product_pricelist'][0] == 4:
            rab = 0.50
        else:
            print 'Not 45 or 50. Order id %s.' % (row[0])
            continue

        fields = ['type']
#        print partner['property_invoice_type']
     #   addresses = sock.execute(dbname, uid, pwd, 'res.partner.address','read',partner['address'], fields)

        #print row
        order_id = ''
        shipping_id = ''
        invoice_id = ''

#        for address in addresses:
#            if address['type'] == 'default':
 #               invoice_id = address['id']
  #              order_id = address['id']
   #             shipping_id = address['id']
    #            break;
     #       elif address['type'] == 'invoice':
      #          invoice_id = address['id']
       #     elif address['type'] == 'delivery':
        #        shipping_id = address['id']
         #   elif address['type'] == 'contact':
          #      order_id = address['id']
        
      #  if order_id == '':
       #     order_id = invoice_id

 #       print "%s|%s|%s" % (invoice_id, order_id, shipping_id)
        if row[1] != '':
            notes = row[1].decode('cp1252')
            notes = string.replace(notes, '&quot;', '"')
            notes = string.replace(notes, '&amp;', '&')
            notes = string.replace(notes, '\\r', '')
            notes = string.replace(notes, '\\n', '\n')
        else:
            notes = ''
        #print notes
        print 'Partner %s. Weborder %s' % (partner_id[0], row[0])
        order = {
            'client_order_ref' : '%08d' % row[0],
            'company_id' : 1,
          #  'date_order' : datetime.datetime.fromtimestamp(row[7]).strftime("%Y-%m-%d"),
            'fiscal_position' : partner['property_account_position'][0],  # property_account_position
            'invoice_quantity' : 'order',
            'invoice_type_id' : partner['property_invoice_type'][0],  # property_invoice_type
            'note' : 'Weborder %08d\n%s' % (row[0], notes),
            'origin' : '%08d' % row[0],
            'partner_id' : partner_id[0],
	    'section_id': 35,
          #  'partner_invoice_id' : invoice_id,  # address
          #  'partner_order_id' : order_id,    # address
          #  'partner_shipping_id' : shipping_id, # address
            'payment_term' : partner['property_payment_term'][0],  # property_payment_term
            'pricelist_id' : partner['property_product_pricelist'][0],  # property_product_pricelist
            'carrier_id' : partner['property_delivery_carrier'][0],  #property_delivery_carrier
        }
        print order
        order_id = sock.execute(dbname, uid, pwd, 'sale.order', 'create', order)

        cursor2.execute("""SELECT order_item_sku, order_item_name, product_quantity FROM jos_vm_order_item WHERE order_id = %s""", (row[0],))
        rows2 = cursor2.fetchall()
        for row2 in rows2:
            orderItemSku = row2[0][:11]
            args = [('default_code', '=', orderItemSku)]
            ids = sock.execute(dbname, uid, pwd, 'product.product', 'search', args)
            if not ids:
                args = [('default_code', '=', orderItemSku), ('active', '=', False)] #query clause
                ids = sock.execute(dbname, uid, pwd, 'product.product', 'search', args)
            if not ids:
                print "Product saknas [%s] %s." % (row2[0], row2[1])
                continue
            else:
                fields = ['name_template', 'default_code', 'list_price', 'cost_price', 'product_tmpl_id']
                product = sock.execute(dbname, uid, pwd, 'product.product', 'read', ids, fields)[0]
                product_description = sock.execute(dbname, uid, pwd, 'product.product', 'name_get', ids)[0][1]
                order_line = {
                    'order_id' : order_id,
                    'product_id' : product['id'],
                  #  'price_unit' : product['list_price']*rab,
                  #  'purchase_price' : product['cost_price'],
                    'name' : product_description,
                    'product_uom_qty' : row2[2],
		    'delay': 1,
                  #  'tax_id' : [(6, 0, [2])],
                }
                #print order_line
                #args = [[str(partner['property_product_pricelist'])], product['id'], '2.0']
                #print sock.execute_kw(dbname, uid, pwd, 'product.pricelist', 'price_get', args)

                #print product
                order_line_id = sock.execute(dbname, uid, pwd, 'sale.order.line', 'create', order_line)
        #UPDATE
        cursor3.execute("""UPDATE jos_vm_orders SET synced=1, order_status = 'S' WHERE order_id = %s""", (row[0],)) # Dont set order as synced
        cnx.commit()
        #print 'Setting order %s.' % (row[0])
cnx.close()
# VirtueMart - jos_vm_orders
# order_id, user_id

#jos_vm_user_info user_id = user_id
print time.strftime("%H:%M:%S", time.gmtime(time.time() - start))
