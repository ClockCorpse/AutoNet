function toggle_monitor(request,deviceID,elementID){
    button  = document.getElementById(elementID);
    previousStatus = button.innerHTML;
    loadingSpinner = '<span class="spinner-border spinner-border-sm"></span><span class="sr-only">Loading...</span>';
    button.innerHTML = loadingSpinner;
    monitor = new XMLHttpRequest();
    monitor.open('GET',request);
    monitor.onload = function(){
        status = JSON.parse(monitor.responseText);

        console.log(status);
        if(status['success'] != ''){
            button.classList.toggle('btn-success');
            button.classList.toggle('btn-secondary');
            if(previousStatus == 'Add to monitor'){
                button.innerHTML = 'Added to monitor';
            }
            else{
                button.innerHTML = 'Add to monitor';
            }
        }
    };
    monitor.send();
}
