#!/bin/sh
#
# STIG URL: http://www.stigviewer.com/stig/red_hat_enterprise_linux_6/2014-06-11/finding/V-38576
# Finding ID:	V-38576
# Version:	RHEL-06-000063
# Finding Level:	Medium
#
#     The system must use a FIPS 140-2 approved cryptographic hashing 
#     algorithm for generating account password hashes (login.defs). Using 
#     a stronger hashing algorithm makes password cracking attacks more 
#     difficult.
#
############################################################

diag_out() {
   echo "${1}"
}

diag_out "----------------------------------"
diag_out "STIG Finding ID: V-38576"
diag_out "  The system login.defs must be"
diag_out "  configured to use the SHA512"
diag_out "  encryption algorithm for all"
diag_out "  locally-managed user accounts"
diag_out "----------------------------------"
