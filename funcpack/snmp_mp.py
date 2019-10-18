from multiprocessing import Pool
from os import path
import time
from device import SnmpWorker
from pysnmp.hlapi import CommunityData


BASE_DIR = path.dirname(path.abspath(__file__))

def getSnmpResult(hostIp, authData, mibNodeSet, mibSource):
    deviceSnmp = SnmpWorker(authData, (hostIp, 161), mibNodeSet, mibSource)
    requestResult = deviceSnmp.requestSnmp()
    result = filterData(requestResult)
    return result

def parseSnmpResult(deviceData, authData, mibNodeSet, mibSource):
    print(deviceData[0])
    hostIp = deviceData[1]
    result1 = getSnmpResult(hostIp, authData, mibNodeSet, mibSource)
    t1 = time.time()
    time.sleep(10)
    result2 = getSnmpResult(hostIp, authData, mibNodeSet, mibSource)
    # print(result2)
    t2 = time.time()
    result = []
    for interface in result2:
        if result2[interface][0] != 0:
            result.append([
                interface,
                result2[interface][0]/1000, # 带宽单位Gbps
                (result2[interface][2] - result1[interface][2])/result2[interface][0]/(t2-t1)*100,  # In 百分比
                (result2[interface][3] - result1[interface][3])/result2[interface][0]/(t2-t1)*100,  # OUT 百分比
                result2[interface][1],  # 端口描述
            ])
    return result
    
def filterData(requestResult):
    result = {}
    for r in requestResult:
        # print(r)
        # debug
        # if r[0].split('.')[-1] != r[6].split('.')[-1]:
        #     print(r[0], r[6])
        result[r[1]] = (int(r[3]), r[5].split(',')[-1].strip('" '), int(r[7])*8/1000000, int(r[9])*8/1000000)
    return result


def main(deviceList, processNum=1):
    authData = CommunityData('getgmcc!)', mpModel=1)
    mibSource = path.join(BASE_DIR, 'src/pysnmp_fmt/')
    mibNodeSet = (
        ('IF-MIB', 'ifName', 'default'),
        ('IF-MIB', 'ifHighSpeed', 'default'),   # 单位1000000bit/s即Mb
        ('IF-MIB', 'ifDescr', 'default'),
        ('IF-MIB', 'ifHCInOctets', 'default'),  # 字节
        ('IF-MIB', 'ifHCOutOctets', 'default'), # 字节
    )
    p = Pool(processNum)
    resultData = {}
    for d in deviceList:
        result = p.apply_async(parseSnmpResult, args=(d, authData, mibNodeSet, mibSource))
        resultData[d[0]] = result.get()
    p.close()
    p.join()
    return resultData
