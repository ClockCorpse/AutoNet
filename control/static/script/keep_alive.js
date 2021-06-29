function keepAliveEnable(id,interfaceID, deviceID){
    request = '/device_detail/'+ deviceID +'/' + interfaceID + '/keepAlive';
    keepAlive = new XMLHttpRequest();
    keepAlive.open('GET', request);
    keepAlive.onload = function(){
        status = JSON.parse(keepAlive.responseText)['success'];
        if(status = true){
            button = document.getElementById(id)
            button.classList.toggle('custom-button')
            if(button.innerHTML == 'Enable')
            button.innerHTML = 'Disable';
            else
            button.innerHTML = 'Enable';
        }
    };
    keepAlive.send()
}