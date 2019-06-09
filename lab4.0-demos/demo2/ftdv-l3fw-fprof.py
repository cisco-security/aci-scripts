#!/usr/bin/env python
'''
'''
# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.fv
import cobra.model.pol
import cobra.model.vns
from cobra.internal.codec.xmlcodec import toXMLStr
import sys
pod_num = int(sys.argv[1])
tenant_name = sys.argv[2]
csr_ip = sys.argv[3]

lab_prefix,owner,ownersid,ownerpod = tenant_name.split("-")
tenant_login = '%s' % tenant_name
# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://198.19.254.61', '%s' % tenant_login, 'p%s' % tenant_login)

md = cobra.mit.access.MoDirectory(ls)
md.login()

# the top level object on which operations will be made
polUni = cobra.model.pol.Uni('')
fvTenant = cobra.model.fv.Tenant(polUni, '%s' % tenant_name)
vnsAbsFuncProfContr = cobra.model.vns.AbsFuncProfContr(fvTenant)

# build the request using cobra syntax
vnsAbsFuncProfGrp = cobra.model.vns.AbsFuncProfGrp(vnsAbsFuncProfContr, ownerKey=u'', name=u'ftd-cfgs-group', descr=u'', ownerTag=u'')
vnsAbsFuncProf = cobra.model.vns.AbsFuncProf(vnsAbsFuncProfGrp, ownerKey=u'', name=u'l3fw-cfg-ftd', descr=u'', ownerTag=u'')
vnsRsProfToMFunc = cobra.model.vns.RsProfToMFunc(vnsAbsFuncProf, tDn=u'uni/infra/mDev-CISCO-FTD_FI-1.0/mFunc-FTD')
vnsAbsDevCfg = cobra.model.vns.AbsDevCfg(vnsAbsFuncProf, ownerKey=u'', name=u'devConfig', descr=u'', ownerTag=u'')
vnsAbsFolder = cobra.model.vns.AbsFolder(vnsAbsDevCfg, locked=u'no', name=u'internalInterface', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'InterfaceConfig', cardinality=u'unspecified')
vnsAbsParam = cobra.model.vns.AbsParam(vnsAbsFolder, validation=u'', mandatory=u'no', name=u'enabled', value=u'true', key=u'enabled', locked=u'no', cardinality=u'unspecified')
vnsAbsParam2 = cobra.model.vns.AbsParam(vnsAbsFolder, validation=u'', mandatory=u'no', name=u'ifname', value=u'dbnic', key=u'ifname', locked=u'no', cardinality=u'unspecified')
vnsAbsFolder2 = cobra.model.vns.AbsFolder(vnsAbsFolder, locked=u'no', name=u'IPv4Config', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'IPv4Config', cardinality=u'unspecified')
vnsAbsFolder3 = cobra.model.vns.AbsFolder(vnsAbsFolder2, locked=u'no', name=u'static', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'static', cardinality=u'unspecified')
vnsAbsParam3 = cobra.model.vns.AbsParam(vnsAbsFolder3, validation=u'', mandatory=u'no', name=u'address', value=u'10.2.0.1/24', key=u'address', locked=u'no', cardinality=u'unspecified')
vnsAbsFolder4 = cobra.model.vns.AbsFolder(vnsAbsFolder, locked=u'no', name=u'int_security_zone', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'int_security_zone', cardinality=u'unspecified')
vnsAbsCfgRel = cobra.model.vns.AbsCfgRel(vnsAbsFolder4, mandatory=u'no', name=u'security_zone', key=u'security_zone', locked=u'no', cardinality=u'unspecified', targetName=u'db-zone')
vnsAbsFolder5 = cobra.model.vns.AbsFolder(vnsAbsDevCfg, locked=u'no', name=u'app-zone', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'SecurityZone', cardinality=u'unspecified')
vnsAbsParam4 = cobra.model.vns.AbsParam(vnsAbsFolder5, validation=u'', mandatory=u'no', name=u'type', value=u'ROUTED', key=u'type', locked=u'no', cardinality=u'unspecified')
vnsAbsFolder6 = cobra.model.vns.AbsFolder(vnsAbsDevCfg, locked=u'no', name=u'ftd-policy', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessPolicy', cardinality=u'unspecified')
vnsAbsFolder7 = cobra.model.vns.AbsFolder(vnsAbsFolder6, locked=u'no', name=u'ftd-rule2', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'AccessRule', cardinality=u'unspecified')
vnsAbsParam5 = cobra.model.vns.AbsParam(vnsAbsFolder7, validation=u'', mandatory=u'no', name=u'bidirectional', value=u'true', key=u'bidirectional', locked=u'no', cardinality=u'unspecified')
vnsAbsFolder8 = cobra.model.vns.AbsFolder(vnsAbsFolder7, locked=u'no', name=u'AccDestinationZones', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'AccDestinationZones', cardinality=u'unspecified')
vnsAbsCfgRel2 = cobra.model.vns.AbsCfgRel(vnsAbsFolder8, mandatory=u'no', name=u'DestinationZones', key=u'DestinationZones', locked=u'no', cardinality=u'unspecified', targetName=u'internalInterface/int_security_zone')
vnsAbsFolder9 = cobra.model.vns.AbsFolder(vnsAbsFolder7, locked=u'no', name=u'AccSourceZones', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'AccSourceZones', cardinality=u'unspecified')
vnsAbsCfgRel3 = cobra.model.vns.AbsCfgRel(vnsAbsFolder9, mandatory=u'no', name=u'SourceZones', key=u'SourceZones', locked=u'no', cardinality=u'unspecified', targetName=u'externalInterface/int_security_zone')
vnsAbsFolder10 = cobra.model.vns.AbsFolder(vnsAbsFolder6, locked=u'no', name=u'ftd-rule1', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'AccessRule', cardinality=u'unspecified')
vnsAbsParam6 = cobra.model.vns.AbsParam(vnsAbsFolder10, validation=u'', mandatory=u'no', name=u'Bi-Directional', value=u'true', key=u'bidirectional', locked=u'no', cardinality=u'unspecified')
vnsAbsFolder11 = cobra.model.vns.AbsFolder(vnsAbsFolder10, locked=u'no', name=u'AccDestinationZones', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'AccDestinationZones', cardinality=u'unspecified')
vnsAbsCfgRel4 = cobra.model.vns.AbsCfgRel(vnsAbsFolder11, mandatory=u'no', name=u'DestinationZones', key=u'DestinationZones', locked=u'no', cardinality=u'unspecified', targetName=u'internalInterface/int_security_zone')

vnsAbsFolder12 = cobra.model.vns.AbsFolder(vnsAbsFolder10, locked=u'no', name=u'AccSourceZones', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'AccSourceZones', cardinality=u'unspecified')
vnsAbsCfgRel5 = cobra.model.vns.AbsCfgRel(vnsAbsFolder12, mandatory=u'no', name=u'SourceZone', key=u'SourceZones', locked=u'no', cardinality=u'unspecified', targetName=u'externalInterface/int_security_zone')
vnsAbsFolder13 = cobra.model.vns.AbsFolder(vnsAbsDevCfg, locked=u'no', name=u'externalInterface', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'InterfaceConfig', cardinality=u'unspecified')
vnsAbsParam7 = cobra.model.vns.AbsParam(vnsAbsFolder13, validation=u'', mandatory=u'no', name=u'enabled', value=u'true', key=u'enabled', locked=u'no', cardinality=u'unspecified')
vnsAbsParam8 = cobra.model.vns.AbsParam(vnsAbsFolder13, validation=u'', mandatory=u'no', name=u'ifname', value=u'appnic', key=u'ifname', locked=u'no', cardinality=u'unspecified')
vnsAbsFolder14 = cobra.model.vns.AbsFolder(vnsAbsFolder13, locked=u'no', name=u'IPv4Config', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'IPv4Config', cardinality=u'unspecified')
vnsAbsFolder15 = cobra.model.vns.AbsFolder(vnsAbsFolder14, locked=u'no', name=u'static', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'static', cardinality=u'unspecified')
vnsAbsParam9 = cobra.model.vns.AbsParam(vnsAbsFolder15, validation=u'', mandatory=u'no', name=u'address', value=u'10.1.0.1/16', key=u'address', locked=u'no', cardinality=u'unspecified')
vnsAbsFolder16 = cobra.model.vns.AbsFolder(vnsAbsFolder13, locked=u'no', name=u'int_security_zone', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'int_security_zone', cardinality=u'unspecified')
vnsAbsCfgRel6 = cobra.model.vns.AbsCfgRel(vnsAbsFolder16, mandatory=u'no', name=u'security_zone', key=u'security_zone', locked=u'no', cardinality=u'unspecified', targetName=u'app-zone')
vnsAbsFolder17 = cobra.model.vns.AbsFolder(vnsAbsDevCfg, locked=u'no', name=u'db-zone', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'SecurityZone', cardinality=u'unspecified')
vnsAbsParam10 = cobra.model.vns.AbsParam(vnsAbsFolder17, validation=u'', mandatory=u'no', name=u'type', value=u'ROUTED', key=u'type', locked=u'no', cardinality=u'unspecified')
vnsAbsFuncCfg = cobra.model.vns.AbsFuncCfg(vnsAbsFuncProf, ownerKey=u'', name=u'funcConfig', descr=u'', ownerTag=u'')
vnsAbsFolder18 = cobra.model.vns.AbsFolder(vnsAbsFuncCfg, locked=u'no', name=u'IntConfig', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'InIntfConfigRelFolder', cardinality=u'unspecified')
vnsAbsCfgRel7 = cobra.model.vns.AbsCfgRel(vnsAbsFolder18, mandatory=u'no', name=u'InConfigrel', key=u'InIntfConfigRel', locked=u'no', cardinality=u'unspecified', targetName=u'internalInterface')
vnsAbsFolder19 = cobra.model.vns.AbsFolder(vnsAbsFuncCfg, locked=u'no', name=u'AccessPolicyFolder', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessPolicyFolder', cardinality=u'unspecified')
vnsAbsCfgRel8 = cobra.model.vns.AbsCfgRel(vnsAbsFolder19, mandatory=u'no', name=u'InAccessPolicyRel', key=u'InAccessPolicyRel', locked=u'no', cardinality=u'unspecified', targetName=u'ftd-policy')
vnsAbsFolder20 = cobra.model.vns.AbsFolder(vnsAbsFuncCfg, locked=u'no', name=u'ExtConfig', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'no', key=u'ExIntfConfigRelFolder', cardinality=u'unspecified')
vnsAbsCfgRel9 = cobra.model.vns.AbsCfgRel(vnsAbsFolder20, mandatory=u'no', name=u'ExtConfigrel', key=u'ExIntfConfigRel', locked=u'no', cardinality=u'unspecified', targetName=u'externalInterface')


# commit the generated code to APIC
print toXMLStr(vnsAbsFuncProfContr)
c = cobra.mit.request.ConfigRequest()
c.addMo(vnsAbsFuncProfContr)
md.commit(c)

