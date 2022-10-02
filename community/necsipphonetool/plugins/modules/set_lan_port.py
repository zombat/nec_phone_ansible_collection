#!/usr/bin/python

# Copyright: (c) 2022, Raymond Rizzo <ray@raymondrizzo.com>
#  MIT license (see COPYING or https://opensource.org/licenses/MIT)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: set_lan_port

short_description: This module sets the LAN values on a NEC phone.

version_added: "0.0.2"

description: This module sets the LAN values on a NEC-SIP IP phone.

options:
    default_gateway:
        description: The default gateway for the phone.
        required: false
        type: str
    dhcp_mode:
        description: This is the DHCP mode for the phone.
        required: false
        type: bool
    dns_address:
        description: This is the DNS address for the phone.
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
    ip_address:
        description: This is the IP address for the phone.
        required: false
        type: str
    keep_session:
        description: This option keeps the session open after setting options. A logout or hard reset will be required at the end of your playbook.
        required: false
        type: bool
    lldp_mode:
        description: This option sets the LLDP mode on the phone.
        required: false
        type: bool
    password:
        description: Password to log into phone.
        required: true
        type: str
    port_speed:
        description: This option sets the LAN port speed and duplex on the phone (auto, 10half, 10full, 100half, 100full).
        required: false
        type: str
    session_id:
        description: Logon session ID to use for API calls. If not provided, a new logon session will be created.
        required: false
        type: str
    spare_default_gateway:
        description: The spare default gateway for the phone.
        required: false
        type: str
    spare_dns_address:
        description: This is the spare DNS address for the phone.
        required: false
        type: str
    spare_ip_address_mode:
        description: This option sets the spare IP address mode on the phone (spare, backup, disable).
        required: false
        type: bool
    spare_ip_address:
        description: This is the spare IP address for the phone.
        required: false
        type: str
    spare_subnet_mask:
        description: This is the spare subnet mask for the phone.
        required: false
        type: str
    subnet_mask:
        description: This is the subnet mask for the phone.
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
- name: Set LAN settings
      community.necsipphonetool.set_lan_port:
        username: 'ADMIN'
        password: '6633222'
        host: "10.4.0.4"      
        force_http: True
        session_id: '{{ result.session_id }}'
        default_gateway: "192.168.1.1"
        dhcp_mode: False
        dns_address: "192.168.1.1"
        lldp_mode: False
        ip_address: "192.168.1.10"
        port_speed: "10half"
        subnet_mask: "255.255.255.0" 
        spare_default_gateway: "192.168.2.1"
        spare_dns_address: "192.168.2.1"
        spare_ip_address: "192.168.2.10"
        spare_ip_address_mode: "spare"
        spare_subnet_mask: "255.255.0.0"
        vlan_id: 222
        vlan_mode: False
        vlan_priority: 2 
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
#     description: The output messages that the test module generates.
#     type: list
#     returned: always
#     sample: '["Message 1", "Message 2"]'
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
        default_gateway=dict(type='str', required=False),
        dhcp_mode=dict(type='bool', required=False),
        dns_address=dict(type='str', required=False),
        force_http=dict(type='bool', required=False, Default=False),
        host=dict(type='str', required=True),
        ip_address=dict(type='str', required=False),
        keep_session=dict(type='bool', required=False, Default=False),
        lldp_mode=dict(type='bool', required=False, Default=False),
        password=dict(type='str', required=False, Default='6633222', no_log=True),
        port_speed=dict(type='str', required=False),
        session_id=dict(type='str', required=False),
        spare_default_gateway=dict(type='str', required=False),
        spare_dns_address=dict(type='str', required=False),
        spare_ip_address_mode=dict(type='str', required=False),
        spare_ip_address=dict(type='str', required=False),
        spare_subnet_mask=dict(type='str', required=False),
        subnet_mask=dict(type='str', required=False),
        username=dict(type='str', required=False, Default='admin', no_log=True),
        verify_certs=dict(type='bool', required=False, Default=False),
        vlan_id=dict(type='int', required=False),
        vlan_mode=dict(type='bool', required=False, Default=False),
        vlan_priority=dict(type='int', required=False),
    )

    result = dict(
        changed=False,
        failed=True,
        message=[]
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
    defaultGateway = module.params['default_gateway']
    dhcpMode = module.params['dhcp_mode']
    dnsAddress = module.params['dns_address']
    forceHttp = module.params['force_http']
    hostName = module.params['host']
    ipAddress = module.params['ip_address']
    keepSession = module.params['keep_session']
    lldpMode = module.params['lldp_mode']
    password = module.params['password']
    portSpeed = module.params['port_speed']
    sessionId = module.params['session_id']
    spareDefaultGateway = module.params['spare_default_gateway']
    spareDnsAddress = module.params['spare_dns_address']
    spareIpAddressMode = module.params['spare_ip_address_mode']
    spareIpAddress = module.params['spare_ip_address']
    spareSubnetMask = module.params['spare_subnet_mask']
    subnetMask = module.params['subnet_mask']
    userName = module.params['username']
    verifyCerts = module.params['verify_certs']
    vlanId = module.params['vlan_id']
    vlanMode = module.params['vlan_mode']
    vlanPriority = module.params['vlan_priority']

    if forceHttp:
        hostName = 'http://' + hostName
    else:
        hostName = 'https://' + hostName

    result = dict(
        changed = False,
        original_message = '',
        message = []
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    if not sessionId:
        logonResponse, sessionId = logOnPhone(hostName, userName, password, False, verifyCerts, False)
        if logonResponse.status_code != 200 or not sessionId:
            result['failed'] = True
        else:
             result['failed'] = False
    if sessionId:
        # Set default gateway
        if defaultGateway:
            defaultGatewayResponse = setTwoParameters(hostName, sessionId, '4020403', defaultGateway, 'type', 'ip', False, verifyCerts, False)
            if defaultGatewayResponse.status_code != 200:
                result['failed'] = True
                result['message'] = 'Failed to set default gateway'
            else:
                result['failed'] = False
                result['message'].append('Default gateway set to ' + defaultGateway)
        # Set DHCP mode
        if dhcpMode is not None:
            if dhcpMode == True:
                dhcpMode = '1'
            else:
                dhcpMode = '0'
            dhcpModeResponse = setSingleItem(hostName, sessionId, '4020401', dhcpMode, False, verifyCerts, False)
            if dhcpModeResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('DHCP mode not set')
            else:
                result['failed'] = False
                result['message'].append('DHCP mode set to ' + dhcpMode)
        # Set DNS address
        if dnsAddress:
            dnsAddressResponse = setTwoParameters(hostName, sessionId, '4020405', dnsAddress, 'type', 'ip', False, verifyCerts, False)
            if dnsAddressResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('DNS address not set')
            else:
                result['failed'] = False
                result['message'].append('DNS address set to ' + dnsAddress)
        # Set LLDP mode
        if lldpMode is not None:
            if lldpMode == True:
                lldpMode = '1'
            else:
                lldpMode = '0'
            lldpModeResponse = setSingleItem(hostName, sessionId, '44604f3', lldpMode, False, verifyCerts, False)
            if lldpModeResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('LLDP mode not set')
            else:
                result['failed'] = False
                result['message'].append('LLDP mode set to ' + lldpMode)
        # Set IP address
        if ipAddress:
            ipAddressResponse = setTwoParameters(hostName, sessionId, '4020402', ipAddress, 'type', 'ip', False, verifyCerts, False)
            if ipAddressResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('IP address not set')
            else:
                result['failed'] = False
                result['message'].append('IP address set to ' + ipAddress)
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
            portSpeedResponse = setSingleItem(hostName, sessionId, '41d044d', portSpeed, False, verifyCerts, False)
            if portSpeedResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Port speed not set')
            else:
                result['failed'] = False
                result['message'].append('Port speed set to ' + portSpeed)
        # Set subnet mask
        if subnetMask:
            subnetMaskResponse = setTwoParameters(hostName, sessionId, '4020404', subnetMask, 'type', 'ip', False, verifyCerts, False)
            if subnetMaskResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Subnet mask not set')
            else:
                result['failed'] = False
                result['message'].append('Subnet mask set to ' + subnetMask)
        # Set VLAN ID
        if vlanId:
            vlanId = str(vlanId)
            vlanIdResponse = setSingleItem(hostName, sessionId, '41d044f', vlanId, False, verifyCerts, False)
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
            vlanModeResponse = setSingleItem(hostName, sessionId, '41d044e', vlanMode, False, verifyCerts, False)
            if vlanModeResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('VLAN mode not set')
            else:
                result['failed'] = False
                result['message'].append('VLAN mode set to ' + vlanMode)
        # Set VLAN priority
        if vlanPriority:
            vlanPriority = str(vlanPriority)
            vlanPriorityResponse = setSingleItem(hostName, sessionId, '41d0450', vlanPriority, False, verifyCerts, False)
            if vlanPriorityResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('VLAN priority not set')
            else:
                result['failed'] = False
                result['message'].append('VLAN priority set to ' + vlanPriority)
        # Set spare default gateway
        if spareDefaultGateway:
            spareDefaultGatewayResponse = setTwoParameters(hostName, sessionId, '4442002', spareDefaultGateway, 'type', 'ip', False, verifyCerts, False)
            if spareDefaultGatewayResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Spare default gateway not set')
            else:
                result['failed'] = False
                result['message'].append('Spare default gateway set to ' + spareDefaultGateway)
        # Set spare DNS address
        if spareDnsAddress:
            spareDnsAddressResponse = setTwoParameters(hostName, sessionId, '4442004', spareDnsAddress, 'type', 'ip', False, verifyCerts, False)
            if spareDnsAddressResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Spare DNS address not set')
            else:
                result['failed'] = False
                result['message'].append('Spare DNS address set to ' + spareDnsAddress)
        # Set spare IP address
        if spareIpAddress:
            spareIpAddressResponse = setTwoParameters(hostName, sessionId, '4442001', spareIpAddress, 'type', 'ip', False, verifyCerts, False)
            if spareIpAddressResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Spare IP address not set')
            else:
                result['failed'] = False
                result['message'].append('Spare IP address set to ' + spareIpAddress)
        # Set spare ip address mode
        if spareIpAddressMode:
            if spareIpAddressMode == 'spare':
                spareIpAddressMode = '1'
            elif spareIpAddressMode == 'backup':
                spareIpAddressMode = '2'
            else:
                spareIpAddressMode = '0'
            spareIpAddressModeResponse = setSingleItem(hostName, sessionId, '44304f2', spareIpAddressMode, False, verifyCerts, False)
            if spareIpAddressModeResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Spare IP address mode not set')
            else:
                result['failed'] = False
                result['message'].append('Spare IP address mode set to ' + spareIpAddressMode)
        # Set spare subnet mask
        if spareSubnetMask:
            spareSubnetMaskResponse = setTwoParameters(hostName, sessionId, '4442003', spareSubnetMask, 'type', 'ip', False, verifyCerts, False)
            if spareSubnetMaskResponse.status_code != 200:
                result['failed'] = True
                result['message'].append('Spare subnet mask not set')
            else:
                result['failed'] = False
                result['message'].append('Spare subnet mask set to ' + spareSubnetMask)
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