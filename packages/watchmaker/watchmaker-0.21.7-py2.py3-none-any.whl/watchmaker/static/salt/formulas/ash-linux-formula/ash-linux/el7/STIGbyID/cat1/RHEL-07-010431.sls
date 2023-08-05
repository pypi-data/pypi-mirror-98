# Finding ID:	RHEL-07-010431
# Version:	RHEL-07-010431_rule
# SRG ID:	SRG-OS-000480-GPOS-00229
# Finding Level:	high
# 
# Rule Summary:
#	The operating system must not allow guest logon to the system.
#
# CCI-000366 
#    NIST SP 800-53 :: CM-6 b 
#    NIST SP 800-53A :: CM-6.1 (iv) 
#    NIST SP 800-53 Revision 4 :: CM-6 b 
#
#################################################################
{%- set stig_id = 'RHEL-07-010431' %}
{%- set helperLoc = 'ash-linux/el7/STIGbyID/cat1/files' %}
{%- set checkFile = '/etc/gdm/custom.conf'%}
{%- set checkParm = 'TimedLoginEnable'%}

script_{{ stig_id }}-describe:
  cmd.script:
    - source: salt://{{ helperLoc }}/{{ stig_id }}.sh
    - cwd: /root

{%- if not salt.pkg.version('gdm') %}
eval_{{ stig_id }}:
  cmd.run:
    - name: 'printf "\nchanged=no comment=''GDM susbsystem is not installed.''\n"'
    - cwd: /root
    - stateful: True
{% elif salt.file.search(checkFile, '^' + checkParm) %}
file_{{ stig_id }}:
  file.replace:
    - name: {{ checkFile }}
    - pattern: '^{{ checkParm }}.*$'
    - repl: '{{ checkParm }}=false'
{%- else %}
file_{{ stig_id }}:
  file.replace:
    - name: {{ checkFile }}
    - pattern: '^\[daemon]'
    - repl: '[daemon]\n{{ checkParm }}=false'
{%- endif %}
