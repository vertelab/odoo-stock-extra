# !/bin/bash

error=$(python /usr/share/odoo-stock-extra/stock_dermanord/bin/dn-sync.py 2>&1 > /dev/null)
if [ $? -ne 0 ]
then
    echo $error|mailx admin@example.com -s "$(date +Sync\ failed\ on\ %Y-%m-%d\ %H\:%M)"
fi
