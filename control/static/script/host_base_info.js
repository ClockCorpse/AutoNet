function getBaseInfo(request){
    baseInfo = new XMLHttpRequest();
    baseInfo.open('GET', request);
    baseInfo.onload = function() {
        brand = JSON.parse(baseInfo.responseText)['brand_raw'];
        freq = JSON.parse(baseInfo.responseText)['hz'];
        document.getElementById('brand').innerHTML = brand;
        document.getElementById('freq').innerHTML = freq;
    };
    baseInfo.send();
}
