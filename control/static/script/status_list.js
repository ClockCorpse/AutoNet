var ctx = document.getElementById("status");
var overallStatus = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ['Down', 'Warning', 'Up'],
    datasets: [{
      label: 'Device Status',
      data: [0, 0, 0],
      backgroundColor: [
        'rgba(255, 99, 132, 0.5)',
        'rgba(238, 210, 2, 0.3)',
        'rgba(92, 184, 92, 0.3)'
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(238, 210, 2, 1)',
        'rgb(92, 184, 92, 1)'
      ],
      borderWidth: 1
    }]
  },
  options: {
   	//cutoutPercentage: 40,
    responsive: false,
    plugins: {
      legend: {
          display: true,
          position: 'bottom'
      }
    }
  }
});

var updateOverallStatus = function(ok, warning,critical){
    overallStatus.data.datasets[0].data[0] = critical;
    overallStatus.data.datasets[0].data[1] = warning;
    overallStatus.data.datasets[0].data[2] = ok;
    overallStatus.update();
}

function updateDeviceStatus(deviceStatusRequest){
  ok=0;
  critical=0;
  deviceStatus = new XMLHttpRequest();
  deviceStatus.open('GET', deviceStatusRequest);
  deviceStatus.onload = function() {
      console.log(deviceStatus.responseText);
      ok = JSON.parse(deviceStatus.responseText)['overall']['ok'];
      warning = JSON.parse(deviceStatus.responseText)['overall']['warning'];
      critical = JSON.parse(deviceStatus.responseText)['overall']['critical'];
      updateOverallStatus(ok, warning, critical);
      statusDetail = JSON.parse(deviceStatus.responseText)['status_detail'];
      console.log(statusDetail);
      tableContent = '';
      tableDetail = document.getElementById('status_table_body')
      for (const item in statusDetail){
        output='';
        if(statusDetail[item]['output'].split(' ')[0] =='OK'){
          output = '<td class="table-success">' + statusDetail[item]['output'] + '</td>';
        }else if (statusDetail[item]['output'].split(' ')[0] =='WARNING'){
          output = '<td class="table-warning">' + statusDetail[item]['output'] + '</td>';
        } else{
          output = '<td class="table-danger">' + statusDetail[item]['output'] + '</td>';
        }
        tableContent += '<tr>' + '<td>' + item + '</td>' + output + '<td>' + statusDetail[item]['last_check'] + '</td>' + '</tr>';
        console.log(statusDetail[item]['output']);
        console.log(statusDetail[item]['last_check']);
      }
      tableDetail.innerHTML = tableContent;
  };
  deviceStatus.send();
}