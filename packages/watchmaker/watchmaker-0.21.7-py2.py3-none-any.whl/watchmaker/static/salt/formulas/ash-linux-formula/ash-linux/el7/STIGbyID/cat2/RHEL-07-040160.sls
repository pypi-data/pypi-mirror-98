# Finding ID:	RHEL-07-040160
# Version:	RHEL-07-040160_rule
# SRG ID:	SRG-OS-000163-GPOS-00072
# Finding Level:	medium
# 
# Rule Summary:
#	All network connections associated with a communication
#	session must be terminated at the end of the session or after
#	10 minutes of inactivity from the user at a command prompt,
#	except to fulfill documented and validated mission
#	requirements.
#
# CCI-001133 
# CCI-002361 
#    NIST SP 800-53 :: SC-10 
#    NIST SP 800-53A :: SC-10.1 (ii) 
#    NIST SP 800-53 Revision 4 :: SC-10 
#    NIST SP 800-53 Revision 4 :: AC-12 
#
#################################################################
{%- set stig_id = 'RHEL-07-040160' %}
{%- set helperLoc = 'ash-linux/el7/STIGbyID/cat2/files' %}
{%- set cfgFile = '/etc/profile' %}
{%- set parmName = 'TMOUT' %}
{%- set parmValu = '600' %}

script_{{ stig_id }}-describe:
  cmd.script:
    - source: salt://{{ helperLoc }}/{{ stig_id }}.sh
    - cwd: /root

file_{{ stig_id }}-{{ cfgFile }}:
  file.replace:
    - name: '{{ cfgFile }}'
    - pattern: '^\s{{ parmName }}=.*$'
    - repl: 'readonly {{ parmName }}={{ parmValu }}'
    - append_if_not_found: True
    - not_found_content: |-
        # Inserted per STIG {{ stig_id }}
        readonly {{ parmName }}={{ parmValu }}
 
