getInterface = new XMLHttpRequest();
    getInterface.open('GET', "{% url 'control:updateInterface' device.id %}");
    getInterface.onload = function() {
        var i = 0;
        interfaces = JSON.parse(getInterface.responseText)[0];
        interfacesIP = JSON.parse(getInterface.responseText)[1];
        console.log(interfaces)
        for (const item in interfaces) {
            let mac = interfaces[item]['mac_address'];
            let description = interfaces[item]['description'];
            let status = interfaces[item]['is_enabled'];
            let protocol = interfaces[item]['is_up'];
            idIndex = i + 1;
            document.getElementById('interface' + idIndex).innerHTML = '<strong>' + item + '</strong>';
            for (const int in interfacesIP) {
                if (int == item) {
                    console.log(Object.entries(interfacesIP[int]['ipv4'])[0][1]['prefix_length']);
                    document.getElementById('ipv4' + idIndex).innerHTML = Object.entries(interfacesIP[int]['ipv4'])[0][0] + '/' + Object.entries(interfacesIP[int]['ipv4'])[0][1]['prefix_length'];
                }
            }
            document.getElementById('MAC' + idIndex).innerHTML = mac;
            document.getElementById('description' + idIndex).innerHTML = description;
            document.getElementById('status' + idIndex).innerHTML = status;
            document.getElementById('protocol' + idIndex).innerHTML = protocol;
            i++;
        };
    };
    getInterface.send();