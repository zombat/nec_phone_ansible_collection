#!/usr/bin/python

# Copyright: (c) 2022, Raymond Rizzo <ray@raymondrizzo.com>
#  MIT license (see COPYING or https://opensource.org/licenses/MIT)
from __future__ import (absolute_import, division, print_function)
from random import choices
__metaclass__ = type

DOCUMENTATION = r'''
---
module: set_factoryvalues

short_description: This module sets pc port settings on a NEC phone.

version_added: "0.0.4"

description: This module sets pc port settings on a NEC-SIP IP phone.

options:
    encryption_auth_mode:
        description: Enable or disable encryption mode.
        required: false
        type: bool
    encryption_otp:
        description: Set encryption OTP.
        required: false
        type: str
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
    sip_user_id:
        description: SIP user ID to set.
        required: false
        type: str
    sip_password:
        description: SIP password to set.
        required: false
        type: str
    sip_extension:
        description: SIP extension to set.
        required: false
        type: str
    sip_backup_login:
        description: Enable/disable SIP backup login.
        required: false
        type: bool
    sip_server_one:
        description: SIP server one to set.
        required: false
        type: str
    sip_server_two:
        description: SIP server two to set.
        required: false
        type: str
    sip_server_three:
        description: SIP server three to set.
        required: false
        type: str
    sip_server_four:
        description: SIP server four to set.
        required: false
        type: str
    sip_access_mode:
        description: SIP access mode to set.
        required: false
        type: str
    sip_server_one_port:
        description: SIP server one port to set.
        required: false
        type: str
    sip_server_two_port:
        description: SIP server two port to set.
        required: false
        type: str
    sip_server_three_port:
        description: SIP server three port to set.
        required: false
        type: str
    sip_server_four_port:
        description: SIP server four port to set.
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
    - name: Set PC Port settings
      community.necsipphonetool.set_pc_port:
        username: 'ADMIN'
        password: '6633222'
        host: "10.4.0.4"      
        force_http: True
        session_id: '{{ result.session_id }}'
        eapol_forwarding: False
        port_speed: "10half"
        port_availability: False
        port_security: False
        vlan_id: 222
        vlan_mode: False
        vlan_priority: 2
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
changed:
    description: True if the module itself made any changes
    type: bool
    returned: always
    sample: 'True/False'
failed:
    description: True if the module failed
    type: bool
    returned: always
    sample: 'True/False'
message:
    description: The output messages that the module generates.
    type: list
    returned: always
    sample: '["Message 1", "Message 2"]'
session_id:
    description: The session ID used for API calls.
    type: str
    returned: if keep_session is true
'''

