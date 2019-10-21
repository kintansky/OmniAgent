#-*- coding:utf-8 -*-
from pysnmp.hlapi import *


'''
LOG
'''




'''
SNMP
'''
class SnmpWorker:
    def __init__(self, authData, host, mibNodeSet, mibSource):
        self.__varBinds = self.__constructVarBinds(mibNodeSet, mibSource)
        # print(self.varBinds)
        self.g = nextCmd(
            SnmpEngine(),
            authData,
            UdpTransportTarget(host, timeout=5, retries=2),
            ContextData(),
            *self.__varBinds,
            lexicographicMode=False,    # True则会轮询至最后的Node
        )

    def __constructVarBinds(self, mibNodeSet, mibSource):  # 构造mibset，用于多个mib同时取出
        varBinds = []
        for mibNode in mibNodeSet:
            mibSource = mibNode[2]
            print(mibSource)
            if mibSource == '':
                varBinds.append(ObjectType(ObjectIdentity(*mibNode[0:2])))
            else:
                varBinds.append(ObjectType(ObjectIdentity(*mibNode[0:2]).addMibSource(mibSource)))
        return varBinds

    def requestSnmp(self):
        result = []
        while True:
            try:
                errorIndication, errorStatus, errorIndex, values = next(self.g)
                if errorIndication:
                    print(errorIndication)
                    break
                elif errorStatus:
                    print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and values[int(errorIndex)-1][0] or '?'))
                    break
                else:
                    data = tuple()
                    for varBind in values:
                        data += tuple(x.prettyPrint() for x in varBind)
                    result.append(data)
            except StopIteration:
                break
            except KeyboardInterrupt:
                break
        return result
