#!/usr/bin/env python
################################################################################
#                                                                              #
# Copyright (c) 2017 Cisco Systems                                             #
# All Rights Reserved.                                                         #
#                                                                              #
#    Licensed under the Apache License, Version 2.0 (the "License"); you may   #
#    not use this file except in compliance with the License. You may obtain   #
#    a copy of the License at                                                  #
#                                                                              #
#         http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                              #
#    Unless required by applicable law or agreed to in writing, software       #
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT #
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the  #
#    License for the specific language governing permissions and limitations   #
#    under the License.                                                        #
#                                                                              #
################################################################################
# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.fv
import cobra.model.pol
import cobra.model.vns
from cobra.internal.codec.xmlcodec import toXMLStr
import sys
pod_num_start = int(sys.argv[1])
pod_num_end = int(sys.argv[2])

# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://10.10.35.10', 'pod%s' % pod_num_end, 'cisco')

md = cobra.mit.access.MoDirectory(ls)
md.login()

# the top level object on which operations will be made
for pod_num in range(pod_num_start, (1 + pod_num_end)):
    polUni = cobra.model.pol.Uni('')
    fvTenant = cobra.model.fv.Tenant(polUni, 'pod%s' % pod_num)
    vnsAbsFuncProfContr = cobra.model.vns.AbsFuncProfContr(fvTenant)
    vnsAbsFuncProfGrp = cobra.model.vns.AbsFuncProfGrp(vnsAbsFuncProfContr, 'asa-clu-gr')

    # build the request using cobra syntax
    vnsAbsFuncProfGrp = cobra.model.vns.AbsFuncProfGrp(vnsAbsFuncProfContr, ownerKey=u'', name=u'asa-clu-gr', descr=u'', ownerTag=u'')
    vnsAbsFuncProf = cobra.model.vns.AbsFuncProf(vnsAbsFuncProfGrp, ownerKey=u'', name=u'asa-clu-fprof', descr=u'', ownerTag=u'')
    vnsRsProfToMFunc = cobra.model.vns.RsProfToMFunc(vnsAbsFuncProf, tDn=u'uni/infra/mDev-CISCO-ASA-1.2/mFunc-Firewall')
    vnsAbsDevCfg = cobra.model.vns.AbsDevCfg(vnsAbsFuncProf, ownerKey=u'', name=u'devConfig', descr=u'', ownerTag=u'')
    vnsAbsFolder = cobra.model.vns.AbsFolder(vnsAbsDevCfg, locked=u'no', name=u'internalIf', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'Interface', cardinality=u'unspecified')
    vnsAbsFolder2 = cobra.model.vns.AbsFolder(vnsAbsFolder, locked=u'no', name=u'internalIfCfg', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'InterfaceConfig', cardinality=u'unspecified')
    vnsAbsParam = cobra.model.vns.AbsParam(vnsAbsFolder2, validation=u'', mandatory=u'no', name=u'internal_security_level', value=u'100', key=u'security_level', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder3 = cobra.model.vns.AbsFolder(vnsAbsFolder2, locked=u'no', name=u'IPv4Address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'IPv4Address', cardinality=u'unspecified')
    vnsAbsParam2 = cobra.model.vns.AbsParam(vnsAbsFolder3, validation=u'', mandatory=u'yes', name=u'ipv4_address', value=u'10.40.0.10/255.255.255.0', key=u'ipv4_address', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder4 = cobra.model.vns.AbsFolder(vnsAbsDevCfg, locked=u'no', name=u'access-list-inbound', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessList', cardinality=u'unspecified')
    vnsAbsFolder5 = cobra.model.vns.AbsFolder(vnsAbsFolder4, locked=u'no', name=u'permit-https', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessControlEntry', cardinality=u'unspecified')
    vnsAbsParam3 = cobra.model.vns.AbsParam(vnsAbsFolder5, validation=u'', mandatory=u'yes', name=u'order1', value=u'10', key=u'order', locked=u'no', cardinality=u'unspecified')
    vnsAbsParam4 = cobra.model.vns.AbsParam(vnsAbsFolder5, validation=u'', mandatory=u'yes', name=u'action-permit', value=u'permit', key=u'action', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder6 = cobra.model.vns.AbsFolder(vnsAbsFolder5, locked=u'no', name=u'tcp', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'protocol', cardinality=u'unspecified')
    vnsAbsParam5 = cobra.model.vns.AbsParam(vnsAbsFolder6, validation=u'', mandatory=u'no', name=u'tcp', value=u'tcp', key=u'name_number', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder7 = cobra.model.vns.AbsFolder(vnsAbsFolder5, locked=u'no', name=u'dest-service', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'destination_service', cardinality=u'unspecified')
    vnsAbsParam6 = cobra.model.vns.AbsParam(vnsAbsFolder7, validation=u'', mandatory=u'yes', name=u'op', value=u'eq', key=u'operator', locked=u'no', cardinality=u'unspecified')
    vnsAbsParam7 = cobra.model.vns.AbsParam(vnsAbsFolder7, validation=u'', mandatory=u'yes', name=u'port', value=u'https', key=u'low_port', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder8 = cobra.model.vns.AbsFolder(vnsAbsFolder5, locked=u'no', name=u'src-address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'source_address', cardinality=u'unspecified')
    vnsAbsParam8 = cobra.model.vns.AbsParam(vnsAbsFolder8, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder9 = cobra.model.vns.AbsFolder(vnsAbsFolder5, locked=u'no', name=u'dest-address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'destination_address', cardinality=u'unspecified')
    vnsAbsParam9 = cobra.model.vns.AbsParam(vnsAbsFolder9, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder10 = cobra.model.vns.AbsFolder(vnsAbsFolder4, locked=u'no', name=u'permit-udp', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessControlEntry', cardinality=u'unspecified')
    vnsAbsParam10 = cobra.model.vns.AbsParam(vnsAbsFolder10, validation=u'', mandatory=u'yes', name=u'order', value=u'40', key=u'order', locked=u'no', cardinality=u'unspecified')
    vnsAbsParam11 = cobra.model.vns.AbsParam(vnsAbsFolder10, validation=u'', mandatory=u'yes', name=u'action', value=u'permit', key=u'action', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder11 = cobra.model.vns.AbsFolder(vnsAbsFolder10, locked=u'no', name=u'udp', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'protocol', cardinality=u'unspecified')
    vnsAbsParam12 = cobra.model.vns.AbsParam(vnsAbsFolder11, validation=u'', mandatory=u'no', name=u'name_number', value=u'udp', key=u'name_number', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder12 = cobra.model.vns.AbsFolder(vnsAbsFolder10, locked=u'no', name=u'destination_address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'destination_address', cardinality=u'unspecified')
    vnsAbsParam13 = cobra.model.vns.AbsParam(vnsAbsFolder12, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder13 = cobra.model.vns.AbsFolder(vnsAbsFolder10, locked=u'no', name=u'source_address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'source_address', cardinality=u'unspecified')
    vnsAbsParam14 = cobra.model.vns.AbsParam(vnsAbsFolder13, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder14 = cobra.model.vns.AbsFolder(vnsAbsFolder4, locked=u'no', name=u'permit-icmp', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessControlEntry', cardinality=u'unspecified')
    vnsAbsParam15 = cobra.model.vns.AbsParam(vnsAbsFolder14, validation=u'', mandatory=u'yes', name=u'order', value=u'30', key=u'order', locked=u'no', cardinality=u'unspecified')
    vnsAbsParam16 = cobra.model.vns.AbsParam(vnsAbsFolder14, validation=u'', mandatory=u'yes', name=u'action', value=u'permit', key=u'action', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder15 = cobra.model.vns.AbsFolder(vnsAbsFolder14, locked=u'no', name=u'destination_address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'destination_address', cardinality=u'unspecified')
    vnsAbsParam17 = cobra.model.vns.AbsParam(vnsAbsFolder15, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder16 = cobra.model.vns.AbsFolder(vnsAbsFolder14, locked=u'no', name=u'icmp', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'protocol', cardinality=u'unspecified')
    vnsAbsParam18 = cobra.model.vns.AbsParam(vnsAbsFolder16, validation=u'', mandatory=u'no', name=u'name_number', value=u'icmp', key=u'name_number', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder17 = cobra.model.vns.AbsFolder(vnsAbsFolder14, locked=u'no', name=u'source_address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'source_address', cardinality=u'unspecified')
    vnsAbsParam19 = cobra.model.vns.AbsParam(vnsAbsFolder17, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder18 = cobra.model.vns.AbsFolder(vnsAbsFolder4, locked=u'no', name=u'permit-http', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessControlEntry', cardinality=u'unspecified')
    vnsAbsParam20 = cobra.model.vns.AbsParam(vnsAbsFolder18, validation=u'', mandatory=u'yes', name=u'order1', value=u'10', key=u'order', locked=u'no', cardinality=u'unspecified')
    vnsAbsParam21 = cobra.model.vns.AbsParam(vnsAbsFolder18, validation=u'', mandatory=u'yes', name=u'action-permit', value=u'permit', key=u'action', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder19 = cobra.model.vns.AbsFolder(vnsAbsFolder18, locked=u'no', name=u'tcp', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'protocol', cardinality=u'unspecified')
    vnsAbsParam22 = cobra.model.vns.AbsParam(vnsAbsFolder19, validation=u'', mandatory=u'no', name=u'tcp', value=u'tcp', key=u'name_number', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder20 = cobra.model.vns.AbsFolder(vnsAbsFolder18, locked=u'no', name=u'dest-service', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'destination_service', cardinality=u'unspecified')
    vnsAbsParam23 = cobra.model.vns.AbsParam(vnsAbsFolder20, validation=u'', mandatory=u'yes', name=u'op', value=u'eq', key=u'operator', locked=u'no', cardinality=u'unspecified')
    vnsAbsParam24 = cobra.model.vns.AbsParam(vnsAbsFolder20, validation=u'', mandatory=u'yes', name=u'port', value=u'http', key=u'low_port', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder21 = cobra.model.vns.AbsFolder(vnsAbsFolder18, locked=u'no', name=u'src-address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'source_address', cardinality=u'unspecified')
    vnsAbsParam25 = cobra.model.vns.AbsParam(vnsAbsFolder21, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder22 = cobra.model.vns.AbsFolder(vnsAbsFolder18, locked=u'no', name=u'dest-address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'destination_address', cardinality=u'unspecified')
    vnsAbsParam26 = cobra.model.vns.AbsParam(vnsAbsFolder22, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder23 = cobra.model.vns.AbsFolder(vnsAbsDevCfg, locked=u'no', name=u'externalIf', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'Interface', cardinality=u'unspecified')
    vnsAbsFolder24 = cobra.model.vns.AbsFolder(vnsAbsFolder23, locked=u'no', name=u'externalIfCfg', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'InterfaceConfig', cardinality=u'unspecified')
    vnsAbsParam27 = cobra.model.vns.AbsParam(vnsAbsFolder24, validation=u'', mandatory=u'no', name=u'external_security_level', value=u'50', key=u'security_level', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder25 = cobra.model.vns.AbsFolder(vnsAbsFolder24, locked=u'no', name=u'IPv4Address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'IPv4Address', cardinality=u'unspecified')
    vnsAbsParam28 = cobra.model.vns.AbsParam(vnsAbsFolder25, validation=u'', mandatory=u'yes', name=u'ipv4_address', value=u'10.50.0.10/255.255.255.0', key=u'ipv4_address', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder26 = cobra.model.vns.AbsFolder(vnsAbsFolder23, locked=u'no', name=u'ExtAccessGroup', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessGroup', cardinality=u'unspecified')
    vnsAbsCfgRel = cobra.model.vns.AbsCfgRel(vnsAbsFolder26, mandatory=u'no', name=u'name', key=u'inbound_access_list_name', locked=u'no', cardinality=u'unspecified', targetName=u'access-list-inbound')
    vnsAbsFuncCfg = cobra.model.vns.AbsFuncCfg(vnsAbsFuncProf, ownerKey=u'', name=u'funcConfig', descr=u'', ownerTag=u'')
    vnsAbsFolder27 = cobra.model.vns.AbsFolder(vnsAbsFuncCfg, locked=u'no', name=u'IntConfig', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'InIntfConfigRelFolder', cardinality=u'unspecified')
    vnsAbsCfgRel2 = cobra.model.vns.AbsCfgRel(vnsAbsFolder27, mandatory=u'no', name=u'InConfigrel', key=u'InIntfConfigRel', locked=u'no', cardinality=u'unspecified', targetName=u'internalIf')
    vnsAbsFolder28 = cobra.model.vns.AbsFolder(vnsAbsFuncCfg, locked=u'no', name=u'ExtConfig', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'ExIntfConfigRelFolder', cardinality=u'unspecified')
    vnsAbsCfgRel3 = cobra.model.vns.AbsCfgRel(vnsAbsFolder28, mandatory=u'no', name=u'ExtConfigrel', key=u'ExIntfConfigRel', locked=u'no', cardinality=u'unspecified', targetName=u'externalIf')

'''
    vnsAbsFuncProf = cobra.model.vns.AbsFuncProf(vnsAbsFuncProfGrp, ownerKey=u'', name=u'asa-clu-fprof', descr=u'', ownerTag=u'')
    vnsRsProfToMFunc = cobra.model.vns.RsProfToMFunc(vnsAbsFuncProf, tDn=u'uni/infra/mDev-CISCO-ASA-1.2/mFunc-Firewall')
    vnsAbsDevCfg = cobra.model.vns.AbsDevCfg(vnsAbsFuncProf, ownerKey=u'', name=u'devConfig', descr=u'', ownerTag=u'')
    vnsAbsFolder = cobra.model.vns.AbsFolder(vnsAbsDevCfg, locked=u'no', name=u'internalIf', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'Interface', cardinality=u'unspecified')
    vnsAbsFolder2 = cobra.model.vns.AbsFolder(vnsAbsFolder, locked=u'no', name=u'internalIfCfg', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'InterfaceConfig', cardinality=u'unspecified')
    vnsAbsParam = cobra.model.vns.AbsParam(vnsAbsFolder2, validation=u'', mandatory=u'no', name=u'internal_security_level', value=u'100', key=u'security_level', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder3 = cobra.model.vns.AbsFolder(vnsAbsFolder2, locked=u'no', name=u'IPv4Address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'IPv4Address', cardinality=u'unspecified')
    vnsAbsParam2 = cobra.model.vns.AbsParam(vnsAbsFolder3, validation=u'', mandatory=u'yes', name=u'ipv4_address', value=u'10.50.0.10/255.255.255.0', key=u'ipv4_address', locked=u'no', cardinality=u'unspecified')
#    vnsAbsFolder4 = cobra.model.vns.AbsFolder(vnsAbsFolder, locked=u'no', name=u'ServicePolicy', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'ServicePolicy', cardinality=u'unspecified')
    vnsAbsFolder5 = cobra.model.vns.AbsFolder(vnsAbsDevCfg, locked=u'no', name=u'access-list-inbound', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessList', cardinality=u'unspecified')
    vnsAbsFolder6 = cobra.model.vns.AbsFolder(vnsAbsFolder5, locked=u'no', name=u'permit-https', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessControlEntry', cardinality=u'unspecified')
    vnsAbsParam3 = cobra.model.vns.AbsParam(vnsAbsFolder6, validation=u'', mandatory=u'yes', name=u'order1', value=u'10', key=u'order', locked=u'no', cardinality=u'unspecified')
    vnsAbsParam4 = cobra.model.vns.AbsParam(vnsAbsFolder6, validation=u'', mandatory=u'yes', name=u'action-permit', value=u'permit', key=u'action', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder7 = cobra.model.vns.AbsFolder(vnsAbsFolder6, locked=u'no', name=u'tcp', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'protocol', cardinality=u'unspecified')
    vnsAbsParam5 = cobra.model.vns.AbsParam(vnsAbsFolder7, validation=u'', mandatory=u'no', name=u'tcp', value=u'tcp', key=u'name_number', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder8 = cobra.model.vns.AbsFolder(vnsAbsFolder6, locked=u'no', name=u'dest-service', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'destination_service', cardinality=u'unspecified')
    vnsAbsParam6 = cobra.model.vns.AbsParam(vnsAbsFolder8, validation=u'', mandatory=u'yes', name=u'op', value=u'eq', key=u'operator', locked=u'no', cardinality=u'unspecified')
    vnsAbsParam7 = cobra.model.vns.AbsParam(vnsAbsFolder8, validation=u'', mandatory=u'yes', name=u'port', value=u'https', key=u'low_port', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder9 = cobra.model.vns.AbsFolder(vnsAbsFolder6, locked=u'no', name=u'src-address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'source_address', cardinality=u'unspecified')
    vnsAbsParam8 = cobra.model.vns.AbsParam(vnsAbsFolder9, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder10 = cobra.model.vns.AbsFolder(vnsAbsFolder6, locked=u'no', name=u'dest-address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'destination_address', cardinality=u'unspecified')
    vnsAbsParam9 = cobra.model.vns.AbsParam(vnsAbsFolder10, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder11 = cobra.model.vns.AbsFolder(vnsAbsFolder5, locked=u'no', name=u'permit-http', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessControlEntry', cardinality=u'unspecified')
    vnsAbsParam10 = cobra.model.vns.AbsParam(vnsAbsFolder11, validation=u'', mandatory=u'yes', name=u'order1', value=u'10', key=u'order', locked=u'no', cardinality=u'unspecified')
    vnsAbsParam11 = cobra.model.vns.AbsParam(vnsAbsFolder11, validation=u'', mandatory=u'yes', name=u'action-permit', value=u'permit', key=u'action', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder12 = cobra.model.vns.AbsFolder(vnsAbsFolder11, locked=u'no', name=u'tcp', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'protocol', cardinality=u'unspecified')
    vnsAbsParam12 = cobra.model.vns.AbsParam(vnsAbsFolder12, validation=u'', mandatory=u'no', name=u'tcp', value=u'tcp', key=u'name_number', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder13 = cobra.model.vns.AbsFolder(vnsAbsFolder11, locked=u'no', name=u'dest-service', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'destination_service', cardinality=u'unspecified')
    vnsAbsParam13 = cobra.model.vns.AbsParam(vnsAbsFolder13, validation=u'', mandatory=u'yes', name=u'op', value=u'eq', key=u'operator', locked=u'no', cardinality=u'unspecified')
    vnsAbsParam14 = cobra.model.vns.AbsParam(vnsAbsFolder13, validation=u'', mandatory=u'yes', name=u'port', value=u'http', key=u'low_port', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder14 = cobra.model.vns.AbsFolder(vnsAbsFolder11, locked=u'no', name=u'src-address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'source_address', cardinality=u'unspecified')
    vnsAbsParam15 = cobra.model.vns.AbsParam(vnsAbsFolder14, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder15 = cobra.model.vns.AbsFolder(vnsAbsFolder11, locked=u'no', name=u'dest-address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'destination_address', cardinality=u'unspecified')
    vnsAbsParam16 = cobra.model.vns.AbsParam(vnsAbsFolder15, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')

    vnsAbsParam2 = cobra.model.vns.AbsParam(vnsAbsFolder3, validation=u'', mandatory=u'yes', name=u'ipv4_address', value=u'10.2.0.1/255.255.255.0', key=u'ipv4_address', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder4 = cobra.model.vns.AbsFolder(vnsAbsDevCfg, locked=u'no', name=u'access-list-inbound', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessList', cardinality=u'unspecified')
    vnsAbsFolder5 = cobra.model.vns.AbsFolder(vnsAbsFolder4, locked=u'no', name=u'permit-https', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessControlEntry', cardinality=u'unspecified')
    vnsAbsParam3 = cobra.model.vns.AbsParam(vnsAbsFolder5, validation=u'', mandatory=u'yes', name=u'order1', value=u'10', key=u'order', locked=u'no', cardinality=u'unspecified')
    vnsAbsParam4 = cobra.model.vns.AbsParam(vnsAbsFolder5, validation=u'', mandatory=u'yes', name=u'action-permit', value=u'permit', key=u'action', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder6 = cobra.model.vns.AbsFolder(vnsAbsFolder5, locked=u'no', name=u'tcp', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'protocol', cardinality=u'unspecified')
    vnsAbsParam5 = cobra.model.vns.AbsParam(vnsAbsFolder6, validation=u'', mandatory=u'no', name=u'tcp', value=u'tcp', key=u'name_number', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder7 = cobra.model.vns.AbsFolder(vnsAbsFolder5, locked=u'no', name=u'dest-service', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'destination_service', cardinality=u'unspecified')
    vnsAbsParam6 = cobra.model.vns.AbsParam(vnsAbsFolder7, validation=u'', mandatory=u'yes', name=u'op', value=u'eq', key=u'operator', locked=u'no', cardinality=u'unspecified')
    vnsAbsParam7 = cobra.model.vns.AbsParam(vnsAbsFolder7, validation=u'', mandatory=u'yes', name=u'port', value=u'https', key=u'low_port', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder8 = cobra.model.vns.AbsFolder(vnsAbsFolder5, locked=u'no', name=u'src-address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'source_address', cardinality=u'unspecified')
    vnsAbsParam8 = cobra.model.vns.AbsParam(vnsAbsFolder8, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder9 = cobra.model.vns.AbsFolder(vnsAbsFolder5, locked=u'no', name=u'dest-address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'destination_address', cardinality=u'unspecified')
    vnsAbsParam9 = cobra.model.vns.AbsParam(vnsAbsFolder9, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder10 = cobra.model.vns.AbsFolder(vnsAbsFolder4, locked=u'no', name=u'permit-udp', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessControlEntry', cardinality=u'unspecified')
    vnsAbsParam10 = cobra.model.vns.AbsParam(vnsAbsFolder10, validation=u'', mandatory=u'yes', name=u'order', value=u'40', key=u'order', locked=u'no', cardinality=u'unspecified')
    vnsAbsParam11 = cobra.model.vns.AbsParam(vnsAbsFolder10, validation=u'', mandatory=u'yes', name=u'action', value=u'permit', key=u'action', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder11 = cobra.model.vns.AbsFolder(vnsAbsFolder10, locked=u'no', name=u'udp', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'protocol', cardinality=u'unspecified')
    vnsAbsParam12 = cobra.model.vns.AbsParam(vnsAbsFolder11, validation=u'', mandatory=u'no', name=u'name_number', value=u'udp', key=u'name_number', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder12 = cobra.model.vns.AbsFolder(vnsAbsFolder10, locked=u'no', name=u'destination_address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'destination_address', cardinality=u'unspecified')
    vnsAbsParam13 = cobra.model.vns.AbsParam(vnsAbsFolder12, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder13 = cobra.model.vns.AbsFolder(vnsAbsFolder10, locked=u'no', name=u'source_address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'source_address', cardinality=u'unspecified')
    vnsAbsParam14 = cobra.model.vns.AbsParam(vnsAbsFolder13, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder14 = cobra.model.vns.AbsFolder(vnsAbsFolder4, locked=u'no', name=u'permit-icmp', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessControlEntry', cardinality=u'unspecified')
    vnsAbsParam15 = cobra.model.vns.AbsParam(vnsAbsFolder14, validation=u'', mandatory=u'yes', name=u'order', value=u'30', key=u'order', locked=u'no', cardinality=u'unspecified')
    vnsAbsParam16 = cobra.model.vns.AbsParam(vnsAbsFolder14, validation=u'', mandatory=u'yes', name=u'action', value=u'permit', key=u'action', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder15 = cobra.model.vns.AbsFolder(vnsAbsFolder14, locked=u'no', name=u'destination_address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'destination_address', cardinality=u'unspecified')
    vnsAbsParam17 = cobra.model.vns.AbsParam(vnsAbsFolder15, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder16 = cobra.model.vns.AbsFolder(vnsAbsFolder14, locked=u'no', name=u'icmp', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'protocol', cardinality=u'unspecified')
    vnsAbsParam18 = cobra.model.vns.AbsParam(vnsAbsFolder16, validation=u'', mandatory=u'no', name=u'name_number', value=u'icmp', key=u'name_number', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder17 = cobra.model.vns.AbsFolder(vnsAbsFolder14, locked=u'no', name=u'source_address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'source_address', cardinality=u'unspecified')
    vnsAbsParam19 = cobra.model.vns.AbsParam(vnsAbsFolder17, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder18 = cobra.model.vns.AbsFolder(vnsAbsFolder4, locked=u'no', name=u'permit-http', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessControlEntry', cardinality=u'unspecified')
    vnsAbsParam20 = cobra.model.vns.AbsParam(vnsAbsFolder18, validation=u'', mandatory=u'yes', name=u'order1', value=u'10', key=u'order', locked=u'no', cardinality=u'unspecified')
    vnsAbsParam21 = cobra.model.vns.AbsParam(vnsAbsFolder18, validation=u'', mandatory=u'yes', name=u'action-permit', value=u'permit', key=u'action', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder19 = cobra.model.vns.AbsFolder(vnsAbsFolder18, locked=u'no', name=u'tcp', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'protocol', cardinality=u'unspecified')
    vnsAbsParam22 = cobra.model.vns.AbsParam(vnsAbsFolder19, validation=u'', mandatory=u'no', name=u'tcp', value=u'tcp', key=u'name_number', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder20 = cobra.model.vns.AbsFolder(vnsAbsFolder18, locked=u'no', name=u'dest-service', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'destination_service', cardinality=u'unspecified')
    vnsAbsParam23 = cobra.model.vns.AbsParam(vnsAbsFolder20, validation=u'', mandatory=u'yes', name=u'op', value=u'eq', key=u'operator', locked=u'no', cardinality=u'unspecified')
    vnsAbsParam24 = cobra.model.vns.AbsParam(vnsAbsFolder20, validation=u'', mandatory=u'yes', name=u'port', value=u'http', key=u'low_port', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder21 = cobra.model.vns.AbsFolder(vnsAbsFolder18, locked=u'no', name=u'src-address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'source_address', cardinality=u'unspecified')
    vnsAbsParam25 = cobra.model.vns.AbsParam(vnsAbsFolder21, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder22 = cobra.model.vns.AbsFolder(vnsAbsFolder18, locked=u'no', name=u'dest-address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'destination_address', cardinality=u'unspecified')
    vnsAbsParam26 = cobra.model.vns.AbsParam(vnsAbsFolder22, validation=u'', mandatory=u'no', name=u'any', value=u'any', key=u'any', locked=u'no', cardinality=u'unspecified')

    vnsAbsFolder23 = cobra.model.vns.AbsFolder(vnsAbsDevCfg, locked=u'no', name=u'externalIf', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'Interface', cardinality=u'unspecified')
    vnsAbsFolder24 = cobra.model.vns.AbsFolder(vnsAbsFolder23, locked=u'no', name=u'externalIfCfg', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'InterfaceConfig', cardinality=u'unspecified')
    vnsAbsParam24 = cobra.model.vns.AbsParam(vnsAbsFolder24, validation=u'', mandatory=u'no', name=u'external_security_level', value=u'50', key=u'security_level', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder24 = cobra.model.vns.AbsFolder(vnsAbsFolder24, locked=u'no', name=u'IPv4Address', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'IPv4Address', cardinality=u'unspecified')
    vnsAbsParam25 = cobra.model.vns.AbsParam(vnsAbsFolder24, validation=u'', mandatory=u'yes', name=u'ipv4_address', value=u'10.40.0.10/255.255.255.0', key=u'ipv4_address', locked=u'no', cardinality=u'unspecified')
    vnsAbsFolder19 = cobra.model.vns.AbsFolder(vnsAbsFolder16, locked=u'no', name=u'ExtAccessGroup', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'AccessGroup', cardinality=u'unspecified')
    vnsAbsCfgRel = cobra.model.vns.AbsCfgRel(vnsAbsFolder19, mandatory=u'no', name=u'name', key=u'inbound_access_list_name', locked=u'no', cardinality=u'unspecified', targetName=u'access-list-inbound')
    vnsAbsFuncCfg = cobra.model.vns.AbsFuncCfg(vnsAbsFuncProf, ownerKey=u'', name=u'funcConfig', descr=u'', ownerTag=u'')
    vnsAbsFolder20 = cobra.model.vns.AbsFolder(vnsAbsFuncCfg, locked=u'no', name=u'IntConfig', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'InIntfConfigRelFolder', cardinality=u'unspecified')
    vnsAbsCfgRel2 = cobra.model.vns.AbsCfgRel(vnsAbsFolder20, mandatory=u'no', name=u'InConfigrel', key=u'InIntfConfigRel', locked=u'no', cardinality=u'unspecified', targetName=u'internalIf')
    vnsAbsFolder21 = cobra.model.vns.AbsFolder(vnsAbsFuncCfg, locked=u'no', name=u'ExtConfig', devCtxLbl=u'', scopedBy=u'epg', profileBehaviorShared=u'yes', key=u'ExIntfConfigRelFolder', cardinality=u'unspecified')
    vnsAbsCfgRel3 = cobra.model.vns.AbsCfgRel(vnsAbsFolder21, mandatory=u'no', name=u'ExtConfigrel', key=u'ExIntfConfigRel', locked=u'no', cardinality=u'unspecified', targetName=u'externalIf')
'''

# commit the generated code to APIC
print toXMLStr(vnsAbsFuncProfGrp)
c = cobra.mit.request.ConfigRequest()
c.addMo(vnsAbsFuncProfGrp)
md.commit(c)

