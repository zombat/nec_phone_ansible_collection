#!/usr/bin/python

# Copyright: (c) 2022, Raymond Rizzo <ray@raymondrizzo.com>
#  MIT license (see COPYING or https://opensource.org/licenses/MIT)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: set_factoryvalues

short_description: This module sets pc port settings on a NEC phone.

version_added: "0.0.3"

description: This module sets pc port settings on a NEC-SIP IP phone.

options:
    eapol_forwarding:
        description: This option enables or disables EAPOL forwarding on the PC port.
        required: false
        type: bool
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
    port_available:
        description: This option sets the PC port to available.
        required: false
        type: bool
    port_security:
        description: This option sets PC port security.
        required: false
        type: bool
    port_speed:
        description: This option sets the LAN port speed and duplex on the phone (auto, 10half, 10full, 100half, 100full).
        required: false
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
    vlan_id:
        description: This option sets the VLAN ID on the LAN port.
        required: false
        type: int
    vlan_mode:
        description: This option sets the VLAN mode on the LAN port.
        required: false
        type: bool
    vlan_priority:
        description: This option sets the VLAN priority on the LAN port (0-7).
        required: false
        type: int
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
        eapol_forwarding=dict(type='bool', required=False),
        force_http=dict(type='bool', required=False, Default=False),
        host=dict(type='str', required=True),
        keep_session=dict(type='bool', required=False, Default=False),
        password=dict(type='str', required=False, Default='6633222', no_log=True),
        port_available=dict(type='bool', required=False),
        port_security=dict(type='bool', required=False),
        port_speed=dict(type='str', required=False, choices=['auto', '10half', '10full', '100half', '100full']),
        session_id=dict(type='str', required=False),
        username=dict(type='str', required=False, Default='admin', no_log=True),
        verify_certs=dict(type='bool', required=False, Default=False),
        vlan_id=dict(type='int', required=False),
        vlan_mode=dict(type='bool', required=False),
        vlan_priority=dict(type='int', required=False, choices=[0, 1, 2, 3, 4, 5, 6, 7])
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
    eapol_forwarding = module.params['eapol_forwarding']
    forceHttp = module.params['force_http']
    hostName = module.params['host']
    keepSession = module.params['keep_session']
    password = module.params['password']
    portAvailable = module.params['port_available']
    portSecurity = module.params['port_security']
    portSpeed = module.params['port_speed']
    sessionId = module.params['session_id']
    userName = module.params['username']
    verifyCerts = module.params['verify_certs']
    vlanId = module.params['vlan_id']
    vlanMode = module.params['vlan_mode']
    vlanPriority = module.params['vlan_priority']

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
        # Set EAPOL forwarding
        if eapol_forwarding is not None:
            if eapol_forwarding == True:
                eapolForwarding = '1'
            else:
                eapolForwarding = '0'
            setEapolForwardingResponse = setSingleItem(hostName, sessionId, '41e0456', eapol_forwarding, False, verifyCerts, False)
            if setEapolForwardingResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set EAPOL forwarding')
            else:
                result['changed'] = True
                result['message'].append('EAPOL forwarding set to ' + eapolForwarding)
        # Set port available    
        if portAvailable is not None:
            if portAvailable == False:
                portAvailable = '1'
            else:
                portAvailable = '0'
            setPortAvailableResponse = setSingleItem(hostName, sessionId, '41e0455', portAvailable, False, verifyCerts, False)
            if setPortAvailableResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set port available')
            else:
                result['changed'] = True
                result['message'].append('Port available set to ' + portAvailable)
        # Set port security
        if portSecurity is not None:
            if portSecurity == True:
                portSecurity = '1'
            else:
                portSecurity = '0'
            setPortSecurityResponse = setSingleItem(hostName, sessionId, '41e0415', portSecurity, False, verifyCerts, False)
            if setPortSecurityResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Failed to set port security')
            else:
                result['changed'] = True
                result['message'].append('Port security set to ' + portSecurity)
        # Set port speed
        if portSpeed:
            if portSpeed == '10half':
                portSpeed = '4'
            elif portSpeed == '10full':
                portSpeed = '3'
            elif portSpeed == '100half':
                portSpeed = '2'
            elif portSpeed == '100full':
                portSpeed = '1'
            else:
                portSpeed = '0'
            portSpeedResponse = setSingleItem(hostName, sessionId, '41e0451', portSpeed, False, verifyCerts, False)
            if portSpeedResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Port speed not set')
            else:
                result['failed'] = False
                result['message'].append('Port speed set to ' + portSpeed)
        # Set VLAN ID
        if vlanId:
            vlanId = str(vlanId)
            vlanIdResponse = setSingleItem(hostName, sessionId, '41e0453', vlanId, False, verifyCerts, False)
            if vlanIdResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('VLAN ID not set')
            else:
                result['failed'] = False
                result['message'].append('VLAN ID set to ' + vlanId)
        # Set VLAN mode
        if vlanMode is not None:
            if vlanMode == True:
                vlanMode = '1'
            else:
                vlanMode = '0'
            vlanModeResponse = setSingleItem(hostName, sessionId, '41e0452', vlanMode, False, verifyCerts, False)
            if vlanModeResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('VLAN mode not set')
            else:
                result['failed'] = False
                result['message'].append('VLAN mode set to ' + vlanMode)
        # Set VLAN priority
        if vlanPriority:
            vlanPriority = str(vlanPriority)
            vlanPriorityResponse = setSingleItem(hostName, sessionId, '41e0454', vlanPriority, False, verifyCerts, False)
            if vlanPriorityResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('VLAN priority not set')
            else:
                result['failed'] = False
                result['message'].append('VLAN priority set to ' + vlanPriority)
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