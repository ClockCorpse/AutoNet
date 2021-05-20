function updateUsageInfo(usageInfoRequest){
    var cpu_usage;
    var used_ram;
    info = new XMLHttpRequest();
    info.open('GET', usageInfoRequest);
    info.onload = function() {
        cpuPercent = JSON.parse(info.responseText)['cpuPercent'];
        memoryPercent = JSON.parse(info.responseText)['memoryPercent'];
        uptime = JSON.parse(info.responseText)['uptime'];
        updateCPUChart(cpuPercent,memoryPercent);
    };
    info.send();
}
