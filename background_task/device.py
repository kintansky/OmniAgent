#-*- coding:utf-8 -*-

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
import mysql.connector
from functools import wraps

class Device:
    def __init__(self, deviceName, deviceType, ip, port, username, password):
        self._deviceName = deviceName
        self._deviceLoginInfo = {
            'device_type': deviceType,
            'ip': ip,
            'port': port,
            'username': username,
            'password': password
                }
    
    def getDeviceInfo(self, cmd, multi=False):  # multi为True可返回多结果列表
        try:
            connection = ConnectHandler(**self._deviceLoginInfo)
        except NetMikoTimeoutException:
            print('- Login timeout.')
            return ''
        except NetMikoAuthenticationException:
            print('- Username or Password error.')
            return ''
        except Exception as err:
            print('- Device error: {}'.format(err))
            return ''
        else:
            try:
                if multi:
                    stdout = []
                    for line in cmd.split('\n'):
                        stdout.append(connection.send_command(line))
                else:
                    stdout = ''
                    for line in cmd.split('\n'):
                        stdout = connection.send_command(line)
                return stdout
            except Exception as err:
                print(err)
                return ''
            finally:
                connection.disconnect()

class SqlDatabase:
    def __init__(self, host, port, user, password, db):
        self.__loginInfo = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
                }
        self._conn = mysql.connector.connect(**self.__loginInfo)
        self._cur = self._conn.cursor()
        self.executeCmd("use %s" % db)
        self._cur.close()
        
    def cursorDecorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.initCursor()
            result = func(self, *args, **kwargs)    # queryResult 需要获取返回值
            self.commitConnection()
            return result
        return wrapper
        
    @cursorDecorator
    def executeCmd(self, cmd):
        self._cur.execute(cmd)
        
    def initCursor(self):
        self._cur = self._conn.cursor()
        
    def commitConnection(self):
        self._cur.close()
        self._conn.commit()
    
    @cursorDecorator
    def queryResult(self, cmd):
        result = []
        self._cur.execute(cmd)
        result = self._cur.fetchall()
        return result
    
    def __del__(self):
        self._conn.close()
        

class SqlTable(SqlDatabase):
    def __init__(self, tb, host, port, user, password, db):
        self._tb = tb
        SqlDatabase.__init__(self, host, port, user, password, db)

