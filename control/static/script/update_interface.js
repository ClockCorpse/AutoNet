function updateInterface(request){
    getInterface = new XMLHttpRequest();
    getInterface.open('GET', request);
    getInterface.onload = function() {
        var i = 0;
        interfaces = JSON.parse(getInterface.responseText)[0];
        interfacesIP = JSON.parse(getInterface.responseText)[1];
        fact = JSON.parse(getInterface.responseText)[2];
        document.getElementById('hostname').innerHTML = fact['hostname'];
        document.getElementById('vendor').innerHTML = fact['vendor'];
        document.getElementById('fqdn').innerHTML = fact['fqdn'];
        document.getElementById('up-time').innerHTML = fact['uptime'] / 60;
        document.getElementById('table_body').innerHTML = ''
        for (const item in interfaces) {
            let mac = interfaces[item]['mac_address'];
            let description = interfaces[item]['description'];
            let status = interfaces[item]['is_enabled'];
            let protocol = interfaces[item]['is_up'];
            idIndex = i + 1;
            document.getElementById('table_body').innerHTML += '<tr>' +
                '<td id="interface' + idIndex + '">' + '<strong>' + item + '</strong>' + '</td>' +
                '<td id="ipv4' + idIndex + '"></td>' +
                '<td id="MAC' + idIndex + '">' + mac + '</td>' +
                '<td id="description' + idIndex + '">' + description + '</td>' +
                '<td id="status' + idIndex + '">' + status + '</td>' +
                '<td id="protocol' + idIndex + '">' + protocol + '</td>' +
                '</tr>';
            for (const int in interfacesIP) {
                if (int == item) {
                    document.getElementById('ipv4' + idIndex).innerHTML = Object.entries(interfacesIP[int]['ipv4'])[0][0] + '/' + Object.entries(interfacesIP[int]['ipv4'])[0][1]['prefix_length'];
                }
            }
            i++;
        };
    };
    getInterface.send();
}
