

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

    // new Chart(document.getElementById("myChart").getContext('2d'), {
    //     type: 'line', 
    //     data: {
    //         labels:  Object.values(weatherData.Hour), 
    //         datasets: [
    //             {
    //                 label: "Temperature in Degrees Celsius", 
    //                 data: Object.values(weatherData.Temperature)
    //             }
    //         ]
    //     }
    // }
    // )
}

