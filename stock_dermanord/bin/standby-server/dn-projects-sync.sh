#!/bin/bash

# Load odootools
. /etc/profile.d/odootools.sh

SRC_ADDRESS=192.168.2.40
SRC_PROJECTS=$(sudo ssh $SRC_ADDRESS ls /usr/share | grep odoo | grep -v odoo-addons)
LOC_PROJECTS=$(ls /usr/share | grep odoo | grep -v odoo-addons)

# Check if we got a list of projects
if [ "$SRC_PROJECTS" = "" ]
then
        exit
fi

# Check if any projects are to be removed
for p in $LOC_PROJECTS
do
        DEL_PROJECT=1
        for sp in $SRC_PROJECTS
        do
                if [ "$sp" = "$p" ]
                then
                        DEL_PROJECT=0
                fi
        done
        if [ "$DEL_PROJECT" -eq 1 ]
        then
                sudo rm -rf /usr/share/$p
        fi
done

# Sync projects
for p in $SRC_PROJECTS
do
        sudo rsync -var --delete --filter="-, p *.pyc" $SRC_ADDRESS:/usr/share/$p /usr/share
        sudo chown odoo:odoo /usr/share/$p -R
        sudo chmod g+w /usr/share/$p -R;
done

# Update addons path and restart Odoo
odooaddons
#odoorestart
# That didn't work for some reason
sudo service odoo restart && sudo service apache2 restart
