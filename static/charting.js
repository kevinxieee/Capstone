

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

function makeChart(displayData){
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