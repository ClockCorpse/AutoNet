from netmiko import ConnectHandler
import json
import requests
from napalm import get_network_driver

# pylint: disable=no-member
requests.packages.urllib3.disable_warnings()


class device:
    def __init__(self, host, port, username, password, enablePassword, deviceDriver):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.enablePassword = enablePassword
        self.deviceDriver = deviceDriver

    def getInterfaceInfo(self):
        driver = get_network_driver(self.deviceDriver)
        networdDevice = driver(self.host, self.username, self.password, optional_args={'secret': self.enablePassword})
        networdDevice.open()
        intStat_ip = networdDevice.get_interfaces_ip()
        intStat = networdDevice.get_interfaces()
        networdDevice.close()
        return intStat_ip, intStat

    def getDeviceFact(self):
        driver = get_network_driver(self.deviceDriver)
        networdDevice = driver(self.host, self.username, self.password, optional_args={'secret': self.enablePassword})
        networdDevice.open()
        output = networdDevice.get_facts()
        networdDevice.close()
        return output

    def checkStatus(self):
        driver = get_network_driver(self.deviceDriver)
        networdDevice = driver(self.host, self.username, self.password, optional_args={'secret': self.enablePassword})
        networdDevice.open()
        output = networdDevice.is_alive()
        networdDevice.close()
        return output

    def discover(self):
        sshCli = ConnectHandler(device_type='cisco_ios',
                                host=self.host,
                                port=self.port,
                                username=self.username,
                                password=self.password)
        output = sshCli.send_command('show cdp neighbor detail', use_textfsm=True)
        sshCli.disconnect()
        return output

    def getInterfaceAPI(self):
        api_url = "https://" + self.host + "/restconf/data/ietf-interfaces:interfaces"

        headers = {"Accept": "application/yang-data+json",
                   "Content-type": "application/yang-data+json"}

        basicauth = ("cisco", "cisco123!")

        resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)

        response_json = resp.json()
        interfacesInfo = {'interface': []}
        for interface in response_json['ietf-interfaces:interfaces']['interface']:
            newInterface = {}
            newInterface['name'] = interface['name']
            newInterface['enabled'] = interface['enabled']
            newInterface['ipv4'] = {}
            newInterface['ipv6'] = {}
            newInterface['ipv4']['address'] = []
            if interface['ietf-ip:ipv4'] != {}:
                for ip in interface['ietf-ip:ipv4']['address']:
                    newInterface['ipv4']['address'].append(ip)
            if interface['ietf-ip:ipv6'] != {}:
                for ip in interface['ietf-ip:ipv6']['address']:
                    newInterface['ipv6']['address'].append(ip)
            interfacesInfo['interface'].append(newInterface)
        return interfacesInfo

    def getRunningConfig(self):
        driver = get_network_driver(self.deviceDriver)
        networdDevice = driver(self.host, self.username, self.password, optional_args={'secret': self.enablePassword})
        networdDevice.open()
        output = networdDevice.get_config(retrieve='running')
        networdDevice.close()
        return output['running']

    def getStartupConfig(self):
        driver = get_network_driver(self.deviceDriver)
        networdDevice = driver(self.host, self.username, self.password, optional_args={'secret': self.enablePassword})
        networdDevice.open()
        output = networdDevice.get_config(retrieve='startup')
        networdDevice.close()
        return output['startup']

    def manual_config(self, config):
        device_os = ''
        # if self.deviceDriver = 'cisco_ios':
        device_os = 'ios'
        try:
            driver = get_network_driver(device_os)
            device = driver(self.host, self.username, self.password, optional_args={'global_delay_factor': 2,'secret': self.enablePassword})
            device.open()
            device.load_merge_candidate(config=config)
            print(device.compare_config())
            device.commit_config()
            device.close()
            return 0
        except Exception as e:
            print(e)
            return 1

    def enable_keepAlive(self, interfaceName):
        device_os = ''
        config = fr'''
        event manager applet {interfaceName}_AUTO_NO_SHUT
        event syslog pattern "Interface {interfaceName}, changed state to administratively down"
        action 1.0 cli command "enable"
        action 1.1 cli command "conf t"
        action 1.2 cli command "interface {interfaceName}"
        action 1.3 cli command "no shutdown"
        '''
        print(config)
        # event manager applet 
        # event syslog pattern "Interface GigabitEthernet4, changed state to adminisratively down
        # action 1.0 cli command "enable"
        # action 1.1 cli command "conf t"
        # action 1.2 cli command "int g4"
        # action 1.3 cli command "no shut"
        # if self.deviceDriver = 'cisco_ios':
        device_os = 'ios'
        try:
            driver = get_network_driver(device_os)
            device = driver(self.host, self.username, self.password, optional_args={'global_delay_factor': 2,'secret': self.enablePassword})
            device.open()
            device.load_merge_candidate(config=config)
            print(device.compare_config())
            device.commit_config()
            device.close()
            return 0
        except Exception as e:
            print(e)
            return 1
    
    def disable_keepAlive(self, interfaceName):
        device_os = ''
        config = f'no event manager applet {interfaceName}_AUTO_NO_SHUT'
        # if self.deviceDriver = 'cisco_ios':
        device_os = 'ios'
        try:
            driver = get_network_driver(device_os)
            device = driver(self.host, self.username, self.password, optional_args={'global_delay_factor': 2,'secret': self.enablePassword})
            device.open()
            device.load_merge_candidate(config=config)
            print(device.compare_config())
            device.commit_config()
            device.close()
            return 0
        except Exception as e:
            print(e)
            return 1

    def tracert(self, dest):
        sshCli = ConnectHandler(device_type='cisco_ios',
                                host=self.host,
                                port=self.port,
                                username=self.username,
                                password=self.password)
        output = sshCli.send_command(f'traceroute {dest}', expect_string=r"#", use_textfsm=True)
        sshCli.disconnect()
        return output


    def getRoutingTable(self):
        sshCli = ConnectHandler(device_type='cisco_ios',
                                host=self.host,
                                port=self.port,
                                username=self.username,
                                password=self.password)
        output = sshCli.send_command(f'show ip route', use_textfsm=True)
        sshCli.disconnect()
        return output
    # driver = get_network_driver('ios')
    # device = driver('10.0.0.20', 'cisco', 'cisco',optional_args={'secret':'cisco'})
    # device.open()
    # device.load_merge_candidate(config='hostname TestRouter')
    # print(device.compare_config())
    # device.commit_config()
    # device.close()

    # def manual_config(self, config):
    #     sshCli = ConnectHandler(device_type='cisco_ios',
    #                             host=self.host,
    #                             port=self.port,
    #                             username=self.username,
    #                             password=self.password,
    #                             secret=self.enablePassword,)
    #     commandList = ['configure terminal', config ]
    #     print(commandList[-1])
    #     output =sshCli.send_config_set(commandList)
    #     print(output)
    #     return output 

# interfaces template:
# {
#     "interface": [
#         {
#             "name": "GigabitEthernet1",
#             "enabled": true,
#             "ipv4": {
#                 "address": [
#                     {
#                         "ip": "192.168.1.50",
#                         "netmask": "255.255.255.0"
#                     }
#                 ]
#             },
#             "ipv6": {}
#         },
#         {
#             "name": "Loopback1",
#             "enabled": false,
#             "ipv4": {
#                 "address": []
#             },
#             "ipv6": {}
#         }
#     ]
# }
