import psutil
import platform
import cpuinfo
import json
from uptime import uptime

def baseInfo():
    response={}
    cpuInfo = cpuinfo.get_cpu_info()
    response['brand_raw'] = cpuInfo['brand_raw']
    response['bits'] = cpuInfo['bits']
    response['hz'] = cpuInfo['hz_actual_friendly']
    return response
# # print(platform.processor())
# while True:
#     print(psutil.cpu_percent(interval=1))


def resourceMonitor():
    response = {}
    # up = uptime()
    # hour = round(up / 3600)
    # minute = round((up % 3600)/60)
    # sencond = round(minute % 60)
    # upString = f'{hour}:{minute}:{sencond}'
    ramInfo = psutil.virtual_memory()
    response['cpu_usage'] = round(psutil.cpu_percent(interval=1))
    response['total_ram'] = round(ramInfo[0]/1073741824)
    response['used_ram_percentage'] = round(ramInfo.percent)
    # response['uptime'] = upString
    return response
