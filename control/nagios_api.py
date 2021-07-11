import requests

class host_template:
    def __init__(self, server, host, hostname, apikey):
        self.server = server
        self.host = host
        self.hostname = hostname
        self.apikey = apikey
    
    def add_host(self):
        url = f'http://{self.server}/nagiosxi/api/v1/config/host?apikey={self.apikey}'
        param = { 'host_name' : self.hostname,
            'address':self.host,
            'use':[
                'xiwizard_switch_host'
            ],
            'max_check_attempts':5,
            'check_interval': 5,
            'retry_interval': 1,
            'check_period':'24x7',
            'contacts':'nagiosadmin',
            'notification_interval':60,
            'notification_period':'24x7',
            'applyconfig':1
        }
        response = requests.post(url,data=param)
        return response.text

    def delete_host(self):
        url = f'http://{self.server}/nagiosxi/api/v1/config/host/?apikey={self.apikey}&host_name={self.hostname}&applyconfig=1'
        response = requests.delete(url)
        print(url)
        print(response.text)
        return response.text

    def add_check_interface(self, index):
        url = f'http://{self.server}/nagiosxi/api/v1/config/service?apikey={self.api}'
        param = { 
            'host_name' : self.hostname,
            'service_description': f'{self.hostname} status',
            'check_command': f'check_xi_service_ifoperstatus\!public\!{index}\!-v 2 -p 161',
            'max_check_attempts':5,
            'check_interval':5,
            'retry_interval': 1,
            'check_period':'xi_timeperiod_24x7',
            'notification_interval':60,
            'notification_period':'xi_timeperiod_24x7',
            'contacts':[
                'nagiosadmin'
            ],
            '_xiwizard':'switch',
            'register':1,
            'applyconfig':1,
        }
        response = requests.post(url,data=param)
        return response.text


class get_status:
    def __init__(self, server, apikey):
        self.server = server
        self.apikey = apikey

    def get_host_status(self):
    # Returns the current host status.
        url = f'http://{self.server}/nagiosxi/api/v1/objects/hoststatus?apikey={self.apikey}'
        response = requests.get(url)
        return response.text
