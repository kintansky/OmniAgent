#
# PySNMP MIB module RMON2-MIB (http://snmplabs.com/pysmi)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/RMON2-MIB
# Produced by pysmi-0.3.4 at Fri Jun 21 11:44:01 2019
# On host ? platform ? version ? by user ?
# Using Python version 3.6.8 (tags/v3.6.8:3c6b436a57, Dec 24 2018, 00:16:47) [MSC v.1916 64 bit (AMD64)]
#
Integer, OctetString, ObjectIdentifier = mibBuilder.importSymbols("ASN1", "Integer", "OctetString", "ObjectIdentifier")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
SingleValueConstraint, ValueRangeConstraint, ConstraintsIntersection, ConstraintsUnion, ValueSizeConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "SingleValueConstraint", "ValueRangeConstraint", "ConstraintsIntersection", "ConstraintsUnion", "ValueSizeConstraint")
ifIndex, = mibBuilder.importSymbols("IF-MIB", "ifIndex")
history, matrix, filter, filterEntry, OwnerString, matrixControlEntry, etherStatsEntry, statistics, channelEntry, hostControlEntry, historyControlEntry, hosts = mibBuilder.importSymbols("RMON-MIB", "history", "matrix", "filter", "filterEntry", "OwnerString", "matrixControlEntry", "etherStatsEntry", "statistics", "channelEntry", "hostControlEntry", "historyControlEntry", "hosts")
ModuleCompliance, NotificationGroup, ObjectGroup = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "NotificationGroup", "ObjectGroup")
iso, mib_2, Bits, IpAddress, Counter64, NotificationType, ObjectIdentity, TimeTicks, Unsigned32, MibScalar, MibTable, MibTableRow, MibTableColumn, MibIdentifier, ModuleIdentity, Integer32, Gauge32, Counter32 = mibBuilder.importSymbols("SNMPv2-SMI", "iso", "mib-2", "Bits", "IpAddress", "Counter64", "NotificationType", "ObjectIdentity", "TimeTicks", "Unsigned32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "MibIdentifier", "ModuleIdentity", "Integer32", "Gauge32", "Counter32")
DisplayString, TextualConvention, RowStatus, TimeStamp = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention", "RowStatus", "TimeStamp")
rmon = ModuleIdentity((1, 3, 6, 1, 2, 1, 16))
if mibBuilder.loadTexts: rmon.setLastUpdated('9605270000Z')
if mibBuilder.loadTexts: rmon.setOrganization('IETF RMON MIB Working Group')
protocolDir = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 11))
protocolDist = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 12))
addressMap = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 13))
nlHost = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 14))
nlMatrix = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 15))
alHost = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 16))
alMatrix = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 17))
usrHistory = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 18))
probeConfig = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 19))
rmonConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 20))
class ZeroBasedCounter32(TextualConvention, Gauge32):
    status = 'current'

class LastCreateTime(TimeStamp):
    status = 'current'

class TimeFilter(TextualConvention, TimeTicks):
    status = 'current'

class DataSource(TextualConvention, ObjectIdentifier):
    status = 'current'

mibBuilder.exportSymbols("RMON2-MIB", protocolDir=protocolDir, PYSNMP_MODULE_ID=rmon, nlMatrix=nlMatrix, alHost=alHost, probeConfig=probeConfig, rmonConformance=rmonConformance, DataSource=DataSource, ZeroBasedCounter32=ZeroBasedCounter32, alMatrix=alMatrix, usrHistory=usrHistory, TimeFilter=TimeFilter, rmon=rmon, nlHost=nlHost, LastCreateTime=LastCreateTime, addressMap=addressMap, protocolDist=protocolDist)
