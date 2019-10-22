from multiprocessing import Pool
from os import path
import time
from .model_class import SnmpWorker
from pysnmp.hlapi import CommunityData


BASE_DIR = path.dirname(path.abspath(__file__))

def getSnmpResult(hostIp, authData, mibNodeSet, mibSource):
    deviceSnmp = SnmpWorker(authData, (hostIp, 161), mibNodeSet, mibSource)
    requestResult = deviceSnmp.requestSnmp()
    result = filterData(requestResult)
    return result

def parseSnmpResult(deviceData, authData, mibNodeSet, mibSource):
    hostIp = deviceData[1]
    print(deviceData[0], hostIp)
    result1 = getSnmpResult(hostIp, authData, mibNodeSet, mibSource)
    t1 = time.time()
    time.sleep(10)  # 计算间隔
    result2 = getSnmpResult(hostIp, authData, mibNodeSet, mibSource)
    # print(result2)
    t2 = time.time()
    result = []
    for interface in result2:
        if result2[interface][0] != 0:
            result.append([
                interface,
                result2[interface][0]/1000, # 带宽,单位Gbps
                round((result2[interface][2] - result1[interface][2])/result2[interface][0]/(t2-t1)*100, 2),  # In 百分比
                round((result2[interface][3] - result1[interface][3])/result2[interface][0]/(t2-t1)*100, 2),  # OUT 百分比
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


def mainLinkUtilization(deviceList, processNum=1):
    authData = CommunityData('getgmcc!)', mpModel=1)
    mibSource = path.join(BASE_DIR, 'pysnmp_fmt/')
    print(mibSource)
    mibNodeSet = (
        ('IF-MIB', 'ifName', mibSource),
        ('IF-MIB', 'ifHighSpeed', mibSource),   # 单位1000000bit/s即Mb
        ('IF-MIB', 'ifDescr', mibSource),
        ('IF-MIB', 'ifHCInOctets', mibSource),  # 字节
        ('IF-MIB', 'ifHCOutOctets', mibSource), # 字节
    )
    # 多线程
    p = Pool(processNum)
    resultData = {}
    for d in deviceList:
        result = p.apply_async(parseSnmpResult, args=(d, authData, mibNodeSet, mibSource))
        # print(result.get())
        resultData[d[0]] = result.get()
    p.close()
    p.join()
    return resultData
    # 单线程
    # resultData = {}
    # for d in deviceList:
    #     resultData[d[0]] = parseSnmpResult(d, authData, mibNodeSet, mibSource)
    # return resultData
