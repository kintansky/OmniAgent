#
# PySNMP MIB module P-BRIDGE-MIB (http://snmplabs.com/pysmi)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/P-BRIDGE-MIB
# Produced by pysmi-0.3.4 at Fri Jun 21 09:01:22 2019
# On host ? platform ? version ? by user ?
# Using Python version 3.6.8 (tags/v3.6.8:3c6b436a57, Dec 24 2018, 00:16:47) [MSC v.1916 64 bit (AMD64)]
#
OctetString, Integer, ObjectIdentifier = mibBuilder.importSymbols("ASN1", "OctetString", "Integer", "ObjectIdentifier")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ValueSizeConstraint, ConstraintsUnion, ValueRangeConstraint, ConstraintsIntersection, SingleValueConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueSizeConstraint", "ConstraintsUnion", "ValueRangeConstraint", "ConstraintsIntersection", "SingleValueConstraint")
dot1dBasePortEntry, dot1dBasePort, dot1dTpPort, dot1dTp, dot1dBridge = mibBuilder.importSymbols("BRIDGE-MIB", "dot1dBasePortEntry", "dot1dBasePort", "dot1dTpPort", "dot1dTp", "dot1dBridge")
ObjectGroup, NotificationGroup, ModuleCompliance = mibBuilder.importSymbols("SNMPv2-CONF", "ObjectGroup", "NotificationGroup", "ModuleCompliance")
Counter32, Unsigned32, iso, Bits, NotificationType, MibIdentifier, TimeTicks, IpAddress, Gauge32, ObjectIdentity, ModuleIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, Counter64, Integer32 = mibBuilder.importSymbols("SNMPv2-SMI", "Counter32", "Unsigned32", "iso", "Bits", "NotificationType", "MibIdentifier", "TimeTicks", "IpAddress", "Gauge32", "ObjectIdentity", "ModuleIdentity", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Counter64", "Integer32")
TimeInterval, MacAddress, TextualConvention, TruthValue, DisplayString = mibBuilder.importSymbols("SNMPv2-TC", "TimeInterval", "MacAddress", "TextualConvention", "TruthValue", "DisplayString")
pBridgeMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 17, 6))
pBridgeMIB.setRevisions(('2006-01-09 00:00', '1999-08-25 00:00',))
if mibBuilder.loadTexts: pBridgeMIB.setLastUpdated('200601090000Z')
if mibBuilder.loadTexts: pBridgeMIB.setOrganization('IETF Bridge MIB Working Group')
pBridgeMIBObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 17, 6, 1))
class EnabledStatus(TextualConvention, Integer32):
    status = 'current'
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2))
    namedValues = NamedValues(("enabled", 1), ("disabled", 2))