from ansible.module_utils.basic import AnsibleModule
# import module snippets from community.necsipphonetool
from ansible_collections.community.necsipphonetool.plugins.module_utils.nec_phone_tool import *

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        encryption_auth_mode=dict(type='bool', required=False),
        encryption_otp=dict(type='str', required=False),
        force_http=dict(type='bool', required=False, Default=False),
        host=dict(type='str', required=True),
        keep_session=dict(type='bool', required=False, Default=False),
        password=dict(type='str', required=False, Default='6633222', no_log=True),
        session_id=dict(type='str', required=False),
        sip_user_id=dict(type='str', required=False),
        sip_password=dict(type='str', required=False, no_log=True),
        sip_extension=dict(type='str', required=False),
        sip_backup_login=dict(type='bool', required=False),
        sip_server_one=dict(type='str', required=False),
        sip_server_two=dict(type='str', required=False),
        sip_server_three=dict(type='str', required=False),
        sip_server_four=dict(type='str', required=False),
        sip_access_mode=dict(type='str', required=False, choices=['normal', 'remote']),
        sip_server_one_port=dict(type='str', required=False),
        sip_server_two_port=dict(type='str', required=False),
        sip_server_three_port=dict(type='str', required=False),
        sip_server_four_port=dict(type='str', required=False),
        username=dict(type='str', required=False, Default='admin', no_log=True),
        verify_certs=dict(type='bool', required=False, Default=False),
    )

    result = dict(
        changed=False,
        failed=True,
        original_message = '',
        message = []
        )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    result['original_message'] = module.params['host']
    
    # Set variables from module arguments
    encryption_auth_mode = module.params['encryption_auth_mode']
    encryption_otp = module.params['encryption_otp']
    forceHttp = module.params['force_http']
    hostName = module.params['host']
    keepSession = module.params['keep_session']
    password = module.params['password']
    sessionId = module.params['session_id']
    sipUserId = module.params['sip_user_id']
    sipPassword = module.params['sip_password']
    sipExtension = module.params['sip_extension']
    sipBackupLogin = module.params['sip_backup_login']
    sipServerOne = module.params['sip_server_one']
    sipServerTwo = module.params['sip_server_two']
    sipServerThree = module.params['sip_server_three']
    sipServerFour = module.params['sip_server_four']
    sipAccessMode = module.params['sip_access_mode']
    sipServerOnePort = module.params['sip_server_one_port']
    sipServerTwoPort = module.params['sip_server_two_port']
    sipServerThreePort = module.params['sip_server_three_port']
    sipServerFourPort = module.params['sip_server_four_port']
    userName = module.params['username']
    verifyCerts = module.params['verify_certs']

    if forceHttp:
        hostName = 'http://' + hostName
    else:
        hostName = 'https://' + hostName

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
        # Set encryption auth mode
        if encryption_auth_mode is not None:
            if encryptionAuthMode == True:
                encryptionAuthMode = '1'
            else:
                encryptionAuthMode = '0'
            encryptionAuthModeResponse = setSingleItem(hostName, sessionId, '40d0427', encryptionAuthMode, False, verifyCerts, False)
            if encryptionAuthModeResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set encryption auth mode')
            else:
                result['failed'] = False
                result['message'].append('Encryption auth mode set successfully')
        # Set encryption OTP
        if encryption_otp:
            encryptionOtpResponse = setSingleItem(hostName, sessionId, '40d0428', encryption_otp, False, verifyCerts, False)
            if encryptionOtpResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set encryption OTP')
            else:
                result['failed'] = False
                result['message'].append('Encryption OTP set successfully')
        # Set SIP user ID
        if sipUserId:
            sipUserIdResponse = setSingleItem(hostName, sessionId, '40a0418', sipUserId, False, verifyCerts, False)
            if sipUserIdResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set SIP user ID')
            else:
                result['failed'] = False
                result['message'].append('SIP user ID set successfully')
        # Set SIP password
        if sipPassword:
            sipPasswordResponse = setSingleItem(hostName, sessionId, '40a0419', sipPassword, False, verifyCerts, False)
            if sipPasswordResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set SIP password')
            else:
                result['failed'] = False
                result['message'].append('SIP password set successfully')
        # Set SIP extension
        if sipExtension:
            sipExtensionResponse = setSingleItem(hostName, sessionId, '40a041a', sipExtension, False, verifyCerts, False)
            if sipExtensionResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set SIP extension')
            else:
                result['failed'] = False
                result['message'].append('SIP extension set successfully')
        # Set SIP backup login
        if sipBackupLogin is not None:
            if sipBackupLogin == True:
                sipBackupLogin = '1'
            else:
                sipBackupLogin = '0'
            sipBackupLoginResponse = setSingleItem(hostName, sessionId, '40a04ca', sipBackupLogin, False, verifyCerts, False)
            if sipBackupLoginResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set SIP backup login')
            else:
                result['failed'] = False
                result['message'].append('SIP backup login set successfully')
        # Set SIP server one
        if sipServerOne:
            sipServerOneResponse = setTwoParameters(hostName, sessionId, '40b041b', sipServerOne, 'type', 'ip', False, verifyCerts, False)
            if sipServerOneResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set SIP server one')
            else:
                result['failed'] = False
                result['message'].append('SIP server one set successfully')
        # Set SIP server two
        if sipServerTwo:
            sipServerTwoResponse = setTwoParameters(hostName, sessionId, '40b041c', sipServerTwo, 'type', 'ip', False, verifyCerts, False)
            if sipServerTwoResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set SIP server two')
            else:
                result['failed'] = False
                result['message'].append('SIP server two set successfully')
        # Set SIP server three
        if sipServerThree:
            sipServerThreeResponse = setTwoParameters(hostName, sessionId, '40b041d', sipServerThree, 'type', 'ip', False, verifyCerts, False)
            if sipServerThreeResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set SIP server three')
            else:
                result['failed'] = False
                result['message'].append('SIP server three set successfully')
        # Set SIP server four
        if sipServerFour:
            sipServerFourResponse = setTwoParameters(hostName, sessionId, '40b041e', sipServerFour, 'type', 'ip', False, verifyCerts, False)
            if sipServerFourResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set SIP server four')
            else:
                result['failed'] = False
                result['message'].append('SIP server four set successfully')
        # Set SIP server one port
        if sipServerOnePort:
            sipServerOnePortResponse = setTwoParameters(hostName, sessionId, '40c0423', sipServerOnePort, 'port', 'int', False, verifyCerts, False)
            if sipServerOnePortResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set SIP server one port')
            else:
                result['failed'] = False
                result['message'].append('SIP server one port set successfully')
        # Set SIP server two port
        if sipServerTwoPort:
            sipServerTwoPortResponse = setTwoParameters(hostName, sessionId, '40b041c', sipServerTwoPort, 'port', 'int', False, verifyCerts, False)
            if sipServerTwoPortResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set SIP server two port')
            else:
                result['failed'] = False
                result['message'].append('SIP server two port set successfully')
        # Set SIP server three port
        if sipServerThreePort:
            sipServerThreePortResponse = setTwoParameters(hostName, sessionId, '40b041d', sipServerThreePort, 'port', 'int', False, verifyCerts, False)
            if sipServerThreePortResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set SIP server three port')
            else:
                result['failed'] = False
                result['message'].append('SIP server three port set successfully')
        # Set SIP server four port
        if sipServerFourPort:
            sipServerFourPortResponse = setTwoParameters(hostName, sessionId, '40b041e', sipServerFourPort, 'port', 'int', False, verifyCerts, False)
            if sipServerFourPortResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set SIP server four port')
            else:
                result['failed'] = False
                result['message'].append('SIP server four port set successfully')
        # Set SIP access mode
        if sipAccessMode:
            if sipAccessMode == 'normal':
                sipAccessMode = '0'
            elif sipAccessMode == 'remote':
                sipAccessMode = '1'
            sipAccessModeResponse = setSingleItem(hostName, sessionId, '4030406', sipAccessMode, False, verifyCerts, False)
            if sipAccessModeResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set SIP access mode')
            else:
                result['failed'] = False
                result['message'].append('SIP access mode set successfully')
        if not keepSession:
            # Log off phone and reboot
            logOffResponse = logOffPhone(hostName, sessionId, False, verifyCerts, False)
            if logOffResponse.status_code != 200:
                result['failed'] = True
        else:
            result['session_id'] = sessionId
        result['changed'] = True
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()