#-*- coding:utf-8 -*-

from device import Device, SqlTable
import re
import time

def ipFinderHW(ipInfo):
    ips = {}
    exp1 = re.compile(r'.*?(Eth-Trunk\d+\.\d+).*?')
    exp2 = re.compile(r'.*?ip-address\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\svlan\s(\d+)\sce-vlan\s(\d+).*?')
    i = 0
    while i < len(ipInfo):
        m1 = re.match(exp1, ipInfo[i])
        if m1:
            i += 1
            if i >= len(ipInfo):
                break
            m2 = re.match(exp2, ipInfo[i])
            while m2:
                if int(m2.group(1).split('.')[0]) > 127:
                    if m1.group(1) not in ips:
                        ips[m1.group(1)] = []
                    ips[m1.group(1)].append([m2.group(1), m2.group(2), m2.group(3), 'None'])
                i += 1
                if i >= len(ipInfo):
                    break
                m2 = re.match(exp2, ipInfo[i])
        else:
            i += 1
    return ips

def ipFinderAL(ipInfo):
    ips = {}
    exp1 = re.compile(r'\s+sap\s(.*?)\screate')
    exp2 = re.compile(r'\s+description\s"(.*?)"')
    exp3 = re.compile(r'\s+static-host\sip\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\screate')
    i = 0
    while i < len(ipInfo):
        m1 = re.match(exp1, ipInfo[i])
        if i+1 >= len(ipInfo):
            break
        m2 = re.match(exp2, ipInfo[i+1])
        if m1 and m2:
            i += 2
            if i >= len(ipInfo):
                break
            m3 = re.match(exp3, ipInfo[i])
            while m3:
                if m1.group(1) not in ips:
                    ips[m1.group(1)] = []
                m4 = re.match(r'.*?:(\d+)(\.\d+)?', m1.group(1))    # 适应PTN开通专线，通用匹配5/1/2:1000这种端口
                vlan = [m4.group(1), str(m4.group(2)).strip('.')]   # 适应PTN开通专线，通用匹配5/1/2:1000这种端口
                ips[m1.group(1)].append([m3.group(1), vlan[0], vlan[1], m2.group(1)])
                i += 1
                if i >= len(ipInfo):
                    break
                m3 = re.match(exp3, ipInfo[i])
        else:
            i += 1
    return ips
            
def ipFinder(ipInfo, deviceType):
    """
        parameters: ipInfo由 getDeviceInfo 返回的结果
    """
    if deviceType == 'huawei':
        return ipFinderHW(ipInfo)
    elif deviceType == 'alcatel_aos':
        return ipFinderAL(ipInfo)
    else:
        print('No Such brand of device.')
        return {}

def getDeviceFeedBack(DeviceNeedCheck):
    checkCmd = ''
    if DeviceNeedCheck._deviceLoginInfo['device_type'] == 'huawei':
        checkCmd = 'screen-length 0 temporary\ndis cur int Eth-Trunk | include (Eth-Trunk[0-9]+\.[0-9]+)|(bind-table)'    # 华为配置不含专线描述信息
    elif DeviceNeedCheck._deviceLoginInfo['device_type'] == 'alcatel_aos':
        checkCmd = 'environment no more\nadmin disp | match ZhuanXian context all | match "sap|description|static-host" expression'
    ipInfo = DeviceNeedCheck.getDeviceInfo(checkCmd).split('\n')
    return ipInfo


if __name__ == "__main__":
        # 获得设备列表
    print('- Device list Obtaining...')
    tableInfo = {
        'tb': 'watchdog_device',
        'host': 'localhost',
        'port': 9003,
        'user': 'root',
        'password': 'hlw2018!@#',
        'db': 'omni_agent',
        }
    DeviceInfoTable = SqlTable(**tableInfo)
    cmd = 'select * from {} where device_network = "IPMAN" and device_name regexp "^GDFOS-MS-IPMAN"'.format(DeviceInfoTable._tb)
    deviceList = DeviceInfoTable.queryResult(cmd)
    DeviceInfoTable = None
    del DeviceInfoTable
    
        # 准备ip地址记录表
    print('- Environment setting up...')
    tableInfo['tb'] = 'iprecord_publiciprecord'
    IpTable = SqlTable(**tableInfo)
    IpTable.executeCmd('truncate table %s' % IpTable._tb)
    
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
            print('\r- IP address information collecting...', end='', flush=True)
            ipInfo = getDeviceFeedBack(DeviceNeedCheck)
            print('\r- IP address information filtering...', end='', flush=True)
            ips = ipFinder(ipInfo, DeviceNeedCheck._deviceLoginInfo['device_type'])

            if ips != {}:
                print('\r- Refreshing device address record...')
                recordTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                for port in ips:
                    for line in ips[port]:
                        data = ('"%s"'%l for l in [line[0], DeviceNeedCheck._deviceName, port]+line[1::]+[recordTime])
                        cmd = 'replace into {} values ({})'.format(*(IpTable._tb, ','.join(data)))
                        IpTable.executeCmd(cmd)
            else:
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
            
