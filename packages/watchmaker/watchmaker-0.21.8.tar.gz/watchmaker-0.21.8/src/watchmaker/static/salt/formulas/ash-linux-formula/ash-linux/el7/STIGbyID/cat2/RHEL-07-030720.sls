# STIG ID:	RHEL-07-030720
# Rule ID:	SV-86791r4_rule
# Vuln ID:	V-72167
# SRG ID:	SRG-OS-000037-GPOS-00015
# Finding Level:	medium
# 
# Rule Summary:
#	All uses of the chsh command must be audited.
#
# CCI-000130 
# CCI-000135 
# CCI-000172 
# CCI-002884 
#    NIST SP 800-53 :: AU-3 
#    NIST SP 800-53A :: AU-3.1 
#    NIST SP 800-53 Revision 4 :: AU-3 
#    NIST SP 800-53 :: AU-3 (1) 
#    NIST SP 800-53A :: AU-3 (1).1 (ii) 
#    NIST SP 800-53 Revision 4 :: AU-3 (1) 
#    NIST SP 800-53 :: AU-12 c 
#    NIST SP 800-53A :: AU-12.1 (iv) 
#    NIST SP 800-53 Revision 4 :: AU-12 c 
#    NIST SP 800-53 Revision 4 :: MA-4 (1) (a) 
#
#################################################################
{%- set stig_id = 'RHEL-07-030720' %}
{%- set helperLoc = 'ash-linux/el7/STIGbyID/cat2/files' %}
{%- set ruleFile = '/etc/audit/rules.d/priv_acts.rules' %}
{%- set sysuserMax = salt['cmd.shell']("awk '/SYS_UID_MAX/{ IDVAL = $2 + 1} END { print IDVAL }' /etc/login.defs") %}
{%- set path2mon = '/usr/bin/chsh' %}
{%- set key2mon = 'privileged-priv_change' %}

script_{{ stig_id }}-describe:
  cmd.script:
    - source: salt://{{ helperLoc }}/{{ stig_id }}.sh
    - cwd: /root

{%- if not salt.file.file_exists(ruleFile) %}
touch_{{ stig_id }}-{{ ruleFile }}:
  file.touch:
    - name: '{{ ruleFile }}'
{%- endif %}

file_{{ stig_id }}-{{ ruleFile }}:
  file.replace:
    - name: '{{ ruleFile }}'
    - pattern: '^-a always,exit -F path={{ path2mon }}.*$'
    - repl: '-a always,exit -F path={{ path2mon }} -F auid>={{ sysuserMax }} -F auid!=4294967295 -k {{ key2mon }}'
    - append_if_not_found: True

