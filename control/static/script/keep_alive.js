function keepAliveEnable(id,interfaceID, deviceID){
    loadingSpinner = '&nbsp;&nbsp;<span class="spinner-border spinner-border-sm"></span><span class="sr-only">Loading...</span>';
    button = document.getElementById(id);
    button.innerHTML += loadingSpinner;
    request = '/device_detail/'+ deviceID +'/' + interfaceID + '/keepAlive';
    keepAlive = new XMLHttpRequest();
    keepAlive.open('GET', request);
    keepAlive.onload = function(){
        status = JSON.parse(keepAlive.responseText)['success'];
        if(status = true){
            button.classList.toggle('custom-button');
            if(button.innerHTML == 'Enable' + loadingSpinner)
            button.innerHTML = 'Enabled';
            else
            button.innerHTML = 'Enable';
        }
    };
    keepAlive.send()
}