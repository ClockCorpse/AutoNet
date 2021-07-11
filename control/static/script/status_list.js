var ctx = document.getElementById("status");
var overallStatus = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ['Down', 'Up'],
    datasets: [{
      label: 'aaaa',
      data: [0, 0],
      backgroundColor: [
        'rgba(255, 99, 132, 0.5)',
        'rgb(92, 184, 92, 0.3)'
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgb(92, 184, 92, 1)'
      ],
      borderWidth: 1
    }]
  },
  options: {
   	//cutoutPercentage: 40,
    responsive: false,

  }
});

var updateOverallStatus = function(ok,critical){
    overallStatus.data.datasets[0].data[0] = critical;
    overallStatus.data.datasets[0].data[1] = ok;
    overallStatus.update();
}

function updateDeviceStatus(deviceStatusRequest){
  ok=0;
  critical=0;
  deviceStatus = new XMLHttpRequest();
  deviceStatus.open('GET', deviceStatusRequest);
  deviceStatus.onload = function() {
      console.log(deviceStatus.responseText);
      ok = JSON.parse(deviceStatus.responseText)['ok'];
      critical = JSON.parse(deviceStatus.responseText)['critical'];
      updateOverallStatus(ok,critical)
  };
  deviceStatus.send();
}