async function getTable(){
    data = await getData();
    //document.getElementById("demo").innerHTML = data.pcea[0][0];

    var table_pcea = "";
    var table_esb = "";
    var table_pcddr = "";
    for (var i = 0; i < data.hours.length; i++){
        table_pcea += "<tr>";
        table_esb += "<tr>";
        table_pcddr += "<tr>";
        for (var j = 0; j < data.pcea.length; j++){
            console.log(i, j)
            table_pcea += "<td>" + data.pcea[j][i] + "</td>";
        }
        for (var k = 0; k < data.esb.length; k++){
            table_esb += "<td>" + data.esb[k][i] + "</td>";
        }
        for (var x = 0; x < data.pcddr.length; x++){
            table_pcddr += "<td>" + data.pcddr[x][i] + "</td>";
        }
        table_pcea += "</tr>";
        table_esb += "</tr>";
        table_pcddr += "</tr>";
    }

    document.getElementById("table_pcea").innerHTML += table_pcea
    document.getElementById("table_esb").innerHTML += table_esb
    document.getElementById("table_pcddr").innerHTML += table_pcddr
}

getTable();

