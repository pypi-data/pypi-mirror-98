#!/bin/sh
#
# STIG URL: http://www.stigviewer.com/stig/red_hat_enterprise_linux_6/2014-06-11/finding/V-38529
# Finding ID:	V-38529
# Version:	RHEL-06-000089
# Finding Level:	Medium
#
#     The system must not accept IPv4 source-routed packets by default. 
#     Accepting source-routed packets in the IPv4 protocol has few 
#     legitimate uses. It should be disabled unless it is absolutely 
#     required.
#
############################################################

diag_out() {
   echo "${1}"
}

diag_out "----------------------------------"
diag_out "STIG Finding ID: V-38529"
diag_out "  System must not accept IPv4"
diag_out "  secure redirect routed packets on"
diag_out "  any interface"
diag_out "----------------------------------"
