# Finding ID:	RHEL-07-020010
# Version:	RHEL-07-020010_rule
# SRG ID:	SRG-OS-000095-GPOS-00049
# Finding Level:	high
# 
# Rule Summary:
#	The ypserv package must not be installed.
#
# CCI-000381 
#    NIST SP 800-53 :: CM-7 
#    NIST SP 800-53A :: CM-7.1 (ii) 
#    NIST SP 800-53 Revision 4 :: CM-7 a 
#
#################################################################
{%- set stig_id = 'RHEL-07-020010' %}
{%- set helperLoc = 'ash-linux/el7/STIGbyID/cat1/files' %}

script_{{ stig_id }}-describe:
  cmd.script:
    - source: salt://{{ helperLoc }}/{{ stig_id }}.sh
    - cwd: /root

package_{{ stig_id }}-nuke:
  pkg.removed:
    - name: 'ypserv'

