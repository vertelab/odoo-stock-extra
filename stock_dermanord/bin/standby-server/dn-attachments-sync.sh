#!/bin/bash

SRC_ADDRESS=192.168.2.40

rsync -var --delete $SRC_ADDRESS:/var/lib/odoo/.local/share/Odoo/filestore /var/lib/odoo/.local/share/Odoo
