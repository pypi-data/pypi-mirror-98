# Finding ID:	RHEL-07-030444
# Version:	RHEL-07-030444_rule
# SRG ID:	SRG-OS-000392-GPOS-00172
# Finding Level:	medium
# 
# Rule Summary:
#	All uses of the restorecon command must be audited.
#
# CCI-000172 
# CCI-002884 
#    NIST SP 800-53 :: AU-12 c 
#    NIST SP 800-53A :: AU-12.1 (iv) 
#    NIST SP 800-53 Revision 4 :: AU-12 c 
#    NIST SP 800-53 Revision 4 :: MA-4 (1) (a) 
#
#################################################################
{%- set stig_id = 'RHEL-07-030444' %}
{%- set helperLoc = 'ash-linux/el7/STIGbyID/cat2/files' %}
{%- set sysuserMax = salt['cmd.shell']("awk '/SYS_UID_MAX/{ IDVAL = $2 + 1} END { print IDVAL }' /etc/login.defs") %}
{%- set path2mon = '/usr/sbin/restorecon' %}
{%- set actKey = 'privileged-priv_change' %}
{%- set audit_cfg_file = '/etc/audit/rules.d/audit.rules' %}
{%- set usertypes = {
    'rootUser': { 'search_string' : ' ' + path2mon + ' -F auid=0 ',
                  'rule' : '-a always,exit -F path=' + path2mon + ' -F auid=0 -k ' + actKey,
                },
    'regUsers': { 'search_string' : ' ' + path2mon + ' -F auid>=' + sysuserMax + ' ',
                  'rule' : '-a always,exit -F path=' + path2mon + ' -F auid>=' + sysuserMax + ' -F auid!=4294967295 -k ' + actKey,
                },
} %}

script_{{ stig_id }}-describe:
  cmd.script:
    - source: salt://{{ helperLoc }}/{{ stig_id }}.sh
    - cwd: /root

# Monitoring of SELinux DAC config
{%- if grains['cpuarch'] == 'x86_64' %}
  {%- for usertype,audit_options in usertypes.items() %}
    {%- if not salt['cmd.shell']('grep -c -E -e "' + audit_options['rule'] + '" ' + audit_cfg_file , output_loglevel='quiet') == '0' %}
file_{{ stig_id }}-auditRules_{{ usertype }}:
  cmd.run:
    - name: 'printf "\nchanged=no comment=''Appropriate audit rule already in place.''\n"'
    - cwd: /root
    - stateful: True
    {%- elif not salt['cmd.shell']('grep -c -E -e "' + audit_options['search_string'] + '" ' + audit_cfg_file , output_loglevel='quiet') == '0' %}
file_{{ stig_id }}-auditRules_{{ usertype }}:
  file.replace:
    - name: '{{ audit_cfg_file }}'
    - pattern: '^.*{{ audit_options['search_string'] }}.*$'
    - repl: '{{ audit_options['rule'] }}'
    {%- else %}
file_{{ stig_id }}-auditRules_{{ usertype }}:
  file.append:
    - name: '{{ audit_cfg_file }}'
    - text: |-
        
        # Monitor for SELinux DAC changes (per STIG-ID {{ stig_id }})
        {{ audit_options['rule'] }}
    {%- endif %}
  {%- endfor %}
{%- else %}
file_{{ stig_id }}-auditRules_selDAC:
  cmd.run:
    - name: 'printf "\nchanged=no comment=''Architecture not supported: no changes made.''\n"'
    - cwd: /root
    - stateful: True
{%- endif %}
