#!/bin/sh
#
# STIG URL: http://www.stigviewer.com/stig/red_hat_enterprise_linux_6/2014-06-11/finding/V-38588
# Finding ID:	V-38588
# Version:	RHEL-06-000070
# Finding Level:	Medium
#
#     The system must not permit interactive boot. Using interactive boot, 
#     the console user could disable auditing, firewalls, or other 
#     services, weakening system security.
#
############################################################

diag_out() {
   echo "${1}"
}

diag_out "----------------------------------"
diag_out "STIG Finding ID: V-38588"
diag_out "  Disable interactive boot"
diag_out "----------------------------------"
