function updateUsageInfo(usageInfoRequest){
    var cpu_usage;
    var used_ram;
    info = new XMLHttpRequest();
    info.open('GET', usageInfoRequest);
    info.onload = function() {
        cpu_usage = JSON.parse(info.responseText)['cpu_usage'];
        total_ram = JSON.parse(info.responseText)['total_ram'];
        used_ram = JSON.parse(info.responseText)['used_ram_percentage'];
        uptime = JSON.parse(info.responseText)['uptime'];
        document.getElementById('cpu-percent').innerHTML=cpu_usage;
        document.getElementById('ram-percent').innerHTML=used_ram;
        updateCPUChart(cpu_usage,used_ram);
    };
    info.send();
}
