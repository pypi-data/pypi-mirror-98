#!/bin/sh
#
# STIG URL: http://www.stigviewer.com/stig/red_hat_enterprise_linux_6/2014-06-11/finding/V-38448
# Finding ID:	V-38448
# Version:	RHEL-06-000037
# Finding Level:	Medium
#
#     The /etc/gshadow file must be group-owned by root. The "/etc/gshadow" 
#     file contains group password hashes. Protection of this file is 
#     critical for system security.
#
#  CCI: CCI-000366
#  NIST SP 800-53 :: CM-6 b
#  NIST SP 800-53A :: CM-6.1 (iv)
#  NIST SP 800-53 Revision 4 :: CM-6 b
#
############################################################

# Standard outputter function
diag_out() {
   echo "${1}"
}

diag_out "----------------------------------"
diag_out "STIG Finding ID: V-38448"
diag_out "  Ensure gshadow is group-owned by"
diag_out "  the root group"
diag_out "----------------------------------"

