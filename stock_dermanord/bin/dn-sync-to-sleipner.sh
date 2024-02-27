#!/bin/bash

SLEIPNER=192.168.2.51

sudo ssh $SLEIPNER "dn-projects-sync && dn-attachments-sync && dn-flush-cache"
