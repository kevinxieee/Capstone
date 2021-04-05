async function getData() {
    const hours = [];
    const pcea = [[], [], [], [], [], []];
    const esb = [[], [], [], [], [], []];
    const pcddr = [[], [], [], [], [], []];
    const data_file = await fetch('../data/SampleChartData.csv');
    const data = await data_file.text();

    const table = data.split('\n').slice(1);
    table.forEach(elt => {
        const columns = elt.split(',');
        hours.push(columns[0]);
        pcea[0].push(parseFloat(columns[1]).toFixed(3));
        pcea[1].push(parseFloat(columns[2]).toFixed(3));
        pcea[2].push(parseFloat(columns[3]).toFixed(3));
        pcea[3].push(parseFloat(columns[4]).toFixed(3));
        pcea[4].push(parseFloat(columns[5]).toFixed(3));
        pcea[5].push(parseFloat(columns[6]).toFixed(3));
        esb[0].push(parseFloat(columns[7]).toFixed(3));
        esb[1].push(parseFloat(columns[8]).toFixed(3));
        esb[2].push(parseFloat(columns[9]).toFixed(3));
        esb[3].push(parseFloat(columns[10]).toFixed(3));
        esb[4].push(parseFloat(columns[11]).toFixed(3));
        esb[5].push(parseFloat(columns[12]).toFixed(3));
        pcddr[0].push(parseFloat(columns[13]).toFixed(3));
        pcddr[1].push(parseFloat(columns[14]).toFixed(3));
        pcddr[2].push(parseFloat(columns[15]).toFixed(3));
        pcddr[3].push(parseFloat(columns[16]).toFixed(3));
        pcddr[4].push(parseFloat(columns[17]).toFixed(3));
        pcddr[5].push(parseFloat(columns[18]).toFixed(3));
    });
    return { hours, pcea, esb, pcddr };
}

var myChart;
var data;
chart();
async function chart() {
    data = await getData();
    const ctx = document.getElementById('chart').getContext('2d');
    Chart.defaults.global.defaultFontColor = 'white'
    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.hours,
            datasets: [
                {
                    label: 'Month 1 and Month 2',
                    data: data.pcea[0],
                    fill: false,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 3
                },
                {
                    label: 'Month 3 and Month 4',
                    data: data.pcea[1],
                    fill: false,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 3
                },
                {
                    label: 'Month 5 and Month 6',
                    data: data.pcea[2],
                    fill: false,
                    backgroundColor: 'rgba(255, 206, 86, 0.2)',
                    borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 3
                },
                {
                    label: 'Month 7 and Month 8',
                    data: data.pcea[3],
                    fill: false,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 3
                },
                {
                    label: 'Month 9 and Month 10',
                    data: data.pcea[4],
                    fill: false,
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 3
                },
                {
                    label: 'Month 11 and Month 12',
                    data: data.pcea[5],
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
document.getElementById("toggle").addEventListener('click', () => {
    myChart.data.datasets.forEach(function (ds) {
        ds.hidden = !ds.hidden;
    })
    myChart.update();
});

document.getElementById("pcea").addEventListener('click', () => {
    myChart.options.title.text = 'PCEA'
    myChart.data.datasets.forEach(function (dataset, index) {
        dataset.data = data.pcea[index];
    })
    myChart.update();
})
document.getElementById("esb").addEventListener('click', () => {
    myChart.options.title.text = 'ESB'
    myChart.data.datasets.forEach(function (dataset, index) {
        dataset.data = data.esb[index];
    })
    myChart.update();
})
document.getElementById("pcddr").addEventListener('click', () => {
    myChart.options.title.text = 'PCDDR'
    myChart.data.datasets.forEach(function (dataset, index) {
        dataset.data = data.pcddr[index];
    })
    myChart.update();
})

var csvFileData = [
    ['Alan Walker', 'Singer'],
    ['Cristiano Ronaldo', 'Footballer'],
    ['Saina Nehwal', 'Badminton Player'],
    ['Arijit Singh', 'Singer'],
    ['Terence Lewis', 'Dancer']
];

//create a user-defined function to download CSV file 
function download_csv_file() {

    //define the heading for each row of the data
    var csv = 'Name,Profession\n';

    //merge the data with CSV
    csvFileData.forEach(function (row) {
        csv += row.join(',');
        csv += "\n";
    });

    //display the created CSV data on the web browser 
    document.write(csv);


    var hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
    hiddenElement.target = '_blank';

    //provide the name for the CSV file to be downloaded
    hiddenElement.download = 'Famous Personalities.csv';
    hiddenElement.click();
}