dot1dExtBase = MibIdentifier((1, 3, 6, 1, 2, 1, 17, 6, 1, 1))
dot1dPriority = MibIdentifier((1, 3, 6, 1, 2, 1, 17, 6, 1, 2))
dot1dGarp = MibIdentifier((1, 3, 6, 1, 2, 1, 17, 6, 1, 3))
dot1dGmrp = MibIdentifier((1, 3, 6, 1, 2, 1, 17, 6, 1, 4))
dot1dDeviceCapabilities = MibScalar((1, 3, 6, 1, 2, 1, 17, 6, 1, 1, 1), Bits().clone(namedValues=NamedValues(("dot1dExtendedFilteringServices", 0), ("dot1dTrafficClasses", 1), ("dot1qStaticEntryIndividualPort", 2), ("dot1qIVLCapable", 3), ("dot1qSVLCapable", 4), ("dot1qHybridCapable", 5), ("dot1qConfigurablePvidTagging", 6), ("dot1dLocalVlanCapable", 7)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: dot1dDeviceCapabilities.setStatus('current')
dot1dTrafficClassesEnabled = MibScalar((1, 3, 6, 1, 2, 1, 17, 6, 1, 1, 2), TruthValue().clone('true')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: dot1dTrafficClassesEnabled.setStatus('current')
dot1dGmrpStatus = MibScalar((1, 3, 6, 1, 2, 1, 17, 6, 1, 1, 3), EnabledStatus().clone('enabled')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: dot1dGmrpStatus.setStatus('current')
dot1dPortCapabilitiesTable = MibTable((1, 3, 6, 1, 2, 1, 17, 6, 1, 1, 4), )
if mibBuilder.loadTexts: dot1dPortCapabilitiesTable.setStatus('current')
dot1dPortCapabilitiesEntry = MibTableRow((1, 3, 6, 1, 2, 1, 17, 6, 1, 1, 4, 1), )
dot1dBasePortEntry.registerAugmentions(("P-BRIDGE-MIB", "dot1dPortCapabilitiesEntry"))
dot1dPortCapabilitiesEntry.setIndexNames(*dot1dBasePortEntry.getIndexNames())
if mibBuilder.loadTexts: dot1dPortCapabilitiesEntry.setStatus('current')
dot1dPortCapabilities = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 6, 1, 1, 4, 1, 1), Bits().clone(namedValues=NamedValues(("dot1qDot1qTagging", 0), ("dot1qConfigurableAcceptableFrameTypes", 1), ("dot1qIngressFiltering", 2)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: dot1dPortCapabilities.setStatus('current')
dot1dPortPriorityTable = MibTable((1, 3, 6, 1, 2, 1, 17, 6, 1, 2, 1), )
if mibBuilder.loadTexts: dot1dPortPriorityTable.setStatus('current')
dot1dPortPriorityEntry = MibTableRow((1, 3, 6, 1, 2, 1, 17, 6, 1, 2, 1, 1), )
dot1dBasePortEntry.registerAugmentions(("P-BRIDGE-MIB", "dot1dPortPriorityEntry"))
dot1dPortPriorityEntry.setIndexNames(*dot1dBasePortEntry.getIndexNames())
if mibBuilder.loadTexts: dot1dPortPriorityEntry.setStatus('current')
dot1dPortDefaultUserPriority = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 6, 1, 2, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 7))).setMaxAccess("readwrite")
if mibBuilder.loadTexts: dot1dPortDefaultUserPriority.setStatus('current')
dot1dPortNumTrafficClasses = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 6, 1, 2, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 8))).setMaxAccess("readwrite")
if mibBuilder.loadTexts: dot1dPortNumTrafficClasses.setStatus('current')
dot1dUserPriorityRegenTable = MibTable((1, 3, 6, 1, 2, 1, 17, 6, 1, 2, 2), )
if mibBuilder.loadTexts: dot1dUserPriorityRegenTable.setStatus('current')
dot1dUserPriorityRegenEntry = MibTableRow((1, 3, 6, 1, 2, 1, 17, 6, 1, 2, 2, 1), ).setIndexNames((0, "BRIDGE-MIB", "dot1dBasePort"), (0, "P-BRIDGE-MIB", "dot1dUserPriority"))
if mibBuilder.loadTexts: dot1dUserPriorityRegenEntry.setStatus('current')
dot1dUserPriority = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 6, 1, 2, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 7)))
if mibBuilder.loadTexts: dot1dUserPriority.setStatus('current')
dot1dRegenUserPriority = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 6, 1, 2, 2, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 7))).setMaxAccess("readwrite")
if mibBuilder.loadTexts: dot1dRegenUserPriority.setStatus('current')
dot1dTrafficClassTable = MibTable((1, 3, 6, 1, 2, 1, 17, 6, 1, 2, 3), )
if mibBuilder.loadTexts: dot1dTrafficClassTable.setStatus('current')
dot1dTrafficClassEntry = MibTableRow((1, 3, 6, 1, 2, 1, 17, 6, 1, 2, 3, 1), ).setIndexNames((0, "BRIDGE-MIB", "dot1dBasePort"), (0, "P-BRIDGE-MIB", "dot1dTrafficClassPriority"))
if mibBuilder.loadTexts: dot1dTrafficClassEntry.setStatus('current')
dot1dTrafficClassPriority = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 6, 1, 2, 3, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 7)))
if mibBuilder.loadTexts: dot1dTrafficClassPriority.setStatus('current')
dot1dTrafficClass = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 6, 1, 2, 3, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 7))).setMaxAccess("readwrite")
if mibBuilder.loadTexts: dot1dTrafficClass.setStatus('current')
dot1dPortOutboundAccessPriorityTable = MibTable((1, 3, 6, 1, 2, 1, 17, 6, 1, 2, 4), )
if mibBuilder.loadTexts: dot1dPortOutboundAccessPriorityTable.setStatus('current')
dot1dPortOutboundAccessPriorityEntry = MibTableRow((1, 3, 6, 1, 2, 1, 17, 6, 1, 2, 4, 1), ).setIndexNames((0, "BRIDGE-MIB", "dot1dBasePort"), (0, "P-BRIDGE-MIB", "dot1dRegenUserPriority"))
if mibBuilder.loadTexts: dot1dPortOutboundAccessPriorityEntry.setStatus('current')
dot1dPortOutboundAccessPriority = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 6, 1, 2, 4, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 7))).setMaxAccess("readonly")
if mibBuilder.loadTexts: dot1dPortOutboundAccessPriority.setStatus('current')
dot1dPortGarpTable = MibTable((1, 3, 6, 1, 2, 1, 17, 6, 1, 3, 1), )
if mibBuilder.loadTexts: dot1dPortGarpTable.setStatus('current')
dot1dPortGarpEntry = MibTableRow((1, 3, 6, 1, 2, 1, 17, 6, 1, 3, 1, 1), )
dot1dBasePortEntry.registerAugmentions(("P-BRIDGE-MIB", "dot1dPortGarpEntry"))
dot1dPortGarpEntry.setIndexNames(*dot1dBasePortEntry.getIndexNames())
if mibBuilder.loadTexts: dot1dPortGarpEntry.setStatus('current')
dot1dPortGarpJoinTime = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 6, 1, 3, 1, 1, 1), TimeInterval().clone(20)).setMaxAccess("readwrite")
if mibBuilder.loadTexts: dot1dPortGarpJoinTime.setStatus('current')
dot1dPortGarpLeaveTime = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 6, 1, 3, 1, 1, 2), TimeInterval().clone(60)).setMaxAccess("readwrite")
if mibBuilder.loadTexts: dot1dPortGarpLeaveTime.setStatus('current')
dot1dPortGarpLeaveAllTime = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 6, 1, 3, 1, 1, 3), TimeInterval().clone(1000)).setMaxAccess("readwrite")
if mibBuilder.loadTexts: dot1dPortGarpLeaveAllTime.setStatus('current')
dot1dPortGmrpTable = MibTable((1, 3, 6, 1, 2, 1, 17, 6, 1, 4, 1), )
if mibBuilder.loadTexts: dot1dPortGmrpTable.setStatus('current')
dot1dPortGmrpEntry = MibTableRow((1, 3, 6, 1, 2, 1, 17, 6, 1, 4, 1, 1), )
dot1dBasePortEntry.registerAugmentions(("P-BRIDGE-MIB", "dot1dPortGmrpEntry"))
dot1dPortGmrpEntry.setIndexNames(*dot1dBasePortEntry.getIndexNames())
if mibBuilder.loadTexts: dot1dPortGmrpEntry.setStatus('current')
dot1dPortGmrpStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 6, 1, 4, 1, 1, 1), EnabledStatus().clone('enabled')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: dot1dPortGmrpStatus.setStatus('current')
dot1dPortGmrpFailedRegistrations = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 6, 1, 4, 1, 1, 2), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: dot1dPortGmrpFailedRegistrations.setStatus('current')
dot1dPortGmrpLastPduOrigin = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 6, 1, 4, 1, 1, 3), MacAddress()).setMaxAccess("readonly")
if mibBuilder.loadTexts: dot1dPortGmrpLastPduOrigin.setStatus('current')
dot1dPortRestrictedGroupRegistration = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 6, 1, 4, 1, 1, 4), TruthValue().clone('false')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: dot1dPortRestrictedGroupRegistration.setStatus('current')
dot1dTpHCPortTable = MibTable((1, 3, 6, 1, 2, 1, 17, 4, 5), )
if mibBuilder.loadTexts: dot1dTpHCPortTable.setStatus('current')
dot1dTpHCPortEntry = MibTableRow((1, 3, 6, 1, 2, 1, 17, 4, 5, 1), ).setIndexNames((0, "BRIDGE-MIB", "dot1dTpPort"))
if mibBuilder.loadTexts: dot1dTpHCPortEntry.setStatus('current')
dot1dTpHCPortInFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 4, 5, 1, 1), Counter64()).setMaxAccess("readonly")
if mibBuilder.loadTexts: dot1dTpHCPortInFrames.setStatus('current')
dot1dTpHCPortOutFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 4, 5, 1, 2), Counter64()).setMaxAccess("readonly")
if mibBuilder.loadTexts: dot1dTpHCPortOutFrames.setStatus('current')
dot1dTpHCPortInDiscards = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 4, 5, 1, 3), Counter64()).setMaxAccess("readonly")
if mibBuilder.loadTexts: dot1dTpHCPortInDiscards.setStatus('current')
dot1dTpPortOverflowTable = MibTable((1, 3, 6, 1, 2, 1, 17, 4, 6), )
if mibBuilder.loadTexts: dot1dTpPortOverflowTable.setStatus('current')
dot1dTpPortOverflowEntry = MibTableRow((1, 3, 6, 1, 2, 1, 17, 4, 6, 1), ).setIndexNames((0, "BRIDGE-MIB", "dot1dTpPort"))
if mibBuilder.loadTexts: dot1dTpPortOverflowEntry.setStatus('current')
dot1dTpPortInOverflowFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 4, 6, 1, 1), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: dot1dTpPortInOverflowFrames.setStatus('current')
dot1dTpPortOutOverflowFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 4, 6, 1, 2), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: dot1dTpPortOutOverflowFrames.setStatus('current')
dot1dTpPortInOverflowDiscards = MibTableColumn((1, 3, 6, 1, 2, 1, 17, 4, 6, 1, 3), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: dot1dTpPortInOverflowDiscards.setStatus('current')
pBridgeConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 17, 6, 2))
pBridgeGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 17, 6, 2, 1))
pBridgeCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 17, 6, 2, 2))
pBridgeExtCapGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 17, 6, 2, 1, 1)).setObjects(("P-BRIDGE-MIB", "dot1dDeviceCapabilities"), ("P-BRIDGE-MIB", "dot1dPortCapabilities"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    pBridgeExtCapGroup = pBridgeExtCapGroup.setStatus('current')
pBridgeDeviceGmrpGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 17, 6, 2, 1, 2)).setObjects(("P-BRIDGE-MIB", "dot1dGmrpStatus"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    pBridgeDeviceGmrpGroup = pBridgeDeviceGmrpGroup.setStatus('current')
pBridgeDevicePriorityGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 17, 6, 2, 1, 3)).setObjects(("P-BRIDGE-MIB", "dot1dTrafficClassesEnabled"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    pBridgeDevicePriorityGroup = pBridgeDevicePriorityGroup.setStatus('current')
pBridgeDefaultPriorityGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 17, 6, 2, 1, 4)).setObjects(("P-BRIDGE-MIB", "dot1dPortDefaultUserPriority"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    pBridgeDefaultPriorityGroup = pBridgeDefaultPriorityGroup.setStatus('current')
pBridgeRegenPriorityGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 17, 6, 2, 1, 5)).setObjects(("P-BRIDGE-MIB", "dot1dRegenUserPriority"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    pBridgeRegenPriorityGroup = pBridgeRegenPriorityGroup.setStatus('current')
pBridgePriorityGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 17, 6, 2, 1, 6)).setObjects(("P-BRIDGE-MIB", "dot1dPortNumTrafficClasses"), ("P-BRIDGE-MIB", "dot1dTrafficClass"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    pBridgePriorityGroup = pBridgePriorityGroup.setStatus('current')
pBridgeAccessPriorityGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 17, 6, 2, 1, 7)).setObjects(("P-BRIDGE-MIB", "dot1dPortOutboundAccessPriority"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    pBridgeAccessPriorityGroup = pBridgeAccessPriorityGroup.setStatus('current')
pBridgePortGarpGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 17, 6, 2, 1, 8)).setObjects(("P-BRIDGE-MIB", "dot1dPortGarpJoinTime"), ("P-BRIDGE-MIB", "dot1dPortGarpLeaveTime"), ("P-BRIDGE-MIB", "dot1dPortGarpLeaveAllTime"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    pBridgePortGarpGroup = pBridgePortGarpGroup.setStatus('current')
pBridgePortGmrpGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 17, 6, 2, 1, 9)).setObjects(("P-BRIDGE-MIB", "dot1dPortGmrpStatus"), ("P-BRIDGE-MIB", "dot1dPortGmrpFailedRegistrations"), ("P-BRIDGE-MIB", "dot1dPortGmrpLastPduOrigin"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    pBridgePortGmrpGroup = pBridgePortGmrpGroup.setStatus('deprecated')
pBridgeHCPortGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 17, 6, 2, 1, 10)).setObjects(("P-BRIDGE-MIB", "dot1dTpHCPortInFrames"), ("P-BRIDGE-MIB", "dot1dTpHCPortOutFrames"), ("P-BRIDGE-MIB", "dot1dTpHCPortInDiscards"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    pBridgeHCPortGroup = pBridgeHCPortGroup.setStatus('current')
pBridgePortOverflowGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 17, 6, 2, 1, 11)).setObjects(("P-BRIDGE-MIB", "dot1dTpPortInOverflowFrames"), ("P-BRIDGE-MIB", "dot1dTpPortOutOverflowFrames"), ("P-BRIDGE-MIB", "dot1dTpPortInOverflowDiscards"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    pBridgePortOverflowGroup = pBridgePortOverflowGroup.setStatus('current')
pBridgePortGmrpGroup2 = ObjectGroup((1, 3, 6, 1, 2, 1, 17, 6, 2, 1, 12)).setObjects(("P-BRIDGE-MIB", "dot1dPortGmrpStatus"), ("P-BRIDGE-MIB", "dot1dPortGmrpFailedRegistrations"), ("P-BRIDGE-MIB", "dot1dPortGmrpLastPduOrigin"), ("P-BRIDGE-MIB", "dot1dPortRestrictedGroupRegistration"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    pBridgePortGmrpGroup2 = pBridgePortGmrpGroup2.setStatus('current')
pBridgeCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 17, 6, 2, 2, 1)).setObjects(("P-BRIDGE-MIB", "pBridgeExtCapGroup"), ("P-BRIDGE-MIB", "pBridgeDeviceGmrpGroup"), ("P-BRIDGE-MIB", "pBridgeDevicePriorityGroup"), ("P-BRIDGE-MIB", "pBridgeDefaultPriorityGroup"), ("P-BRIDGE-MIB", "pBridgeRegenPriorityGroup"), ("P-BRIDGE-MIB", "pBridgePriorityGroup"), ("P-BRIDGE-MIB", "pBridgeAccessPriorityGroup"), ("P-BRIDGE-MIB", "pBridgePortGarpGroup"), ("P-BRIDGE-MIB", "pBridgePortGmrpGroup"), ("P-BRIDGE-MIB", "pBridgeHCPortGroup"), ("P-BRIDGE-MIB", "pBridgePortOverflowGroup"))

if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    pBridgeCompliance = pBridgeCompliance.setStatus('deprecated')
pBridgeCompliance2 = ModuleCompliance((1, 3, 6, 1, 2, 1, 17, 6, 2, 2, 2)).setObjects(("P-BRIDGE-MIB", "pBridgeExtCapGroup"), ("P-BRIDGE-MIB", "pBridgeDeviceGmrpGroup"), ("P-BRIDGE-MIB", "pBridgeDevicePriorityGroup"), ("P-BRIDGE-MIB", "pBridgeDefaultPriorityGroup"), ("P-BRIDGE-MIB", "pBridgeRegenPriorityGroup"), ("P-BRIDGE-MIB", "pBridgePriorityGroup"), ("P-BRIDGE-MIB", "pBridgeAccessPriorityGroup"), ("P-BRIDGE-MIB", "pBridgePortGarpGroup"), ("P-BRIDGE-MIB", "pBridgePortGmrpGroup2"), ("P-BRIDGE-MIB", "pBridgeHCPortGroup"), ("P-BRIDGE-MIB", "pBridgePortOverflowGroup"))

if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    pBridgeCompliance2 = pBridgeCompliance2.setStatus('current')
mibBuilder.exportSymbols("P-BRIDGE-MIB", dot1dPortGmrpTable=dot1dPortGmrpTable, pBridgePriorityGroup=pBridgePriorityGroup, EnabledStatus=EnabledStatus, dot1dDeviceCapabilities=dot1dDeviceCapabilities, dot1dPortOutboundAccessPriorityEntry=dot1dPortOutboundAccessPriorityEntry, dot1dTpPortOutOverflowFrames=dot1dTpPortOutOverflowFrames, dot1dPortCapabilities=dot1dPortCapabilities, dot1dTpHCPortInFrames=dot1dTpHCPortInFrames, dot1dPortOutboundAccessPriority=dot1dPortOutboundAccessPriority, dot1dPortCapabilitiesTable=dot1dPortCapabilitiesTable, dot1dPortGmrpStatus=dot1dPortGmrpStatus, dot1dPortRestrictedGroupRegistration=dot1dPortRestrictedGroupRegistration, dot1dUserPriorityRegenTable=dot1dUserPriorityRegenTable, pBridgeCompliances=pBridgeCompliances, dot1dTpPortInOverflowFrames=dot1dTpPortInOverflowFrames, pBridgeDevicePriorityGroup=pBridgeDevicePriorityGroup, pBridgeAccessPriorityGroup=pBridgeAccessPriorityGroup, pBridgePortGmrpGroup=pBridgePortGmrpGroup, dot1dPortPriorityEntry=dot1dPortPriorityEntry, dot1dExtBase=dot1dExtBase, dot1dTpHCPortEntry=dot1dTpHCPortEntry, pBridgeHCPortGroup=pBridgeHCPortGroup, dot1dTrafficClassesEnabled=dot1dTrafficClassesEnabled, dot1dPortGarpTable=dot1dPortGarpTable, pBridgeMIB=pBridgeMIB, pBridgeDefaultPriorityGroup=pBridgeDefaultPriorityGroup, pBridgePortOverflowGroup=pBridgePortOverflowGroup, PYSNMP_MODULE_ID=pBridgeMIB, dot1dTpHCPortInDiscards=dot1dTpHCPortInDiscards, dot1dPortOutboundAccessPriorityTable=dot1dPortOutboundAccessPriorityTable, dot1dUserPriority=dot1dUserPriority, pBridgeGroups=pBridgeGroups, dot1dPortGmrpEntry=dot1dPortGmrpEntry, pBridgeCompliance=pBridgeCompliance, dot1dTpHCPortTable=dot1dTpHCPortTable, dot1dGarp=dot1dGarp, dot1dRegenUserPriority=dot1dRegenUserPriority, dot1dPortGmrpLastPduOrigin=dot1dPortGmrpLastPduOrigin, pBridgeDeviceGmrpGroup=pBridgeDeviceGmrpGroup, pBridgePortGarpGroup=pBridgePortGarpGroup, dot1dTrafficClassPriority=dot1dTrafficClassPriority, pBridgePortGmrpGroup2=pBridgePortGmrpGroup2, pBridgeCompliance2=pBridgeCompliance2, dot1dPortGarpEntry=dot1dPortGarpEntry, dot1dPortGarpLeaveAllTime=dot1dPortGarpLeaveAllTime, dot1dPortCapabilitiesEntry=dot1dPortCapabilitiesEntry, dot1dTrafficClassEntry=dot1dTrafficClassEntry, dot1dPriority=dot1dPriority, dot1dGmrp=dot1dGmrp, dot1dTrafficClassTable=dot1dTrafficClassTable, dot1dTrafficClass=dot1dTrafficClass, pBridgeMIBObjects=pBridgeMIBObjects, dot1dTpPortOverflowTable=dot1dTpPortOverflowTable, dot1dGmrpStatus=dot1dGmrpStatus, dot1dPortDefaultUserPriority=dot1dPortDefaultUserPriority, dot1dPortGarpJoinTime=dot1dPortGarpJoinTime, dot1dTpPortOverflowEntry=dot1dTpPortOverflowEntry, dot1dTpPortInOverflowDiscards=dot1dTpPortInOverflowDiscards, pBridgeConformance=pBridgeConformance, pBridgeExtCapGroup=pBridgeExtCapGroup, dot1dTpHCPortOutFrames=dot1dTpHCPortOutFrames, dot1dUserPriorityRegenEntry=dot1dUserPriorityRegenEntry, dot1dPortPriorityTable=dot1dPortPriorityTable, pBridgeRegenPriorityGroup=pBridgeRegenPriorityGroup, dot1dPortGarpLeaveTime=dot1dPortGarpLeaveTime, dot1dPortGmrpFailedRegistrations=dot1dPortGmrpFailedRegistrations, dot1dPortNumTrafficClasses=dot1dPortNumTrafficClasses)
