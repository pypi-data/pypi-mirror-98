# STIG ID:	RHEL-07-010340
# Rule ID:	SV-86571r3_rule
# Vuln ID:	V-71947
# SRG ID:	SRG-OS-000373-GPOS-00156
# Finding Level:	medium
# 
# Rule Summary:
#	Users must provide a password for privilege escalation.
#
# CCI-002038 
#    NIST SP 800-53 Revision 4 :: IA-11 
#
#################################################################
{%- set stig_id = 'RHEL-07-010340' %}
{%- set helperLoc = 'ash-linux/el7/STIGbyID/cat2/files' %}
{%- set sudoerFiles = [ '/etc/sudoers' ] %}
{%- set sudoerFiles = sudoerFiles + salt.file.find('/etc/sudoers.d', maxdepth='0', type='f') %}

script_{{ stig_id }}-describe:
  cmd.script:
    - source: salt://{{ helperLoc }}/{{ stig_id }}.sh
    - cwd: /root

{%- for sudoer in sudoerFiles %}
  {%- if salt.file.search(sudoer, '^[a-zA-Z%@].*NOPASSWD') %}
notify_{{ stig_id}}-{{ sudoer }}:
  cmd.run:
    - name: 'printf "[WARNING]:\tThe {{ sudoer }} file contains an active ''NOPASSWD''\n\t\tentry. Sites using only key-based logins should ignore this warning.\n" > /dev/stderr'
    - cwd: /root
  {%- endif %}
{%- endfor %}
