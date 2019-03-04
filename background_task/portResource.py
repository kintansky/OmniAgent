#-*- coding:utf-8 -*-

from device import Device, SqlTable
import re
import time
import mysql.connector


def getDeviceFeedBack(DeviceNeedCheck):
    cmds = ''
    if DeviceNeedCheck._deviceLoginInfo['device_type'] == 'alcatel_aos':
        cmds = 'environment no more\nshow port description | match [0-9]{1,2}/[0-9]{1,2}/ expression\nshow port | match [0-9]{1,2}/[0-9]{1,2}/ expression\nshow mda | match "[0-9] " expression\nshow card | match ^[0-9] expression\nadmin disp | match "lag [0-9]{1,}" expression context all | match des context all'
    elif DeviceNeedCheck._deviceLoginInfo['device_type'] == 'huawei':
        cmds = 'screen-length 0 temporary\ndis int des | include "[0-9]+/[0-9]+/[0-9]+|Eth-Trunk" | exclude "Eth-Trunk[0-9]+\."\ndis int brief | include "[0-9]+/[0-9]+/[0-9]+|Eth-Trunk" | exclude "Eth-Trunk[0-9]+\."\ndis device pic-status\ndis device'
    infos = DeviceNeedCheck.getDeviceInfo(cmds, multi=True)[1::]
    return infos

def dataFilterAL(infos):
    # resultPort: dict {port: [slot_num, mda_num, port_des, admin_status, link_status, logic_port]}
    resultPort = {} # dict {port: des}
    ports = infos[0].strip().split('\n')
    portTemp = ''
    for line in ports:
        m = re.split(r'\s+', line, 1)
        if len(m) > 1:
            if m[0] != '':
                resultPort[m[0]] = m[1]
                portTemp = m[0]
            else:
                resultPort[portTemp] = resultPort[portTemp]+m[1]
        elif len(m) == 1:
            resultPort[m[0]] = '-'
    status = infos[1].strip().split('\n')
    for line in status:
        m = re.search(r'((\d+)/(\d+)/\S+)\s+(\S+)\s+\S+\s+(\S+)\s+(|\d+)\s+(|\d+)\s+(-|\d+)\s+', line)
        if m:
            resultPort[m.group(1)] = [m.group(2), m.group(3), resultPort[m.group(1)], m.group(4), m.group(5), m.group(8)]
        else:
            m = re.search(r'(\d+)/(\d+)/\S+', line)
            if m:
                resultPort[m.group(0)] = [m.group(1), m.group(2), resultPort[m.group(0)], '-', '-', '-']
    # resultMda: dict{"slot_num/mda_num": [mda_type, bandwidth]}
    resultMda = {}
    slot, mda = '', ''
    for line in infos[2].strip().split('\n'):
        m = re.split(r'\s+', line)
        bwm = re.search(r'-(\d+\D+?)-', m[2])   # bandwidth
        if bwm:
            bw = bwm.group(1)
        else:
            bw = '-'
        if m[0] != '':
            slot = str(m[0])
            mda = str(m[1])
            resultMda['{}/{}'.format(slot, mda)] = [m[2], bw]
        else:
            resultMda['{}/{}'.format(slot, m[1])] = [m[2], bw]
    # dict {slot_num: slot_type}
    resultSlot = {}
    slots = infos[3].strip().split('\n')
    for line in slots:
        m = re.split(r'\s+', line)
        resultSlot[m[0]] = m[1]
    # resultLag: dict {logic_port: des}
    resultLag = {}
    lags = infos[4].strip()
    lags = re.split(r'\s+lag\s+', lags)
    for line in lags:
        line = line.replace('\n', '')
        m = re.match(r'(\d+)\D+description\s+"(.*?)"', line)
        if m:
            resultLag[m[1]] = m[2]
    return resultPort, resultMda, resultSlot, resultLag

