#!/bin/sh
# STIG ID:	RHEL-07-030580
# Rule ID:	SV-86763r4_rule
# Vuln ID:	V-72139
# SRG ID:	SRG-OS-000392-GPOS-00172
# Finding Level:	medium
# 
# Rule Summary:
#	All uses of the chcon command must be audited.
#
# CCI-000172 
# CCI-002884 
#    NIST SP 800-53 :: AU-12 c 
#    NIST SP 800-53A :: AU-12.1 (iv) 
#    NIST SP 800-53 Revision 4 :: AU-12 c 
#    NIST SP 800-53 Revision 4 :: MA-4 (1) (a) 
#
#################################################################
# Standard outputter function
diag_out() {
   echo "${1}"
}

diag_out "----------------------------------------"
diag_out "STIG Finding ID: RHEL-07-030580"
diag_out "   All uses of the chcon command must"
diag_out "   be audited."
diag_out "----------------------------------------"
