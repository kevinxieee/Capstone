async function getTable(){
    data = await getData();
    document.getElementById("demo").innerHTML = data.pcea[0][0];
}

getTable();
