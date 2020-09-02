 
  var createChart1 = document.getElementById('createdChart1').getContext('2d');
  var createChart2 = document.getElementById('createdChart2').getContext('2d');
  //var aChart = document.getElementById('allChart').getContext('2d');
  var oChart = document.getElementById('openChart').getContext('2d');
  var ocChart = document.getElementById('openclientChart').getContext('2d');
  var opChart = document.getElementById('openproductChart').getContext('2d');
  //var ccChart = document.getElementById('closeclientChart').getContext('2d');

  var doChart = document.getElementById('dailyopenChart').getContext('2d');
   

  var createdChart1 = new Chart(createChart1, {
      type: 'bar',
      data: {
          labels: ['Jan', 'Feb', 'March'],
          datasets: [{
              label: 'Created tickets',
              data: [42, 89, 44],
              backgroundColor: [
              'rgba(114, 147, 203, 2)',
              'rgba(114, 147, 203, 2)',
              'rgba(114, 147, 203, 2)',
                  
              ],
              borderColor: [
                  'rgba(0, 0, 0, 2)',
                   
              ],
              borderWidth: 1
          }]
      },
      options: {
          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero: true
                  }
              }]
          }
      }
  });

  var createdChart2 = new Chart(createChart2, {
      type: 'bar',
      data: {
        labels: ['Jan', 'Feb', 'March'],
          datasets: [{
              label: 'Daily average',
              data: [2.1, 4.5, 3],
              backgroundColor: [
              'rgba(114, 147, 203, 2)',
              'rgba(114, 147, 203, 2)',
              'rgba(114, 147, 203, 2)',
                  
              ],
              borderColor: [
              'rgba(0, 0, 0, 2)',
              'rgba(0, 0, 0, 2)',
              'rgba(0, 0, 0, 2)',
                   
              ],
              borderWidth: 1
          }]
      },
      options: {
          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero: true
                  }
              }]
          }
      }
  });


//   var allChart = new Chart(aChart, {
//       type: 'pie',
//       data: {
//           labels: ['Open', 'Closed'],
//           datasets: [{
//               label: 'All tickets',
//               data: [17, 154],
//               backgroundColor: [
//                 'rgba(114, 147, 203, 2)',
//                 'rgba(125, 25, 203, 2)',
                  
//               ],
//               borderColor: [
//                   'rgba(0, 0, 0, 2)',
                   
//               ],
//               borderWidth: 1
//           }]
//       },
//       options: {
//           scales: {
//               yAxes: [{
//                   ticks: {
//                       beginAtZero: true
//                   }
//               }]
//           }
//       }
//   });

  var openChart = new Chart(oChart, {
      type: 'bar',
      data: {
          labels: ['Jan', 'Feb', 'March'],
          datasets: [{
              label: 'Open tickets',
              data: [42, 89, 44],
              backgroundColor: [
              'rgba(114, 147, 203, 2)',
              'rgba(114, 147, 203, 2)',
              'rgba(114, 147, 203, 2)',
                  
              ],
              borderColor: [
                  'rgba(0, 0, 0, 2)',
                   
              ],
              borderWidth: 1
          },
          {
              label: 'Closed tickets',
              data: [41, 82, 34],
              backgroundColor: [
              'rgba(225, 225, 203, 2)',
              'rgba(225, 225, 203, 2)',
              'rgba(225, 225, 203, 2)',
                  
              ],
              borderColor: [
                  'rgba(0, 0, 0, 2)',
                   
              ],
              borderWidth: 1
          }]
      },
      options: {
          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero: true
                  }
              }]
          }
      }
  });

 




// ##############################
// Clients
// ##############################

 


var openclientChart = new Chart(ocChart, {
    type: 'pie',
    data: { 
        labels: ['Aeon Fantasy', 'Seaoil', 'Pancake House', 'Benilde','UA&P', 'Poveda', 'Hype', 'Fullybooked', 'AllCard'],
        datasets: [{
            label: 'Closed tickets',
            data: [2, 3, 2,1, 1, 3 ,1, 1, 3],
            backgroundColor: [
                '#003f5c',
                '#2f4b7c',
                '#665191',
                '#a05195',
                '#d45087',
                '#f95d6a',
                '#ff7c43',
                '#ffa600'
            ],
            borderColor: [
                '#003f5c',
                '#2f4b7c',
                '#665191',
                '#a05195',
                '#d45087',
                '#f95d6a',
                '#ff7c43',
                '#ffa600'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});



var openproductchart = new Chart(opChart, {
    type: 'doughnut',
    data: { 
        labels: ['Ateilla Rewards Manager', 'ARLO', 'WIP/CPS/INVENTORY', 'Ateilla Time and Attendance', 'MyCampus Card System', 'Door Access System', 'Reloading System'],
        datasets: [{
            label: 'Closed tickets',
            data: [5, 2, 1, 2, 5, 1 ,1],
            backgroundColor: [
                '#003f5c',
                '#2f4b7c',
                '#665191',
                '#a05195',
                '#d45087',
                '#f95d6a',
                '#ff7c43',
                '#ffa600'
            ],
            borderColor: [
                '#003f5c',
                '#2f4b7c',
                '#665191',
                '#a05195',
                '#d45087',
                '#f95d6a',
                '#ff7c43',
                '#ffa600'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});


// var closeclientChart = new Chart(ccChart, {
//     type: 'bar',
//     data: {
//         labels: ['Jan', 'Feb', 'March'],
//         datasets: [{
//             label: 'Closed tickets',
//             data: [41, 82, 34],
//             backgroundColor: [
//                 'rgba(62, 150, 81, 0.2)',
                
//             ],
//             borderColor: [
//                 'rgba(255, 99, 132, 1)',
//                 'rgba(54, 162, 235, 1)',
//                 'rgba(255, 206, 86, 1)',
//                 'rgba(75, 192, 192, 1)',
//                 'rgba(153, 102, 255, 1)',
//                 'rgba(255, 159, 64, 1)'
//             ],
//             borderWidth: 1
//         }]
//     },
//     options: {
//         scales: {
//             yAxes: [{
//                 ticks: {
//                     beginAtZero: true
//                 }
//             }]
//         }
//     }
// });

 

var dailyopenChart = new Chart(doChart, {
    type: 'bar',
    data: {
        labels: ['Jan', 'Feb', 'March'],
        datasets: [{
            label: 'Open tickets',
            data: [2.1, 4.5, 2.2],
            backgroundColor: [
            'rgba(114, 147, 203, 2)',
            'rgba(114, 147, 203, 2)',
            'rgba(114, 147, 203, 2)',
                
            ],
            borderColor: [
                'rgba(0, 0, 0, 2)',
                 
            ],
            borderWidth: 1
        },
        {
            label: 'Closed tickets',
            data: [2.05, 4.1, 1.7],
            backgroundColor: [
            'rgba(114, 147, 203, 2)',
            'rgba(114, 147, 203, 2)',
            'rgba(114, 147, 203, 2)',
                
            ],
            borderColor: [
                'rgba(0, 0, 0, 2)',
                 
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});


 




function controlStatusModal(){
    var modal = document.getElementById('statusModal')
    if(modal.classList.contains("is-active")){
        modal.classList.remove("is-active")
    }
    else{
        modal.classList.add("is-active")
    }
    
}
 