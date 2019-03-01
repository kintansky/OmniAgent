#-*- coding:utf-8 -*-

from device import Device, SqlTable
import time
import re
import os
import mysql.connector

def findOpticalMoudleHW(moudleInfo):
    m = None
    dataLines = []
    exp = re.compile(r'(.*?[0-9]{1,2}/[0-9]{1,2}/[0-9]{1,2}\s+)(\S.*?\s+){3}(\S.*)')
    for line in moudleInfo:
        if m is None:
            m = re.match(exp, line)
        if m is not None:
            port = line[m.span(1)[0]:m.span(1)[1]].strip()
            moudleType = line[m.span(3)[0]::].strip()
            if port == '':  # port=='' 对应模块描述分成多行的情况，需要向上合并
                dataLines[-1][-1] = dataLines[-1][-1] + moudleType    # 对最近插入的一条数据进行修改
            else:
                # result = [recordTime, device._deviceName, port, moudleType]
                result = [port, moudleType]
                dataLines.append(result)
    return dataLines

def findOpticalMoudleAL(moudleInfo):
    m = None
    dataLines = []
    exp = re.compile(r'.*?([0-9]{1,2}/[0-9]{1,2}/[0-9]{1,2})\s+(\S.*?\s+){9}(\S.*)')
    for line in moudleInfo: # 真机测试需要检验一下返回的数据是有会有BOM，如果无BOM可以跟上面HW一样简化
        m = re.match(exp, line)
        if m is not None:
            port = m.group(1)
            moudleType = m.group(3).strip()
            if re.match(r'10GBASE-LR\s+\*', moudleType):    # 部分没有识别出光模块公里数，手工替换
                moudleType = '10GBASE-LR-10KM'
            elif re.match(r'10GBASE-ER\s+\*', moudleType):
                moudleType = '10GBASE-ER-40KM'
            else:
                moudleType = re.sub(r'\s+', '-', moudleType)    # 替换掉空格
            # print('Port:%s Moudle:%s' % (port, moudleType))
            # result = [recordTime, device._deviceName, port, moudleType]
            result = [port, moudleType]
            dataLines.append(result)
    return dataLines

def findOpticalMoudle(moudleInfo, deviceType):
    """
    parameters: moudleInfo由 getDeviceInfo 返回的结果
        插入sql格式datetime, device, port, OpticalMoudle, 前三primary
    """
    if deviceType == 'huawei':
        return findOpticalMoudleHW(moudleInfo)
    elif deviceType == 'alcatel_aos':
        return findOpticalMoudleAL(moudleInfo)
    else:
        print('Device Not Support yet.')
        return []

def getDeviceFeedBack(DeviceNeedCheck):
    checkCmd = ''
    if DeviceNeedCheck._deviceLoginInfo['device_type'] == 'huawei':
        checkCmd = 'screen-length 0 temporary\ndis elabel optical-module brief'
    elif DeviceNeedCheck._deviceLoginInfo['device_type'] == 'alcatel_aos':
        checkCmd = 'environment no more\nshow port | match [0-9]{1,2}/[0-9]{1,2}/[0-9]{1,2} expression'
    moudleInfo = DeviceNeedCheck.getDeviceInfo(checkCmd).split('\n')
    return moudleInfo

