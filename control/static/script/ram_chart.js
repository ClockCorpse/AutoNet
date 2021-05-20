var ramChart = document.getElementById('ram').getContext('2d')
    var massRAMChart = new Chart(ramChart,{
            type:'line',
            data:{
                labels:[],
                datasets:[{
                    label:'',
                    data:[],
                    fill: false,
                    borderColor:'red',
                    borderWidth: 3,
                    backgroundColor:'#ff000033',
                    fill:true,
                    tension:0.2,
                }]
            },
            options: {
                scales: {
                    xAxes: [],
                    yAxes: {
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                }
            }
        });
