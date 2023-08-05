# Finding ID:	RHEL-07-040070
# Version:	RHEL-07-040070_rule
# SRG ID:	SRG-OS-000068-GPOS-00036
# Finding Level:	medium
#
# Rule Summary:
#	The cn_map file must be owned by root.
#
# CCI-000187
#    NIST SP 800-53 :: IA-5 (2)
#    NIST SP 800-53A :: IA-5 (2).1
#    NIST SP 800-53 Revision 4 :: IA-5 (2) (c)
#
#################################################################
{%- set stig_id = 'RHEL-07-040070' %}
{%- set helperLoc = 'ash-linux/el7/STIGbyID/cat2/files' %}
{%- set pkgChk = 'pam_pkcs11' %}
{%- set cfgFile = '/etc/pam_pkcs11/cn_map' %}

script_{{ stig_id }}-describe:
  cmd.script:
    - source: salt://{{ helperLoc }}/{{ stig_id }}.sh
    - cwd: /root

touch_{{ stig_id }}-{{ cfgFile }}:
  file.touch:
    - name: '{{ cfgFile }}'
    - unless: ' test -e {{ cfgFile }}'

mode_{{ stig_id }}-{{ cfgFile }}:
  file.managed:
    - name: '{{ cfgFile }}'
    - owner: 'root'
    - replace: False
    - require:
      - file: 'touch_{{ stig_id }}-{{ cfgFile }}'
