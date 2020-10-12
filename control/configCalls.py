from netmiko import ConnectHandler
import json
import requests
# pylint: disable=no-member
requests.packages.urllib3.disable_warnings()

class device:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def getInterfaceInfo(self):
        sshCli = ConnectHandler(device_type='cisco_ios',
                                host=self.host,
                                port=self.port,
                                username=self.username,
                                password=self.password)
        output = sshCli.send_command('show ip int brief', use_textfsm=True)
        return output
    
    def discover(self):
        sshCli = ConnectHandler(device_type='cisco_ios',
                                host=self.host,
                                port=self.port,
                                username=self.username,
                                password=self.password)
        output =sshCli.send_command('show cdp neighbor detail',use_textfsm=True)
        return output

    def getInterfaceAPI(self):
        api_url = "https://" + self.host + "/restconf/data/ietf-interfaces:interfaces"

        headers = { "Accept": "application/yang-data+json", 
                    "Content-type":"application/yang-data+json"}

        basicauth = ("cisco", "cisco123!")

        resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)

        response_json = resp.json()
        interfacesInfo = {'interface':[]}
        for interface in response_json['ietf-interfaces:interfaces']['interface']:
                newInterface={}
                newInterface['name'] = interface['name']
                newInterface['enabled'] = interface['enabled']
                newInterface['ipv4']={}
                newInterface['ipv6']={}
                newInterface['ipv4']['address']=[]
                if interface['ietf-ip:ipv4'] != {}:
                        for ip in interface['ietf-ip:ipv4']['address']:
                                newInterface['ipv4']['address'].append(ip)
                if interface['ietf-ip:ipv6'] != {}:
                        for ip in interface['ietf-ip:ipv6']['address']:
                                newInterface['ipv6']['address'].append(ip)
                interfacesInfo['interface'].append(newInterface)
        return interfacesInfo

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