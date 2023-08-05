# STIG ID:	RHEL-07-010200
# Rule ID:	SV-86543r3_rule
# Vuln ID:	V-71919
# SRG ID:	SRG-OS-000073-GPOS-00041
# Finding Level:	medium
# 
# Rule Summary:
#	The PAM system service must be configured to store only
#	encrypted representations of passwords.
#
# CCI-000196 
#    NIST SP 800-53 :: IA-5 (1) (c) 
#    NIST SP 800-53A :: IA-5 (1).1 (v) 
#    NIST SP 800-53 Revision 4 :: IA-5 (1) (c) 
#
#################################################################
{%- set stig_id = 'RHEL-07-010200' %}
{%- set helperLoc = 'ash-linux/el7/STIGbyID/cat2/files' %}
{%- set targFile = '/etc/pam.d/system-auth' %}
{%- if salt.file.is_link(targFile) %}
  {%- set targFile = targFile + '-ac' %}
{%- endif %}
{%- set searchRoot = '^password\s+sufficient\s+pam_unix.so\s+' %}

script_{{ stig_id }}-describe:
  cmd.script:
    - source: salt://{{ helperLoc }}/{{ stig_id }}.sh
    - cwd: /root

{%- if salt.file.search(targFile, searchRoot + '.*sha512') %}
file_{{ stig_id }}-{{ targFile }}:
  cmd.run:
    - name: 'printf "\nchanged=no comment=''Found target config in {{ targFile }}.''\n"'
    - cwd: /root
    - stateful: True
{%- elif salt.file.search(targFile, searchRoot) %}
file_{{ stig_id }}-{{ targFile }}:
  file.replace:
    - name: {{ targFile }}
    - pattern: '^(?P<srctok>{{ searchRoot }}.*$)'
    - repl: '\g<srctok> sha512'
file_{{ stig_id }}-{{ targFile }}-cleanup:
  file.replace:
    - name: {{ targFile }}
    - pattern: '(md5|bigcrypt|sha256|blowfish) '
    - repl: ''
    - onchanges:
      - file: file_{{ stig_id }}-{{ targFile }}
{%- else %}
file_{{ stig_id }}-{{ targFile }}:
  file.replace:
    - name: {{ targFile }}
    - pattern: '^(?P<srctok>^password\s+requisite\s+pam_pwquality.so.*)'
    - repl: '\g<srctok>\npassword sufficient pam_unix.so sha512'
{%- endif %}

