import xlwt
import mysql.connector
from functools import wraps
from IPy import IP, IPSet
import os

BASE_SAVE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

def getSubnet(ip, mask):
    subnet = IP(ip).make_net(mask)
    return subnet

def writeXls(book, sheetName, titles, datas):
    sheet = book.add_sheet(sheetName)
    col = 0
    for t in titles:
        sheet.write(0, col, t)
        col += 1
    row = 1
    for info in datas:
        col = 0
        for data in info:
            sheet.write(row, col, data)
            col += 1
        row += 1
    return book


if __name__ == "__main__":
    tableInfo = {
        'tb': 'watchdog_publicipsegment',
        # 'host': 'localhost',
        'host': '10.243.24.174',
        'port': 9003,
        'user': 'root',
        'password': 'hlw2018!@#',
        'db': 'omni_agent',
    }
    # 公网地址段
    SegmentTable = SqlTable(**tableInfo)
    cmd = 'select * from {}'.format(SegmentTable._tb)
    segdata = SegmentTable.queryResult(cmd)
    ipsetDict = {}  # 地址段类型: IPSet(...)
    for gw in segdata:
        if str(gw[3]) not in ipsetDict:
            ipsetDict[str(gw[3])] = IPSet()
        subnet = getSubnet(gw[1], gw[2])
        ipsetDict[str(gw[3])].add(subnet)

    # IP 清单
    tableInfo['db'] = 'cmdb'
    tableInfo['tb'] = 'networkresource_iprecord'
    IPTable = SqlTable(**tableInfo)
    cmd = 'select device_ip, ip_mask, device_name, logic_port, svlan, cvlan, ip_description, gateway, ip_func  from {}'.format(IPTable._tb)
    ips = IPTable.queryResult(cmd)

    result = {}
    for segment_type in ipsetDict:
        result[segment_type] = []
    if '-1' not in result:
        result['-1'] = []
    for ip in ips:
        public = False
        for segment_type in ipsetDict:
            s = ipsetDict[segment_type]
            if IP(ip[0]) in s:
                result[segment_type].append(ip)
                public = True
                break
        if public is False:
            result['-1'].append(ip)

    # 写入
    bk = xlwt.Workbook()
    titles = ('ip', '掩码', '设备', '逻辑端口', '外层vlan', '内层vlan', '描述', '网关', '类型')
    idx = {'-1': '私网', '1': '公网外部使用', '2': '公网内部使用'}
    for t in result:
        bk = writeXls(bk, idx[t], titles, result[t])
    filepath = os.path.join(BASE_SAVE_DIR, 'collected_static/downloads/files/iprecord_all.xls')
    bk.save(filepath)
