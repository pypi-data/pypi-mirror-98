#!/bin/sh
#
# STIG URL: http://www.stigviewer.com/stig/red_hat_enterprise_linux_6/2014-06-11/finding/V-38534
# Finding ID:	V-38534
# Version:	RHEL-06-000175
# Finding Level:	Low
#
#     The operating system must automatically audit account modification. 
#     In addition to auditing new user and group accounts, these watches 
#     will alert the system administrator(s) to any modifications. Any 
#     unexpected users, groups, or modifications should be investigated
#     for legitimacy
#
#  CCI: CCI-001403
#  NIST SP 800-53 :: AC-2 (4)
#  NIST SP 800-53A :: AC-2 (4).1 (i&ii)
#  NIST SP 800-53 Revision 4 :: AC-2 (4)
#
############################################################

diag_out() {
   echo "${1}"
}

diag_out "-----------------------------------"
diag_out "STIG Finding ID: V-38534"
diag_out "  Operating system must"
diag_out "  automatically audit account"
diag_out "  modification"
diag_out "-----------------------------------"
