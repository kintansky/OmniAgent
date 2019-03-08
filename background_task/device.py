#-*- coding:utf-8 -*-

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
import mysql.connector
from functools import wraps
import logging
import logging.handlers
import os, sys

funcDirection = sys.path[0]
fatherDirection = os.path.split(funcDirection)
os.chdir(fatherDirection[0])

class ActionLogger:
    def __init__(self, logLevel=logging.INFO, logFile='bk_error.log', printable=False):
        self.logger = logging.getLogger('bk_error_log')
        self.logger.setLevel(logLevel)
        self.__rh = logging.handlers.RotatingFileHandler(logFile, encoding='utf8', maxBytes=10 * 1024 * 1024, backupCount=1)
        self.__rh.setLevel(logLevel)
        self.__formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        self.__rh.setFormatter(self.__formatter)
        self.logger.addHandler(self.__rh)
        if printable:
            self.__ch = logging.StreamHandler()
            self.__ch.setLevel(logging.INFO)    # 注意输出的层次INFO、ERROR...
            self.__ch.setFormatter(self.__formatter)
            self.logger.addHandler(self.__ch)
    
    def infoLog(self, infoString):
        self.logger.info(infoString)
    
    def errorLog(self, errorString):
        self.logger.error(errorString)

# stastic variable
LOG = ActionLogger(printable=True)

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
            # print('- Login timeout.')
            LOG.errorLog('Login timeout: {}, {}'.format(self._deviceName, self._deviceLoginInfo['ip']))
            return ''
        except NetMikoAuthenticationException:
            # print('- Username or Password error.')
            LOG.errorLog('Invalid username or password: {}, {}, {}'.format(self._deviceName, self._deviceLoginInfo['ip'], self._deviceLoginInfo['username']))
            return ''
        except Exception as err:
            # print('- Device error: {}'.format(err))
            LOG.errorLog('Device error: {}'.format(err))
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
                LOG.errorLog('Device error: {}'.format(err))
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
    def executeCmd(self, cmd, fill=None):
        if fill is None:
            self._cur.execute(cmd)
        else:
            self._cur.execute(cmd, fill)
        
    def initCursor(self):
        self._cur = self._conn.cursor()
        
    def commitConnection(self):
        self._cur.close()
        self._conn.commit()
    '''
    如果希望多行一次提交，则不要使用方法executeCmd(...)
    通过以下格式可实现多行一起提交
    initCursor()
    _cur.execute(...)
    _cur.execute(...)
    ...
    commitConnection()
    '''
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

