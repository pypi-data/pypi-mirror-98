# Finding ID:	RHEL-07-020690
# Version:	RHEL-07-020690_rule
# SRG ID:	SRG-OS-000480-GPOS-00227
# Finding Level:	medium
# 
# Rule Summary:
#	All files and directories contained in local interactive user
#	home directories must be group-owned by a group of which the
#	home directory owner is a member.
#
# CCI-000366 
#    NIST SP 800-53 :: CM-6 b 
#    NIST SP 800-53A :: CM-6.1 (iv) 
#    NIST SP 800-53 Revision 4 :: CM-6 b 
#
#################################################################
{%- set stig_id = 'RHEL-07-020690' %}
{%- set helperLoc = 'ash-linux/el7/STIGbyID/cat2/files' %}
{%- set sysuserMax = salt['cmd.shell']("awk '/SYS_UID_MAX/{ IDVAL = $2 + 1} END { print IDVAL }' /etc/login.defs")|int %}
{%- set userList = salt.user.list_users() %}
{%- set iShells = [
                   '/bin/sh',
                   '/bin/bash',
                   '/bin/csh',
                   '/bin/ksh',
                   '/bin/mksh',
                   '/bin/tcsh',
                   '/bin/zsh',
                   '/usr/bin/sh',
                   '/usr/bin/bash',
                   '/usr/bin/csh',
                   '/usr/bin/ksh',
                   '/usr/bin/mksh',
                   '/usr/bin/tcsh',
                   '/usr/bin/zsh'
                    ] %}


script_{{ stig_id }}-describe:
  cmd.script:
    - source: salt://{{ helperLoc }}/{{ stig_id }}.sh
    - cwd: /root

# Iterate local user-list
{%- for user in userList %}
  {%- set uinfo = salt.user.info(user) %}
  # Regular interactive-users will have UID > SYS_USER_MAX and
  # will have an interactive shell assigned.
  {%- if ( uinfo['uid'] > sysuserMax ) and
         ( uinfo['shell'] in iShells ) %}
    {%- set uGrpLst = uinfo['groups']|join(', ') %}
    {%- set findstr = '-group ' + uGrpLst.replace(',', ' -o -group') %}
    {%- set uhome = uinfo['home'] %}
    {%- set ugid = uinfo['gid'] %}
    {%- set foundFiles = salt['cmd.shell']('find ' + uhome + ' -type f ! \( ' + findstr + ' \)').split('\n') %}
    {%- set foundDirs = salt['cmd.shell']('find ' + uhome + ' -type d ! \( ' + findstr + ' \)').split('\n') %}
    {% for elem in foundFiles %}
      {% if elem %}
file_{{ stig_id }}-{{ elem }}:
  file.managed:
    - name: '{{ elem }}'
    - group: {{ ugid }}
      {% endif %}
    {% endfor %}
    {% for elem in foundDirs %}
      {% if elem %}
file_{{ stig_id }}-{{ elem }}:
  file.directory:
    - name: '{{ elem }}'
    - group: {{ ugid }}
      {% endif %}
    {% endfor %}
  {%- endif %}
{%- endfor %}
