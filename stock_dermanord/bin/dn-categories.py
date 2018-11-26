#!/usr/bin/python
import odoorpc
import argparse


parser = argparse.ArgumentParser(prog='cp_categories',description='Copy public categories between two Odoo databases.')
parser.add_argument('--list','-l',action='store_true', help='List databases')
parser.add_argument('--password','-p', dest='password',help='Password for the databases')
parser.add_argument('--user','-u', dest='user',default='admin',help='User for login')
parser.add_argument('--server','-s', dest='server',default='localhost',help='Server or ip')
parser.add_argument('--port','-P', dest='port',default='8069',help='Port (default 8069)')
parser.add_argument('databases',nargs=2,default='',help='A list of two databases from to')

args = parser.parse_args()
print args.databases


# Prepare the connection to the server
db_from = odoorpc.ODOO(args.server, port=args.port)
db_to = odoorpc.ODOO(args.server, port=args.port)

# Check available databases
if args.list:
    print(db_from.db.list())
    exit()
# Login
db_from.login(args.databases[0], args.user, args.password)
db_to.login(args.databases[1], args.user, args.password)

print 'Hello'
# Current user
user = db_from.env.user
print "Hello again"
print(user.name)            # name of the user connected
print(user.company_id.name) # the name of its company

# Simple 'raw' query
user_data = db_from.execute('res.users', 'read', [user.id])
print(user_data)

exit()
# Use all methods of a model
if 'sale.order' in odoo.env:
    Order = odoo.env['sale.order']
    order_ids = Order.search([])
    for order in Order.browse(order_ids):
        print(order.name)
        products = [line.product_id.name for line in order.order_line]
        print(products)

# Update data through a record
user.name = "Brian Jones"
