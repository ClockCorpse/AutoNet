function updateInterface(request){
    // document.getElementById('loading').innerHTML = '<div class="row justify-content-center"><div class="lds-dual-ring"></div></div>';
    getInterface = new XMLHttpRequest();
    getInterface.open('GET', request);
    getInterface.onload = function() {
        // document.getElementById('loading').innerHTML = ''
        var i = 0;
        interfaces = JSON.parse(getInterface.responseText)[0];
        interfacesIP = JSON.parse(getInterface.responseText)[1];
        fact = JSON.parse(getInterface.responseText)[2];
        keepAliveStatus = JSON.parse(getInterface.responseText)[3];
        deviceID = JSON.parse(getInterface.responseText)[4]['deviceID'];
        document.getElementById('hostname').innerHTML = fact['hostname'];
        document.getElementById('vendor').innerHTML = fact['vendor'];
        document.getElementById('fqdn').innerHTML = fact['fqdn'];
        document.getElementById('up-time').innerHTML = fact['uptime'] / 60;
        document.getElementById('table_body').innerHTML = ''
        for (const item in interfaces) {
            let mac = interfaces[item]['mac_address'];
            let description = interfaces[item]['description'];
            let status = interfaces[item]['is_enabled'];
            if(status == true){
                status = 'up';
            }else{
                status = 'down';
            }
            let protocol = interfaces[item]['is_up'];
            if(protocol == true){
                protocol = 'up';
            }else{
                protocol = 'down';
            }
            let buttonContent = 'Enable';
            let buttonStyle = 'custom-button';
            if( keepAliveStatus[item]['status'] == true){
                buttonContent = 'Enabled';
                buttonStyle = 'btn-secondary';
            }
            idIndex = i + 1;
            document.getElementById('table_body').innerHTML += '<tr>' +
                '<td id="interface' + idIndex + '">' + '<strong>' + item + '</strong>' + '</td>' +
                '<td id="ipv4' + idIndex + '"></td>' +
                '<td id="MAC' + idIndex + '">' + mac + '</td>' +
                '<td id="description' + idIndex + '">' + description + '</td>' +
                '<td id="status' + idIndex + '">' + status + '</td>' +
                '<td id="protocol' + idIndex + '">' + protocol + '</td>' +
                '<td id="keepAlive' + idIndex + '">' + '<button id="keepAliveButton' + idIndex + '" class="btn btn-sm btn-secondary ' + buttonStyle + '" onclick="keepAliveEnable(\'keepAliveButton' + idIndex+'\',' + keepAliveStatus[item]['id'] + ','+ deviceID +')">' + buttonContent + '</button>' + '</td>' +
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
