#
# PySNMP MIB module HUAWEI-CPU-MIB (http://snmplabs.com/pysmi)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/HUAWEI-CPU-MIB
# Produced by pysmi-0.3.4 at Thu Jun 20 22:25:05 2019
# On host ? platform ? version ? by user ?
# Using Python version 3.6.8 (tags/v3.6.8:3c6b436a57, Dec 24 2018, 00:16:47) [MSC v.1916 64 bit (AMD64)]
#
OctetString, ObjectIdentifier, Integer = mibBuilder.importSymbols("ASN1", "OctetString", "ObjectIdentifier", "Integer")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ConstraintsUnion, ValueRangeConstraint, SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsUnion", "ValueRangeConstraint", "SingleValueConstraint", "ConstraintsIntersection", "ValueSizeConstraint")
hwFrameIndex, hwSlotIndex = mibBuilder.importSymbols("HUAWEI-DEVICE-MIB", "hwFrameIndex", "hwSlotIndex")
huaweiUtility, = mibBuilder.importSymbols("HUAWEI-MIB", "huaweiUtility")
NotificationGroup, ObjectGroup, ModuleCompliance = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ObjectGroup", "ModuleCompliance")
Gauge32, ModuleIdentity, Bits, iso, MibScalar, MibTable, MibTableRow, MibTableColumn, ObjectIdentity, Counter32, NotificationType, Unsigned32, IpAddress, TimeTicks, MibIdentifier, Counter64, Integer32 = mibBuilder.importSymbols("SNMPv2-SMI", "Gauge32", "ModuleIdentity", "Bits", "iso", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "ObjectIdentity", "Counter32", "NotificationType", "Unsigned32", "IpAddress", "TimeTicks", "MibIdentifier", "Counter64", "Integer32")
DisplayString, TextualConvention = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
hwDev = ModuleIdentity((1, 3, 6, 1, 4, 1, 2011, 6, 3))
if mibBuilder.loadTexts: hwDev.setLastUpdated('200406280900Z')
if mibBuilder.loadTexts: hwDev.setOrganization('Fix-Net Dept, Huawei Technologies Co.,Ltd.')
hwCpuDevTable = MibTable((1, 3, 6, 1, 4, 1, 2011, 6, 3, 4), )
if mibBuilder.loadTexts: hwCpuDevTable.setStatus('current')
hwCpuDevEntry = MibTableRow((1, 3, 6, 1, 4, 1, 2011, 6, 3, 4, 1), ).setIndexNames((0, "HUAWEI-DEVICE-MIB", "hwFrameIndex"), (0, "HUAWEI-DEVICE-MIB", "hwSlotIndex"), (0, "HUAWEI-CPU-MIB", "hwCpuDevIndex"))
if mibBuilder.loadTexts: hwCpuDevEntry.setStatus('current')
hwCpuDevIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 2011, 6, 3, 4, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255)))
if mibBuilder.loadTexts: hwCpuDevIndex.setStatus('current')
hwCpuDevDuty = MibTableColumn((1, 3, 6, 1, 4, 1, 2011, 6, 3, 4, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 100))).setMaxAccess("readonly")
if mibBuilder.loadTexts: hwCpuDevDuty.setStatus('current')
hwAvgDuty1min = MibTableColumn((1, 3, 6, 1, 4, 1, 2011, 6, 3, 4, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 100))).setMaxAccess("readonly")
if mibBuilder.loadTexts: hwAvgDuty1min.setStatus('current')
hwAvgDuty5min = MibTableColumn((1, 3, 6, 1, 4, 1, 2011, 6, 3, 4, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 100))).setMaxAccess("readonly")
if mibBuilder.loadTexts: hwAvgDuty5min.setStatus('current')
mibBuilder.exportSymbols("HUAWEI-CPU-MIB", hwCpuDevEntry=hwCpuDevEntry, PYSNMP_MODULE_ID=hwDev, hwCpuDevIndex=hwCpuDevIndex, hwDev=hwDev, hwCpuDevTable=hwCpuDevTable, hwAvgDuty1min=hwAvgDuty1min, hwCpuDevDuty=hwCpuDevDuty, hwAvgDuty5min=hwAvgDuty5min)
