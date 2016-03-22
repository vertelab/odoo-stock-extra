all : migrate_product_variants2.pyc

migrate_product_variants2.pyc : migrate_product_variants2.py
	python -m py_compile migrate_product_variants2.py
	sudo cp migrate_product_variants2.pyc /usr/bin/dn-migrate-products
	sudo chmod a+rx /usr/bin/dn-migrate-products
	@echo 
	@echo "=================================="
	@echo "This script requires odoorpc. You can install it by running:"
	@echo "sudo pip install odoorpc"
	@echo "=================================="
