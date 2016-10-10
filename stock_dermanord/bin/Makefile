
all : erppeek.tmp dn-migrate-products.tmp odoorpc.tmp dn-customer_no.tmp dn-partner_name.tmp dn-fix-product-template-attributes.tmp dn-inventory-remote.tmp dn-weight.tmp dn-product_name.tmp dn-get_product_category.tmp dn-account_voucher_customer_no.tmp dn-iskit.tmp dn-latest-activity.tmp dn-update-product_info.tmp dn-remove_old_translation.tmp
	@echo Complete

erppeek.tmp:
	@sudo pip install erppeek
	@cp erppeek.ini ~
	@echo "erppeek.ini copied to ~ (run your commands from your home directory)"
	@touch erppeek.tmp

odoorpc.tmp:
	@sudo pip install odoorpc
	@touch odoorpc.tmp

dn-migrate-products.tmp: dn-migrate-products.py
	@sudo cp dn-migrate-products.py /usr/bin/dn-migrate-products
	@sudo chmod a+x /usr/bin/dn-migrate-products
	@touch dn-migrate-products.tmp

dn-account_voucher_customer_no.tmp: dn-account_voucher_customer_no.py
	@sudo cp dn-account_voucher_customer_no.py /usr/bin/dn-account_voucher_customer_no
	@sudo chmod a+x /usr/bin/dn-account_voucher_customer_no
	@echo "dn-account_voucher_customer_no copied to /usr/bin"
	@touch dn-account_voucher_customer_no.tmp

dn-inventory-remote.tmp: dn-inventory-remote.py
	@sudo cp dn-inventory-remote.py /usr/bin/dn-inventory-remote
	@sudo chmod a+x /usr/bin/dn-inventory-remote
	@touch dn-inventory-remote.tmp

dn-fix-product-template-attributes.tmp: dn-fix-product-template-attributes.py
	@sudo cp dn-fix-product-template-attributes.py /usr/bin/dn-fix-product-template-attributes
	@sudo chmod a+x /usr/bin/dn-fix-product-template-attributes
	@touch dn-fix-product-template-attributes.tmp

dn-partner_name.tmp: dn-partner_name.py
	@sudo cp dn-partner_name.py /usr/bin/dn-partner_name
	@sudo chmod a+x /usr/bin/dn-partner_name
	@touch dn-partner_name.tmp

dn-customer_no.tmp: dn-customer_no.py
	@sudo cp dn-customer_no.py /usr/bin/dn-customer_no
	@sudo chmod a+x /usr/bin/dn-customer_no
	@touch dn-customer_no.tmp

dn-iskit.tmp: dn-iskit.py
	@sudo cp dn-iskit.py /usr/bin/dn-iskit
	@sudo chmod a+x /usr/bin/dn-iskit
	@touch dn-iskit.tmp

dn-weight.tmp: dn-weight.py
	@sudo cp dn-weight.py /usr/bin/dn-weight
	@sudo chmod a+x /usr/bin/dn-weight
	@touch dn-weight.tmp

dn-weborder_sync.tmp: dn-weborder_sync.py
	@sudo cp dn-weborder_sync.py /usr/bin/dn-weborder_sync
	@sudo chmod a+x /usr/bin/dn-weborder_sync
	@touch dn-weborder_sync.tmp

dn-product_name.tmp: dn-product_name.py
	@sudo cp dn-product_name.py /usr/bin/dn-product_name
	@sudo chmod a+x /usr/bin/dn-product_name
	@touch dn-product_name.tmp

dn-get_product_category.tmp: dn-get_product_category.py
	@sudo cp dn-get_product_category.py /usr/bin/dn-get_product_category
	@sudo chmod a+x /usr/bin/dn-get_product_category
	@touch dn-get_product_category.tmp

dn-latest-activity.tmp: dn-latest-activity.py
	@sudo cp dn-latest-activity.py /usr/bin/dn-latest-activity
	@sudo chmod a+x /usr/bin/dn-latest-activity
	@touch dn-latest-activity.tmp

dn-update-product_info.tmp: dn-update-product_info.py
	@sudo cp dn-update-product_info.py /usr/bin/dn-update-product_info
	@sudo chmod a+x /usr/bin/dn-update-product_info
	@touch dn-update-product_info.tmp

dn-remove_old_translation.tmp: dn-remove_old_translation.py
	@sudo cp dn-remove_old_translation.py /usr/bin/dn-remove_old_translation
	@sudo chmod a+x /usr/bin/dn-remove_old_translation
	@touch dn-remove_old_translation.tmp

clean:
	@rm -f *tmp
	@echo "Cleaned up"

