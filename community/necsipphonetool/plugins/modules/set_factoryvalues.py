#!/usr/bin/python

# Copyright: (c) 2022, Raymond Rizzo <ray@raymondrizzo.com>
#  MIT license (see COPYING or https://opensource.org/licenses/MIT)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: set_factoryvalues

short_description: This module sets the factory values on a NEC phone.

version_added: "0.0.1"

description: This module sets the factory values on a NEC-SIP IP phone.

options:
    force_http:
        description: This option forces the use of HTTP instead of HTTPS.
        required: false
        type: bool
    host:
        description: IPv4 or hostname of phone.
        required: true
        type: str
    keep_session:
        description: This option keeps the session open after setting options. A logout or hard reset will be required at the end of your playbook.
        required: false
        type: bool
    password:
        description: Password to log into phone.
        required: true
        type: str
    session_id:
        description: Logon session ID to use for API calls. If not provided, a new logon session will be created.
        required: false
        type: str
    username:
        description: Username to log into phone.
        required: true
        type: str
    verify_certs:
        description: This option verifies the SSL certificate on the phone.
        required: false
        type: bool
author:
    - Raymond Rizzo (@zombat)
'''

EXAMPLES = r'''
# Set factory values, save, and reboot.
- name: Set factory values on phone and reboot it
  community.necsipphonetool.set_factoryvalues:
    hostAddress: "{{ inventory_hostname }}"
    logOnName: "{{ logOnName }}"
    logOnPassword: "{{ logOnPassword }}"
    verifyCerts: "{{ verifyCerts }}"   
'''

# RETURN = r'''
# # These are examples of possible return values, and in general should use other names for return values.
# changed:
#     description: True if the module itself made any changes
#     type: bool
#     returned: always
#     sample: 'True/False'
# failed:
#     description: True if the module failed
#     type: bool
#     returned: always
#     sample: 'True/False'
# message:
#     description: The output message that the test module generates.
#     type: str
#     returned: always
#     sample: 'Phone reset to factory defaults.'
# session_id:
#     description: The session ID used for API calls.
#     type: str
#     returned: if keep_session is true
# '''

from ansible.module_utils.basic import AnsibleModule
# import module snippets from community.necsipphonetool
from ansible_collections.community.necsipphonetool.plugins.module_utils.nec_phone_tool import *
import re

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        force_http=dict(type='bool', required=False, Default=False),
        host=dict(type='str', required=True),
        keep_session=dict(type='bool', required=False, Default=False),
        password=dict(type='str', required=False, Default='6633222', no_log=True),
        session_id=dict(type='str', required=False),
        username=dict(type='str', required=False, Default='admin', no_log=True),
        verify_certs=dict(type='bool', required=False, Default=False),
    )


    result = dict(
        changed=False,
        failed=True,
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    result['original_message'] = module.params['host']
    result['message'] = 'goodbye'

    # Set variables from module arguments
    forceHttp = module.params['force_http']
    hostName = module.params['host']
    keepSession = module.params['keep_session']
    password = module.params['password']
    sessionId = module.params['session_id']
    userName = module.params['username']
    verifyCerts = module.params['verify_certs']

    if forceHttp:
        hostName = 'http://' + hostName
    else:
        hostName = 'https://' + hostName

    result = dict(
        changed = False,
        original_message = '',
        message = 'Nothing done...'
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    if not sessionId:
        logonResponse, sessionId = logOnPhone(hostName, userName, password, True, verifyCerts, False)
        if logonResponse.status_code != 200 or not sessionId:
            result['failed'] = True
        else:
             result['failed'] = False
    if sessionId:        
        # Clear configuration on phone
        clearConfigResponse = passSingleParameter(hostName, sessionId, 'data_clear', '4110430', '0', verifyCerts, False)
        result['clearConfigResponse'] = clearConfigResponse.text
        if clearConfigResponse.status_code != 200: # or re.search('error', clearConfigResponse.text, re.IGNORECASE):
            result['failed'] = True
        else:
             result['failed'] = False
        if not keepSession:
            # Hard reset phone
            hardResetResponse = passSingleParameter(hostName, sessionId, 'hard_reset', '4040408', '0', verifyCerts, False)
            if hardResetResponse.status_code != 200:
                result['failed'] = True
        else:
            result['session_id'] = sessionId
        result['changed'] = True
        result['message'] = 'Phone reset to factory defaults.'

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()