def dataFilterHW(infos):
    resultPort = {}
    resultLag = {}  # resultLag: dict {logic_port: des}
    exp1 = re.compile(r'Eth-Trunk(\d+)\s+\S+\s+\S+\s+(\S+)')
    exp2 = re.compile(r'\D+(\d+/\d+/\d+)(\(.*?\)|)\s+\S+\s+\S+\s+(\S+|)')
    for line in infos[0].strip().split('\n'):
        m1 = re.match(exp1, line)
        m2 = re.match(exp2, line)
        if m1:
            resultLag[m1.group(1)] = m1.group(2)
        elif m2:
            if m2.group(3) == '':
                resultPort[m2.group(1)] = 'no-use'
            else:
                resultPort[m2.group(1)] = m2.group(3)
    # resultPort: dict {port: [slot_num, mda_num, port_des, admin_status, link_status, logic_port]}
    exp1 = re.compile(r'Eth-Trunk(\d+)\s')
    exp2 = re.compile(r'(\s*)\S+((\d+)/(\d+)/\d+)(\(.*?\))*\s+(\S+)\s+(\S+)')
    logicPort = ''
    for line in infos[1].strip().split('\n'):
        m1 = re.search(exp1, line)
        if m1:
            logicPort = m1.group(1)
        else:
            m2 = re.search(exp2, line)
            if m2:
                if m2.group(1) == '':
                    resultPort[m2.group(2)] = [m2.group(3), m2.group(4), resultPort[m2.group(2)], m2.group(6), m2.group(7), '-']
                else:
                    resultPort[m2.group(2)] = [m2.group(3), m2.group(4), resultPort[m2.group(2)], m2.group(6), m2.group(7), logicPort]
    # resultMda: dict {"slot_num/mda_num": [mda_type, brandwidth]}
    resultMda = {}
    for line in infos[2].strip().split('\n'):
        m = re.match(r'(\d+/\d+)\s+\S+\s+(\S+x(.*?)_\S+)\s.*?', line)
        if m:
            resultMda[m.group(1)] = [m.group(2), m.group(3)]
    # resultSlot: dict {slog_num: slot_type}
    resultSlot = {}
    for line in infos[3].strip().split('\n'):
        m = re.match(r'(\d+)\s+(\S+)\s+?', line)
        if m:
            resultSlot[m.group(1)] = m.group(2)
    return resultPort, resultMda, resultSlot, resultLag
        
def dataFilter(infos, deviceType):
    if deviceType == 'huawei':
        return dataFilterHW(infos)
    elif deviceType == 'alcatel_aos':
        return dataFilterAL(infos)
    else:
        print('Device Not Support yet.')
        return []

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
    
    # 准备记录表
    tableInfo['db'] = 'cmdb'
    tableInfo['tb'] = 'networkresource_ipmanresource'
    ResourceTable = SqlTable(**tableInfo)
    ResourceTable.executeCmd('truncate table %s' % ResourceTable._tb)

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
            print('\r- Information collecting...', end='', flush=True)
            infos = getDeviceFeedBack(DeviceNeedCheck)
            if infos != [''] and infos != '':
                resultPort, resultMda, resultSlot, resultLag = dataFilter(infos, deviceInfo['deviceType'])
                for port in resultPort:
                    '''
                        字典信息
                        resultPort: {port: [slot_num, mda_num, port_des, admin_status, link_status, logic_port]}
                        resultMda: {"slot_num/mda_num": [mda_type, bandwidth]}
                        resultSlot: {slot_num: slot_type}
                        resultLag: {logic_port: des}
                    '''
                    portData = resultPort[port]
                    slot_num, mda_num = portData[0], portData[1]
                    slot_mda = '{}/{}'.format(slot_num, mda_num)
                    # lag 信息异常处理
                    lag_des = ''
                    if portData[5] in resultLag:
                        lag_des = resultLag[portData[5]]
                    else:
                        lag_des = '-'
                    # slot 信息异常处理，华为0/0/0端口没有对应slot mda信息
                    slot_type = ''
                    if slot_num in resultSlot:
                        slot_type = resultSlot[slot_num]
                    else:
                        slot_type = '-'
                    # mda 信息异常处理，华为0/0/0端口没有对应slot mda信息
                    mda_type = []
                    if slot_mda in resultMda:
                        mda_type = resultMda[slot_mda]
                    else:
                        mda_type = ['-', '-']
                    data =  ('"%s"'%d for d in [DeviceNeedCheck._deviceName, slot_num, slot_type, mda_num, mda_type[0], port, mda_type[1], portData[3], portData[4], portData[5], lag_des, portData[2]])
                    # print(data)
                    cmd = 'insert into {}(device_name, slot, slot_type, mda, mda_type, port, brand_width, port_status, port_phy_status, logic_port, logic_port_description, port_description) values ({})'.format(*(ResourceTable._tb, ','.join(data)))
                    ResourceTable.executeCmd(cmd)
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
