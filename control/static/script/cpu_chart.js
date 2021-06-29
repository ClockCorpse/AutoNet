var cpuChart = document.getElementById('resource').getContext('2d')
    var massCPUChart = new Chart(cpuChart,{
            type:'line',
            data:{
                labels:[],
                datasets:[{
                    label:'CPU',
                    data:[],
                    fill: false,
                    borderColor:'green',
                    borderWidth: 2,
                    backgroundColor:'#00ff0033',
                    fill:true,
                    tension:0.3,
                    pointRadius: 1
                },
                {
                    label:'Memory',
                    data:[],
                    fill: false,
                    borderColor:'red',
                    borderWidth: 2,
                    backgroundColor:'#ff000033',
                    fill:true,
                    tension:0.2,
                    pointRadius: 1
                }],
            },
            options: {
                scales: {
                    x: {
                        grid: {
                          display: false,
                        }
                      },
                    y: {
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                }
            }
        });
var updateCPUChart = function(cpu_usage,used_ram){
    massCPUChart.data.labels.push('')
    massCPUChart.data.datasets[0].data.push(cpu_usage);
    massCPUChart.data.datasets[1].data.push(used_ram);
    if(massCPUChart.data.datasets[0].data.length>50){
        massCPUChart.data.labels.shift()
        massCPUChart.data.datasets[0].data.shift()
        massCPUChart.data.datasets[1].data.shift();
    }
    massCPUChart.update();
}
