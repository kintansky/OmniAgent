#-*- coding:utf-8 -*-

from device import Device, SqlTable
import re
import time
import mysql.connector

def getCommands(tableInfo, ptn):    # ptn参数支持正则表达式
    deviceCmd = {}
    CommandTable = SqlTable(**tableInfo)
    cmd = 'select * from {} where cmd_func like "{}"'.format(*(CommandTable._tb, ptn))
    result = CommandTable.queryResult(cmd)
    temp1, temp2 = [], []
    for r in result:
        manufactor = r[4]
        if manufactor not in deviceCmd:
            deviceCmd[manufactor] = [[r[1]], [r[2]]]
        else:
            deviceCmd[manufactor][0].append(r[1])
            deviceCmd[manufactor][1].append(r[2])
    return deviceCmd
    
def getDeviceFeedBack(DeviceNeedCheck, ptn):    # ptn参数支持正则表达式
    userAmount = {}
    tableInfo = {
        'tb': 'watchdog_commandline',
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'root1234',
        'db': 'omni_agent',
        }
    deviceCmd = getCommands(tableInfo, ptn)
    cmds = deviceCmd[DeviceNeedCheck._deviceLoginInfo['device_type']]
    screenSetting = ''
    if DeviceNeedCheck._deviceLoginInfo['device_type'] == 'alcatel_aos':
        screenSetting = 'environment no more\n'
    elif DeviceNeedCheck._deviceLoginInfo['device_type'] == 'huawei':
        screenSetting = 'screen-length 0 temporary\n'
    r = DeviceNeedCheck.getDeviceInfo(screenSetting+'\n'.join(cmds[1]), multi=True)[1::]
    for i in range(len(cmds[0])):
        userAmount[cmds[0][i]] = r[i]
    return userAmount # 输出结果需要根据cmdFunc进行处理

def dataFilter(userAmount):
    result = {}
    for cmdFunc in userAmount:
        line = userAmount[cmdFunc]
        result[cmdFunc] = ''
        m = re.search(r'((Total\s+users\s.*?)|(Number\sof\s.*?)):\D*(\d+).*?', line)
        if m:
            result[cmdFunc] = m.group(4)
    return result

def saveData(result, deviceName):
    tableInfo = {
        'tb': 'watchdog_deviceuseramount',
        'host': 'localhost',
        'port': 9003,
        'user': 'root',
        'password': 'hlw2018!@#',
        'db': 'omni_agent',
        }
    UserAmountTable = SqlTable(**tableInfo)
    
    idx = {
        'XM1_0': 'home_user_amount', 
        'XM1_1': 'otv_user_amount', 
        'XM1_2': 'ims_user_amount', 
        'XM1_3': 'itms_user_amount',
        }
    recordTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    title = (idx[t] for t in idx)
    data = (result[t] for t in idx)
    UserAmountTable.executeCmd('insert into {}(device_name,{},record_time) values ({},{},{})'.format(*(UserAmountTable._tb, ','.join(title), '"%s"'%deviceName, ','.join(data), '"%s"'%recordTime)))
    


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
    cmd = 'select * from {} where device_network = "IPMAN" and device_name regexp "^GDFOS-MS-IPMAN"'.format(DeviceInfoTable._tb)
    deviceList = DeviceInfoTable.queryResult(cmd)
    DeviceInfoTable = None
    del DeviceInfoTable
    
    i = 0
    for d in deviceList[0:2]:
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
            userAmount = getDeviceFeedBack(DeviceNeedCheck, 'XM1_%')
            print('\r- Data filtering...', end='', flush=True)
            result = dataFilter(userAmount)
            if result != {}:    # 这里判断方法可能判断不了空
                print('\r- Writing database...', end='', flush=True)
                print(result)
                # saveData(result, DeviceNeedCheck._deviceName)
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
        
