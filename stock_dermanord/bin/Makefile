
all : erppeek.tmp dn-migrate-products.tmp odoorpc.tmp dn-customer_no.tmp dn-partner_name.tmp dn-fix-product-template-attributes.tmp dn-inventory-remote.tmp
	@echo Complete
	
erppeek.tmp: 
	@sudo pip install erppeek
	@cp erppeek.ini ~
	@echo erppeek.ini copied to ~ (run your commands from your home directory)
	@touch erppeek.tmp

odoorpc.tmp: 
	@sudo pip install odoorpc
	@touch odoorpc.tmp

dn-migrate-products.tmp: dn-migrate-products.py
	@python -m py_compile dn-migrate-products.py
	@sudo cp dn-migrate-products.pyc /usr/bin/dn-migrate-products
	@sudo chmod a+x /usr/bin/dn-migrate-products
	@touch dn-migrate-products.tmp

dn-inventory-remote.tmp: dn-inventory-remote.py
	@python -m py_compile dn-inventory-remote.py
	@sudo cp dn-inventory-remote.pyc /usr/bin/dn-inventory-remote
	@sudo chmod a+x /usr/bin/dn-inventory-remote
	@touch dn-inventory-remote.tmp

dn-fix-product-template-attributes.tmp: dn-fix-product-template-attributes.py
	@python -m py_compile dn-fix-product-template-attributes.py
	@sudo cp dn-fix-product-template-attributes.pyc /usr/bin/dn-fix-product-template-attributes
	@sudo chmod a+x /usr/bin/dn-fix-product-template-attributes
	@touch dn-fix-product-template-attributes.tmp

dn-partner_name.tmp: dn-partner_name.py
	@python -m py_compile dn-partner_name.py
	@sudo cp dn-partner_name.pyc /usr/bin/dn-partner_name
	@sudo chmod a+x /usr/bin/dn-partner_name
	@touch dn-partner_name.tmp

dn-customer_no.tmp: dn-customer_no.py
	@python -m py_compile dn-customer_no.py
	@sudo cp dn-customer_no.pyc /usr/bin/dn-customer_no
	@sudo chmod a+x /usr/bin/dn-customer_no
	@touch dn-customer_no.tmp


clean:
	@rm -f *pyc
	@echo "Cleaned up"
	
