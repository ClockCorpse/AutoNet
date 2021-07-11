var ctx = document.getElementById("devices");
var inventory = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ['Unmonitored', 'Monitored'],
    datasets: [{
      label: 'Inventory',
      data: [0, 0],
      backgroundColor: [
        'rgb(205, 205, 205, 0.75)',
        // 'rgb(92, 184, 92, 0.3)'
        'rgba(54, 162, 235, 0.2)'
        // 'rgba(54, 162, 235, 0.2)',
      ],
      borderColor: [
        'rgba(205, 205, 205, 1)',
        // 'rgba(92, 184, 92, 1)',
        'rgba(54, 162, 235, 1)'
      ],
      borderWidth: 1
    }]
  },
  options: {
   	//cutoutPercentage: 40,
    responsive: false,

  }
});

var updateInventory = function(tracking,untracked){
  inventory.data.datasets[0].data[0] = untracked;
  inventory.data.datasets[0].data[1] = tracking;
  inventory.update();
}

function updateInventoryInfo(inventoryInfoRequest){
  tracking=0;
  untracked=0;
  info = new XMLHttpRequest();
  info.open('GET', inventoryInfoRequest);
  info.onload = function() {
      console.log(info.responseText);
      tracking = JSON.parse(info.responseText)['tracking'];
      untracked = JSON.parse(info.responseText)['untracked'];
      updateInventory(tracking,untracked);
  };
  info.send();
}