def compareMoudle(deviceName, dataLines, DiffTable, recordTime):
    tableInfo = {
        'tb': 'moudle_record_full',
        'host': 'localhost',
        'port': 9003,
        'user': 'root',
        'password': 'hlw2018!@#',
        'db': 'omni_agent',
        }
    MoudleTable = SqlTable(**tableInfo)
    cmd = 'select port, moudle from {} where device = "{}"'.format(*(MoudleTable._tb, deviceName))
    originalData = MoudleTable.queryResult(cmd)
        # 清理旧数据
    cmd = 'delete from {} where device = "{}"'.format(*(MoudleTable._tb, deviceName))
    MoudleTable.executeCmd(cmd)
    portDict = {}
    for data in originalData:
        portDict[data[0]] = data[1]
    for line in dataLines:
        if line[0] not in portDict: # new moudle plugin 
            v = ('"%s"'%l for l in [deviceName]+line+['NoMoudle', 'NEW', recordTime])
            DiffTable.executeCmd('insert into {}(device_name, port, now_moudle, ever_moudle, status, record_time) values ({})'.format(*(DiffTable._tb, ','.join(v))))
        elif line[1] != portDict[line[0]]:  # moudle changed
            v = ('"%s"'%l for l in [deviceName]+line+[portDict[line[0]], 'CH', recordTime])
            DiffTable.executeCmd('insert into {}(device_name, port, now_moudle, ever_moudle, status, record_time) values ({})'.format(*(DiffTable._tb, ','.join(v))))
            portDict.pop(line[0])
        else:
            portDict.pop(line[0])
    if portDict != {}:  # moudle missing
        for port in portDict:
            v = ('"%s"'%l for l in [deviceName, port, 'NoMoudle', portDict[port], 'MISS', recordTime])
            DiffTable.executeCmd('insert into {}(device_name, port, now_moudle, ever_moudle, status, record_time) values ({})'.format(*(DiffTable._tb, ','.join(v))))
    portDict = None
    del portDict


if __name__ == "__main__":
        # 获得设备列表
    print('- Device list Obtaining...')
    tableInfo = {
        'tb': 'watchdog_device',
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'root1234',
        'db': 'omni_agent',
        }
    DeviceInfoTable = SqlTable(**tableInfo)
    # cmd = "select * from {} where device_manufactor_id regexp 'huawei|alcatel_aos'".format(DeviceInfoTable._tb)
    cmd = "select * from {} where device_network = 'IPMAN'".format(DeviceInfoTable._tb)
    deviceList = DeviceInfoTable.queryResult(cmd)
    DeviceInfoTable = None
    del DeviceInfoTable
    
        # 准备设备模块记录表
    print('- Environment setting up...')
    tableInfo['tb'] = 'moudle_record_full'
    MoudleTable = SqlTable(**tableInfo)
    cmd = 'create table if not exists {} (\
        device varchar(100), \
        port varchar(30), \
        moudle varchar(60), \
        recordTime datetime, \
        primary key (device, port)) \
        ENGINE=InnoDB DEFAULT CHARSET=utf8'.format(MoudleTable._tb)
    MoudleTable.executeCmd(cmd)
        # 准备设备模块差异表
    tableInfo['tb'] = 'opticalmoudle_opticalmoudlediff'
    DiffTable = SqlTable(**tableInfo)
    
        # 登陆设备，执行检查命令
    i = 0
    for d in deviceList:
        deviceInfo = {
            'deviceName': d[0],
            'deviceType': d[6],
            'ip': d[1],
            'port': d[3],
            'username': d[4],
            'password': d[5],
                }
        print('%d. Checking Device:%s, IP: %s' % (i, deviceInfo['deviceName'], deviceInfo['ip']))
        try:
            print('\r- Device logging in...', end='', flush=True)
            DeviceNeedCheck = Device(**deviceInfo)
            print('\r- Optical Moudle information collecting...', end='', flush=True)
            moudleInfo = getDeviceFeedBack(DeviceNeedCheck)
            if moudleInfo != ['']:
                recordTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                dataLines = findOpticalMoudle(moudleInfo, deviceInfo['deviceType'])
                print('\r- Optical Moudle differing...', end='', flush=True)
                compareMoudle(DeviceNeedCheck._deviceName, dataLines, DiffTable, recordTime)    # 初始化时可以comment本句
                print('\r- Refreshing Device Moudle record...', end='', flush=True)
                for line in dataLines:
                    data = ('"%s"'%l for l in [DeviceNeedCheck._deviceName]+line+[recordTime])
                    cmd = 'replace into {} values ({})'.format(*(MoudleTable._tb, ','.join(data)))
                    MoudleTable.executeCmd(cmd)
            else:     # 登陆出错情况，不进行处理，直接跳过
                print('\r- Got NOTHING return.')
        except mysql.connector.Error as err:
            print('SQL error: {}'.format(err))
        except Exception as err:
            print('There was an error. {}'.format(err))
        finally:
            DeviceNeedCheck = None
            del DeviceNeedCheck
            print('- Completed!')
            i += 1

