all : bin/migrate_product_variants2.pyc

bin/migrate_product_variants2.pyc : bin/migrate_product_variants2.py
	python -m py_compile bin/migrate_product_variants2.py
	sudo cp bin/migrate_product_variants2.pyc /usr/bin/dn-migrate-products
	chmod u+x /usr/bin/dn-migrate-products
	@echo 
	@echo "=================================="
	@echo "This script requires odoorpc. You can install it by running:"
	@echo "sudo pip install odoorpc"
	@echo "=================================="
