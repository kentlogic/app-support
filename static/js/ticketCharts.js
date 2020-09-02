  var ocChart = document.getElementById('openclientChart').getContext('2d');



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
