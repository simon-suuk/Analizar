let myChart = document.getElementById('myChart').getContext('2d');
let myChart2 = document.getElementById('myChart2').getContext('2d');
let myChart3 = document.getElementById('myChart3').getContext('2d');



// Global Options
Chart.defaults.global.defaultFontFamily = 'Lato';
Chart.defaults.global.defaultFontSize = 18;
Chart.defaults.global.defaultFontColor = '#777';



let fanGrowthChart = new Chart(myChart, {
    type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data:{
        labels:['Monday', 'Tuesday', 'Wednessday', 'Thursday','Friday','Saturday', 'Sunday'],
        datasets:[{

            data:[
                4,
                6,
                5,
                3,
                7,
                2,
                8
            ],
            //backgroundColor:'green',
            backgroundColor:[
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                'rgba(255, 159, 64, 0.6)',
                'rgba(255, 99, 132, 0.6)',
                'rgba(75, 192, 192, 0.6)'
            ],
            borderWidth:1,
            borderColor:'#777',
            hoverBorderWidth:3,
            hoverBorderColor:'#000'
        }]
    },
    options:{
        title:{
            display:true,
            text:'Fan Growth per Day',
            fontSize:25
        },
        legend:{
            display:false,
            position:'right',
            labels:{
                fontColor:'#000'
            }
        },
        layout:{
            padding:{
                left:50,
                right:0,
                bottom:0,
                top:0
            }
        },
        tooltips:{
            enabled:true
        }
    }
});

let engagementContentChart = new Chart(myChart2, {
    type:'pie', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data:{
        labels:['Picture', 'Video', 'Text', 'Link','Gif'],
        datasets:[{
            data:[
                20,
                10,
                5,
                3,
                7
            ],
            //backgroundColor:'green',
            backgroundColor:[
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                // 'rgba(255, 159, 64, 0.6)',
                // 'rgba(255, 99, 132, 0.6)'
            ],
            borderWidth:1,
            borderColor:'#777',
            hoverBorderWidth:3,
            hoverBorderColor:'#000'
        }]
    },
    options:{
        title:{
            display:true,
            text:'Engagement Level per Content Type',
            fontSize:25
        },
        legend:{
            display:true,
            position:'right',
            labels:{
                fontColor:'#000'
            }
        },
        layout:{
            padding:{
                left:50,
                right:0,
                bottom:0,
                top:0
            }
        },
        tooltips:{
            enabled:true
        }
    }
});



let activefanChart = new Chart(myChart3, {
    type:'horizontalBar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data:{
        labels:['Monday', 'Tuesday', 'Wednessday', 'Thursday','Friday','Saturday', 'Sunday'],
        datasets:[{
            data:[
                4,
                6,
                5,
                3,
                7,
                2,
                8
            ],
            //backgroundColor:'green',
            backgroundColor:[
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                'rgba(255, 99, 132, 0.6)',
                'rgba(255, 159, 64, 0.6)'
            ],
            borderWidth:1,
            borderColor:'#777',
            hoverBorderWidth:3,
            hoverBorderColor:'#000'
        }]
    },
    options:{
        title:{
            display:true,
            text:'Active Audience Time',
            fontSize:25
        },
        legend:{
            display:false,
            position:'right',
            labels:{
                fontColor:'#000'
            }
        },
        layout:{
            padding:{
                left:50,
                right:0,
                bottom:0,
                top:0
            }
        },
        tooltips:{
            enabled:true
        }
    }
});

