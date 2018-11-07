#!/bin/bash

CURRENT=$(df | grep /$ | awk '{ print $5}' | sed 's/%//g')
THRESHOLD=30
RECIPIENTS='robin.chatfield@vertel.se anders.wallenquist@vertel.se haojun.zou@vertel.se claes-johan.dahlin@dermanord.se'
SENDER=noreply@vertel.se

if [ "$CURRENT" -gt "$THRESHOLD" ] ; then
    for RECIPIENT in $RECIPIENTS
    do
        mail -s $HOSTNAME' Disk Space Alert' -aFrom:$SENDER $RECIPIENT << EOF
Your remaining free disk space is critically low.
Used: $CURRENT%
EOF
    done
fi
