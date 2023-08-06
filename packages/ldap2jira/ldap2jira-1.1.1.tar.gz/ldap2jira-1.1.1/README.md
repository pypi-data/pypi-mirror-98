# python-ldap2jira

Set of utilities for finding jira accounts with LDAP check and optional file map.

[![Test](https://github.com/RedHat-Eng-PGM/python-ldap2jira/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/RedHat-Eng-PGM/python-ldap2jira/actions/workflows/test.yml)
[![Coverage](https://codecov.io/gh/RedHat-Eng-PGM/python-ldap2jira/branch/master/graph/badge.svg?token=WCXC71LMUA)](https://codecov.io/gh/RedHat-Eng-PGM/python-ldap2jira)
[![Pypi Upload](https://github.com/RedHat-Eng-PGM/python-ldap2jira/actions/workflows/pypi-upload.yml/badge.svg)](https://github.com/RedHat-Eng-PGM/python-ldap2jira/actions/workflows/pypi-upload.yml)
[![Pypi Version](https://img.shields.io/pypi/v/ldap2jira.svg)](https://pypi.org/project/ldap2jira/)
[![Documentation Status](https://readthedocs.org/projects/python-ldap2jira/badge/?version=latest)](https://python-ldap2jira.readthedocs.io/en/latest/?badge=latest)

## Pypi Package
https://pypi.org/project/ldap2jira/

## Docs
https://python-ldap2jira.readthedocs.io/

## Usage
Install package from pypi

    pip install ldap2jira

In python

    from ldap2jira import LDAP2JiraUserMap
    
    l2j = LDAP2JiraUserMap(
        jira_url='https://yourjiraserver',
        jira_user='yourjirauser',
        jira_password='yourpassword',
        ldap_url='ldap://yourldapserver,
        ldap_base='ou=users,dc=your,dc=base',
        ldap_query_fields_username=['uid'],
        ldap_fields_username=['uid'],
        ldap_fields_mail=['mail'],
        ldap_fields_name=['cn'],
        ldap_fields_jira_search=[
            'mail', 'uid', 'cn'],
        email_domain='yourdomain.org'
    )
    
    l2j.find_jira_accounts(['usertofind', 'user2tofind'])
