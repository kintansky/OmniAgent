#
# PySNMP MIB module HUAWEI-MEMORY-MIB (http://snmplabs.com/pysmi)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/HUAWEI-MEMORY-MIB
# Produced by pysmi-0.3.4 at Thu Jun 20 22:26:22 2019
# On host ? platform ? version ? by user ?
# Using Python version 3.6.8 (tags/v3.6.8:3c6b436a57, Dec 24 2018, 00:16:47) [MSC v.1916 64 bit (AMD64)]
#
Integer, OctetString, ObjectIdentifier = mibBuilder.importSymbols("ASN1", "Integer", "OctetString", "ObjectIdentifier")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ValueRangeConstraint, ConstraintsUnion, ValueSizeConstraint, SingleValueConstraint, ConstraintsIntersection = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueRangeConstraint", "ConstraintsUnion", "ValueSizeConstraint", "SingleValueConstraint", "ConstraintsIntersection")
hwSlotIndex, hwFrameIndex = mibBuilder.importSymbols("HUAWEI-DEVICE-MIB", "hwSlotIndex", "hwFrameIndex")
hwDev, = mibBuilder.importSymbols("HUAWEI-MIB", "hwDev")
ModuleCompliance, NotificationGroup, ObjectGroup = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "NotificationGroup", "ObjectGroup")
Counter64, Counter32, Gauge32, Integer32, TimeTicks, IpAddress, iso, ObjectIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, Unsigned32, Bits, NotificationType, MibIdentifier, ModuleIdentity = mibBuilder.importSymbols("SNMPv2-SMI", "Counter64", "Counter32", "Gauge32", "Integer32", "TimeTicks", "IpAddress", "iso", "ObjectIdentity", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Unsigned32", "Bits", "NotificationType", "MibIdentifier", "ModuleIdentity")
TextualConvention, DisplayString = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
hwMemoryDev = ModuleIdentity((1, 3, 6, 1, 4, 1, 2011, 6, 3, 5))
if mibBuilder.loadTexts: hwMemoryDev.setLastUpdated('200212290900Z')
if mibBuilder.loadTexts: hwMemoryDev.setOrganization('HAUWEI MIB Standard community ')
hwMemoryDevTable = MibTable((1, 3, 6, 1, 4, 1, 2011, 6, 3, 5, 1), )
if mibBuilder.loadTexts: hwMemoryDevTable.setStatus('current')
hwMemoryDevEntry = MibTableRow((1, 3, 6, 1, 4, 1, 2011, 6, 3, 5, 1, 1), ).setIndexNames((0, "HUAWEI-DEVICE-MIB", "hwFrameIndex"), (0, "HUAWEI-DEVICE-MIB", "hwSlotIndex"), (0, "HUAWEI-MEMORY-MIB", "hwMemoryDevModuleIndex"))
if mibBuilder.loadTexts: hwMemoryDevEntry.setStatus('current')
hwMemoryDevModuleIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 2011, 6, 3, 5, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)))
if mibBuilder.loadTexts: hwMemoryDevModuleIndex.setStatus('current')
hwMemoryDevSize = MibTableColumn((1, 3, 6, 1, 4, 1, 2011, 6, 3, 5, 1, 1, 2), Unsigned32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: hwMemoryDevSize.setStatus('current')
hwMemoryDevFree = MibTableColumn((1, 3, 6, 1, 4, 1, 2011, 6, 3, 5, 1, 1, 3), Unsigned32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: hwMemoryDevFree.setStatus('current')
hwMemoryDevRawSliceUsed = MibTableColumn((1, 3, 6, 1, 4, 1, 2011, 6, 3, 5, 1, 1, 4), Unsigned32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: hwMemoryDevRawSliceUsed.setStatus('current')
hwMemoryDevLargestFree = MibTableColumn((1, 3, 6, 1, 4, 1, 2011, 6, 3, 5, 1, 1, 5), Unsigned32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: hwMemoryDevLargestFree.setStatus('current')
hwMemoryDevFail = MibTableColumn((1, 3, 6, 1, 4, 1, 2011, 6, 3, 5, 1, 1, 6), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: hwMemoryDevFail.setStatus('current')
hwMemoryDevFailNoMem = MibTableColumn((1, 3, 6, 1, 4, 1, 2011, 6, 3, 5, 1, 1, 7), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: hwMemoryDevFailNoMem.setStatus('current')
hwBufferTable = MibTable((1, 3, 6, 1, 4, 1, 2011, 6, 3, 5, 2), )
if mibBuilder.loadTexts: hwBufferTable.setStatus('current')
hwBufferEntry = MibTableRow((1, 3, 6, 1, 4, 1, 2011, 6, 3, 5, 2, 1), ).setIndexNames((0, "HUAWEI-DEVICE-MIB", "hwFrameIndex"), (0, "HUAWEI-DEVICE-MIB", "hwSlotIndex"), (0, "HUAWEI-MEMORY-MIB", "hwBufferModuleIndex"), (0, "HUAWEI-MEMORY-MIB", "hwBufferSize"))
if mibBuilder.loadTexts: hwBufferEntry.setStatus('current')
hwBufferModuleIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 2011, 6, 3, 5, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)))
if mibBuilder.loadTexts: hwBufferModuleIndex.setStatus('current')
hwBufferSize = MibTableColumn((1, 3, 6, 1, 4, 1, 2011, 6, 3, 5, 2, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts: hwBufferSize.setStatus('current')
hwBufferCurrentTotal = MibTableColumn((1, 3, 6, 1, 4, 1, 2011, 6, 3, 5, 2, 1, 3), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: hwBufferCurrentTotal.setStatus('current')
hwBufferCurrentUsed = MibTableColumn((1, 3, 6, 1, 4, 1, 2011, 6, 3, 5, 2, 1, 4), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: hwBufferCurrentUsed.setStatus('current')
mibBuilder.exportSymbols("HUAWEI-MEMORY-MIB", hwMemoryDevSize=hwMemoryDevSize, hwBufferEntry=hwBufferEntry, hwMemoryDevRawSliceUsed=hwMemoryDevRawSliceUsed, hwBufferSize=hwBufferSize, hwMemoryDevEntry=hwMemoryDevEntry, hwMemoryDev=hwMemoryDev, hwBufferModuleIndex=hwBufferModuleIndex, hwMemoryDevFailNoMem=hwMemoryDevFailNoMem, hwBufferCurrentUsed=hwBufferCurrentUsed, hwMemoryDevTable=hwMemoryDevTable, PYSNMP_MODULE_ID=hwMemoryDev, hwBufferTable=hwBufferTable, hwMemoryDevModuleIndex=hwMemoryDevModuleIndex, hwMemoryDevFree=hwMemoryDevFree, hwMemoryDevLargestFree=hwMemoryDevLargestFree, hwBufferCurrentTotal=hwBufferCurrentTotal, hwMemoryDevFail=hwMemoryDevFail)
