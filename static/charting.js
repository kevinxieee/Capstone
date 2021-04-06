

function sayHello() {
    fetch('/test')
        .then(function (response) {
            return response.json();
        }).then(function (text) {
            console.log('GET response:');
            console.log(text.greeting);
        });
}

async function getData() {

    const response = await fetch(`/getdata`);
    const data = await response.json();
    const optData = JSON.parse(data);

    makeChart(optData);
    makeTable(optData);

}

async function getWeather() {

    const response = await fetch(`/getweather`);
    const data = await response.json();
    const weatherData = JSON.parse(data);

    makeChart(weatherData);

}

function makeChart(displayData) {
    console.log('Making Chart! Here\'s the data!');
    console.log(displayData);

    const ctx = document.getElementById('chart').getContext('2d');
    Chart.defaults.global.defaultFontColor = 'white'
    myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: displayData.columns,
            datasets: [
                {
                    label: 'Base Monthly Bill',
                    data: displayData.base_m_bill,
                    fill: true,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 3
                },
                {
                    label: 'Monthly Bill with Energy Arbitrage Only',
                    data: displayData.EA_m_bill,
                    fill: true,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 3
                },
                {
                    label: 'Monthly Bill with Revenue',
                    data: displayData.ddr_m_bill,
                    fill: true,
                    backgroundColor: 'rgba(255, 206, 86, 0.2)',
                    borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 3
                },
            ]
        },
        options: {
            title: {
                display: true,
                text: 'Monthly Bill',
                fontSize: 20
            },
            scales: {
                xAxes: [{
                    scaleLabel: {
                        display: true,
                    },
                    gridLines: {
                        color: 'white',
                        zeroLineColor: 'white'
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Dollars ($)'
                    },
                    gridLines: {
                        color: 'white',
                        zeroLineColor: 'white'
                    }
                }]
            },
            legend: {
                position: 'bottom',
                padding: 10
            }
        },
    });

}

function makeTable(tableData) {

    var table_pcea = "";
    var table_esb = "";
    var table_pcddr = "";
    for (var i = 0; i < 24; i++) {
        table_pcea += "<tr>";
        table_esb += "<tr>";
        table_pcddr += "<tr>";
        table_pcea += "<td>" + i + "</td>"
        table_esb += "<td>" + i + "</td>"
        table_pcddr += "<td>" + i + "</td>"
        for (var j = 0; j < tableData.pcea.length; j++) {
            console.log(i, j)
            table_pcea += "<td>" + tableData.pcea[j][i].toFixed(3) + "</td>";
        }
        for (var k = 0; k < tableData.esb.length; k++) {
            table_esb += "<td>" + tableData.esb[k][i].toFixed(3) + "</td>";
        }
        for (var x = 0; x < tableData.ddr.length; x++) {
            table_pcddr += "<td>" + tableData.ddr[x][i].toFixed(3) + "</td>";
        }
        table_pcea += "</tr>";
        table_esb += "</tr>";
        table_pcddr += "</tr>";
    }

    document.getElementById("table_pcea").innerHTML += table_pcea
    document.getElementById("table_esb").innerHTML += table_esb
    document.getElementById("table_pcddr").innerHTML += table_pcddr
}

//THIS IS OLD CHART
var displayData_line;
function chart(chart_line) {
    var displayData_line = chart_line;
    const ctx = document.getElementById('chart_line').getContext('2d');
    Chart.defaults.global.defaultFontColor = 'white'
    myChart_line = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
            datasets: [
                {
                    label: 'Month 1 and Month 2',
                    data: displayData_line.pcea[0],
                    fill: false,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 3
                },
                {
                    label: 'Month 3 and Month 4',
                    data: displayData_line.pcea[1],
                    fill: false,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 3
                },
                {
                    label: 'Month 5 and Month 6',
                    data: displayData_line.pcea[2],
                    fill: false,
                    backgroundColor: 'rgba(255, 206, 86, 0.2)',
                    borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 3
                },
                {
                    label: 'Month 7 and Month 8',
                    data: displayData_line.pcea[3],
                    fill: false,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 3
                },
                {
                    label: 'Month 9 and Month 10',
                    data: displayData_line.pcea[4],
                    fill: false,
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 3
                },
                {
                    label: 'Month 11 and Month 12',
                    data: displayData_line.pcea[5],
                    fill: false,
                    backgroundColor: 'rgba(255, 159, 64, 0.2)',
                    borderColor: 'rgba(255, 159, 64, 1)',
                    borderWidth: 3
                }
            ]
        },
        options: {
            title: {
                display: true,
                text: 'PCEA',
                fontSize: 20
            },
            scales: {
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Hour'
                    },
                    gridLines: {
                        color: 'white',
                        zeroLineColor: 'white'
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'kW'
                    },
                    gridLines: {
                        color: 'white',
                        zeroLineColor: 'white'
                    }
                }]
            },
            legend: {
                position: 'bottom',
                padding: 10
            }
        },
    });
};

// FIX THIS, TOGGLING WRONG WHEN CLICKING ONE DATASET FIRST
/*
document.getElementById("toggle").addEventListener('click', () => {
    myChart_line.data.datasets.forEach(function (ds) {
        ds.hidden = !ds.hidden;
    })
    myChart_line.update();
});

document.getElementById("pcea").addEventListener('click', () => {
    myChart_line.options.title.text = 'PCEA'
    myChart_line.data.datasets.forEach(function (dataset, index) {
        dataset.data = displayData_line.pcea[index];
    })
    myChart_line.update();
})
document.getElementById("esb").addEventListener('click', () => {
    myChart_line.options.title.text = 'ESB'
    myChart_line.data.datasets.forEach(function (dataset, index) {
        dataset.data = displayData_line.esb[index];
    })
    myChart_line.update();
})
document.getElementById("pcddr").addEventListener('click', () => {
    myChart_line.options.title.text = 'PCDDR'
    myChart_line.data.datasets.forEach(function (dataset, index) {
        dataset.data = displayData_line.ddr[index];
    })
    myChart_line.update();
})*/