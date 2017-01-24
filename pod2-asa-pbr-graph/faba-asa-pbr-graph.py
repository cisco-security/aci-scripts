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
import sys
from cobra.internal.codec.xmlcodec import toXMLStr

pod_num_start = int(sys.argv[1])
pod_num_end = int(sys.argv[2])

# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://10.10.35.10', 'pod%s' % pod_num_end, 'cisco')
md = cobra.mit.access.MoDirectory(ls)
md.login()

for pod_num in range(pod_num_start, (1 + pod_num_end)):
    # the top level object on which operations will be made
    polUni = cobra.model.pol.Uni('')
    fvTenant = cobra.model.fv.Tenant(polUni, 'pod%d' % pod_num)

    # build the request using cobra syntax
    vnsAbsGraph = cobra.model.vns.AbsGraph(fvTenant, ownerKey=u'', name=u'asa-pbr-graph', descr=u'', ownerTag=u'', uiTemplateType=u'UNSPECIFIED')
    vnsAbsTermNodeCon = cobra.model.vns.AbsTermNodeCon(vnsAbsGraph, ownerKey=u'', name=u'T1', descr=u'', ownerTag=u'')
    vnsAbsTermConn = cobra.model.vns.AbsTermConn(vnsAbsTermNodeCon, ownerKey=u'', attNotify=u'no', name=u'1', descr=u'', ownerTag=u'')
    vnsInTerm = cobra.model.vns.InTerm(vnsAbsTermNodeCon, name=u'', descr=u'')
    vnsOutTerm = cobra.model.vns.OutTerm(vnsAbsTermNodeCon, name=u'', descr=u'')
    vnsAbsTermNodeProv = cobra.model.vns.AbsTermNodeProv(vnsAbsGraph, ownerKey=u'', name=u'T2', descr=u'', ownerTag=u'')
    vnsAbsTermConn2 = cobra.model.vns.AbsTermConn(vnsAbsTermNodeProv, ownerKey=u'', attNotify=u'no', name=u'1', descr=u'', ownerTag=u'')
    vnsInTerm2 = cobra.model.vns.InTerm(vnsAbsTermNodeProv, name=u'', descr=u'')
    vnsOutTerm2 = cobra.model.vns.OutTerm(vnsAbsTermNodeProv, name=u'', descr=u'')
    vnsAbsConnection = cobra.model.vns.AbsConnection(vnsAbsGraph, adjType=u'L3', ownerKey=u'', name=u'C1', descr=u'', connDir=u'provider', connType=u'external', unicastRoute=u'yes', ownerTag=u'', directConnect=u'no')
    vnsRsAbsConnectionConns = cobra.model.vns.RsAbsConnectionConns(vnsAbsConnection, tDn=u'uni/tn-pod%d/AbsGraph-asa-pbr-graph/AbsNode-asa-pbr/AbsFConn-consumer' % pod_num)
    vnsRsAbsConnectionConns2 = cobra.model.vns.RsAbsConnectionConns(vnsAbsConnection, tDn=u'uni/tn-pod%d/AbsGraph-asa-pbr-graph/AbsTermNodeCon-T1/AbsTConn' % pod_num)
    vnsAbsConnection2 = cobra.model.vns.AbsConnection(vnsAbsGraph, adjType=u'L3', ownerKey=u'', name=u'C2', descr=u'', connDir=u'provider', connType=u'external', unicastRoute=u'yes', ownerTag=u'', directConnect=u'no')
    vnsRsAbsConnectionConns3 = cobra.model.vns.RsAbsConnectionConns(vnsAbsConnection2, tDn=u'uni/tn-pod%d/AbsGraph-asa-pbr-graph/AbsTermNodeProv-T2/AbsTConn' % pod_num)
    vnsRsAbsConnectionConns4 = cobra.model.vns.RsAbsConnectionConns(vnsAbsConnection2, tDn=u'uni/tn-pod%d/AbsGraph-asa-pbr-graph/AbsNode-asa-pbr/AbsFConn-provider' % pod_num)
    vnsAbsNode = cobra.model.vns.AbsNode(vnsAbsGraph, funcTemplateType=u'FW_ROUTED', isCopy=u'no', ownerKey=u'', managed=u'yes', name=u'asa-pbr', descr=u'', funcType=u'GoTo', shareEncap=u'no', sequenceNumber=u'0', routingMode=u'Redirect', ownerTag=u'')
    vnsAbsFuncConn = cobra.model.vns.AbsFuncConn(vnsAbsNode, ownerKey=u'', attNotify=u'no', name=u'consumer', descr=u'', ownerTag=u'')
    vnsRsMConnAtt = cobra.model.vns.RsMConnAtt(vnsAbsFuncConn, tDn=u'uni/infra/mDev-CISCO-ASA-1.2/mFunc-Firewall/mConn-external')
    vnsAbsFuncConn2 = cobra.model.vns.AbsFuncConn(vnsAbsNode, ownerKey=u'', attNotify=u'no', name=u'provider', descr=u'', ownerTag=u'')
    vnsRsMConnAtt2 = cobra.model.vns.RsMConnAtt(vnsAbsFuncConn2, tDn=u'uni/infra/mDev-CISCO-ASA-1.2/mFunc-Firewall/mConn-internal')
    vnsRsNodeToAbsFuncProf = cobra.model.vns.RsNodeToAbsFuncProf(vnsAbsNode, tDn=u'uni/tn-pod%d/absFuncProfContr/absFuncProfGrp-pbr-cfg/absFuncProf-pbr-cfg-asa' % pod_num)
    vnsRsNodeToMFunc = cobra.model.vns.RsNodeToMFunc(vnsAbsNode, tDn=u'uni/infra/mDev-CISCO-ASA-1.2/mFunc-Firewall')
    vnsRsNodeToLDev = cobra.model.vns.RsNodeToLDev(vnsAbsNode, tDn=u'uni/tn-pod%d/lDevVip-pod%d-asa-pbr-fover' % (pod_num, pod_num))


    # commit the generated code to APIC
    print toXMLStr(fvTenant)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(fvTenant)
    md.commit(c)

