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
"""
Script creates L3outs for fabric border leaf and ASA context in out-to-web contract.        
"""

# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.fv
import cobra.model.l3ext
import cobra.model.ospf
import cobra.model.pol
from cobra.internal.codec.xmlcodec import toXMLStr
import sys
pod_num_start = int(sys.argv[1])
pod_num_end = int(sys.argv[2])

# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://10.10.35.10', 'pod%s' % pod_num_end, 'cisco')
md = cobra.mit.access.MoDirectory(ls)
md.login()

for pod_num in range(pod_num_start, (1 + pod_num_end)):
    out_vlan = pod_num + 3510
    l3out1_vlan = pod_num + 3000
    l3out2_vlan = pod_num + 3050

 # the top level object on which operations will be made
    polUni = cobra.model.pol.Uni('')
    fvTenant = cobra.model.fv.Tenant(polUni, 'pod%s' % pod_num)

    l3extRouteTagPol = cobra.model.l3ext.RouteTagPol(fvTenant, ownerKey=u'', name=u'asa-inside', descr=u'', tag=u'1040', ownerTag=u'')
    l3extRouteTagPol = cobra.model.l3ext.RouteTagPol(fvTenant, ownerKey=u'', name=u'asa-outside', descr=u'', tag=u'1050', ownerTag=u'')

    fvCtx = cobra.model.fv.Ctx(fvTenant, ownerKey=u'', name=u'pod%snet' % pod_num, descr=u'', knwMcastAct=u'permit', ownerTag=u'', pcEnfPref=u'enforced')
    fvRsCtxToExtRouteTagPol = cobra.model.fv.RsCtxToExtRouteTagPol(fvCtx, tnL3extRouteTagPolName=u'asa-inside')

    fvCtx2 = cobra.model.fv.Ctx(fvTenant, ownerKey=u'', name=u'vrf%snet' % pod_num, descr=u'', knwMcastAct=u'permit', ownerTag=u'', pcEnfPref=u'enforced')
    fvRsCtxToExtRouteTagPol = cobra.model.fv.RsCtxToExtRouteTagPol(fvCtx2, tnL3extRouteTagPolName=u'asa-outside')

    # build the request using cobra syntax
    l3extOut = cobra.model.l3ext.Out(fvTenant, ownerKey=u'', name=u'asa-clu-internal', descr=u'', targetDscp=u'unspecified', enforceRtctrl=u'export', ownerTag=u'')
    l3extRsEctx = cobra.model.l3ext.RsEctx(l3extOut, tnFvCtxName=u'pod%snet' % pod_num)
    l3extLNodeP = cobra.model.l3ext.LNodeP(l3extOut, ownerKey=u'', name=u'leafnp', descr=u'', targetDscp=u'unspecified', tag=u'yellow-green', ownerTag=u'')
    l3extRsNodeL3OutAtt = cobra.model.l3ext.RsNodeL3OutAtt(l3extLNodeP, rtrIdLoopBack=u'yes', rtrId=u'111.0.0.1', tDn=u'topology/pod-1/node-101')
    l3extRsNodeL3OutAtt2 = cobra.model.l3ext.RsNodeL3OutAtt(l3extLNodeP, rtrIdLoopBack=u'yes', rtrId=u'112.0.0.1', tDn=u'topology/pod-1/node-102')
    l3extLIfP = cobra.model.l3ext.LIfP(l3extLNodeP, ownerKey=u'', tag=u'yellow-green', name=u'leafip', descr=u'', ownerTag=u'')
    ospfIfP = cobra.model.ospf.IfP(l3extLIfP, authKeyId=u'1', authType=u'none', name=u'', descr=u'')
    ospfRsIfPol = cobra.model.ospf.RsIfPol(ospfIfP, tnOspfIfPolName=u'')
    l3extRsNdIfPol = cobra.model.l3ext.RsNdIfPol(l3extLIfP, tnNdIfPolName=u'')
    l3extRsIngressQosDppPol = cobra.model.l3ext.RsIngressQosDppPol(l3extLIfP, tnQosDppPolName=u'')
    l3extRsEgressQosDppPol = cobra.model.l3ext.RsEgressQosDppPol(l3extLIfP, tnQosDppPolName=u'')
    l3extRsPathL3OutAtt = cobra.model.l3ext.RsPathL3OutAtt(l3extLIfP, addr=u'0.0.0.0', descr=u'', encapScope=u'local', targetDscp=u'unspecified', llAddr=u'::', mac=u'00:22:BD:F8:19:FF', mode=u'regular', encap=u'vlan-%d' % l3out1_vlan, ifInstT=u'ext-svi', mtu=u'1500', tDn=u'topology/pod-1/protpaths-101-102/pathep-[vpc_aaep_asa1-asa2]')
    l3extMember = cobra.model.l3ext.Member(l3extRsPathL3OutAtt, name=u'', side=u'B', addr=u'10.40.0.2/24', descr=u'', llAddr=u'::')
    l3extMember2 = cobra.model.l3ext.Member(l3extRsPathL3OutAtt, name=u'', side=u'A', addr=u'10.40.0.1/24', descr=u'', llAddr=u'::')
    l3extRsL3DomAtt = cobra.model.l3ext.RsL3DomAtt(l3extOut, tDn=u'uni/l3dom-l3out_domain')
    l3extInstP = cobra.model.l3ext.InstP(l3extOut, prio=u'unspecified', matchT=u'AtleastOne', name=u'l3out1-epg', descr=u'', targetDscp=u'unspecified')
    l3extSubnet = cobra.model.l3ext.Subnet(l3extInstP, aggregate=u'', ip=u'10.40.0.0/24', name=u'', descr=u'')
    l3extSubnet2 = cobra.model.l3ext.Subnet(l3extInstP, aggregate=u'', ip=u'10.70.0.0/24', name=u'', descr=u'')
    l3extSubnet3 = cobra.model.l3ext.Subnet(l3extInstP, aggregate=u'', ip=u'10.1.0.0/24', name=u'', descr=u'', scope='export-rtctrl')
    fvRsCustQosPol = cobra.model.fv.RsCustQosPol(l3extInstP, tnQosCustomPolName=u'')
    ospfExtP = cobra.model.ospf.ExtP(l3extOut, areaCtrl=u'redistribute,summary', areaId=u'backbone', areaType=u'regular', areaCost=u'1', descr=u'')

    # build the request using cobra syntax
    l3extOut = cobra.model.l3ext.Out(fvTenant, ownerKey=u'', name=u'asa-clu-external', descr=u'', targetDscp=u'unspecified', enforceRtctrl=u'export', ownerTag=u'')
    l3extRsEctx = cobra.model.l3ext.RsEctx(l3extOut, tnFvCtxName=u'vrf%snet' % pod_num)
    l3extLNodeP = cobra.model.l3ext.LNodeP(l3extOut, ownerKey=u'', name=u'leaf1np', descr=u'', targetDscp=u'unspecified', tag=u'yellow-green', ownerTag=u'')
    l3extRsNodeL3OutAtt = cobra.model.l3ext.RsNodeL3OutAtt(l3extLNodeP, rtrIdLoopBack=u'yes', rtrId=u'101.0.0.1', tDn=u'topology/pod-1/node-101')
    l3extRsNodeL3OutAtt2 = cobra.model.l3ext.RsNodeL3OutAtt(l3extLNodeP, rtrIdLoopBack=u'yes', rtrId=u'102.0.0.1', tDn=u'topology/pod-1/node-102')
    l3extLIfP = cobra.model.l3ext.LIfP(l3extLNodeP, ownerKey=u'', tag=u'yellow-green', name=u'leaf1ip', descr=u'', ownerTag=u'')
    ospfIfP = cobra.model.ospf.IfP(l3extLIfP, authKeyId=u'1', authType=u'none', name=u'', descr=u'')
    ospfRsIfPol = cobra.model.ospf.RsIfPol(ospfIfP, tnOspfIfPolName=u'')
    l3extRsNdIfPol = cobra.model.l3ext.RsNdIfPol(l3extLIfP, tnNdIfPolName=u'')
    l3extRsIngressQosDppPol = cobra.model.l3ext.RsIngressQosDppPol(l3extLIfP, tnQosDppPolName=u'')
    l3extRsEgressQosDppPol = cobra.model.l3ext.RsEgressQosDppPol(l3extLIfP, tnQosDppPolName=u'')
    l3extRsPathL3OutAtt = cobra.model.l3ext.RsPathL3OutAtt(l3extLIfP, addr=u'0.0.0.0', descr=u'', encapScope=u'local', targetDscp=u'unspecified', llAddr=u'::', mac=u'00:22:BD:F8:19:FF', mode=u'regular', encap=u'vlan-%d' % l3out2_vlan, ifInstT=u'ext-svi', mtu=u'1500', tDn=u'topology/pod-1/protpaths-101-102/pathep-[vpc_aaep_asa1-asa2]')
    l3extMember = cobra.model.l3ext.Member(l3extRsPathL3OutAtt, name=u'', side=u'B', addr=u'10.50.0.2/24', descr=u'', llAddr=u'::')
    l3extMember2 = cobra.model.l3ext.Member(l3extRsPathL3OutAtt, name=u'', side=u'A', addr=u'10.50.0.1/24', descr=u'', llAddr=u'::')
    l3extRsL3DomAtt = cobra.model.l3ext.RsL3DomAtt(l3extOut, tDn=u'uni/l3dom-l3out_domain')
    l3extInstP = cobra.model.l3ext.InstP(l3extOut, prio=u'unspecified', matchT=u'AtleastOne', name=u'l3out2-epg', descr=u'', targetDscp=u'unspecified')
    l3extSubnet = cobra.model.l3ext.Subnet(l3extInstP, aggregate=u'', ip=u'10.70.0.0/24', name=u'', descr=u'', scope='export-rtctrl')
    l3extSubnet2 = cobra.model.l3ext.Subnet(l3extInstP, aggregate=u'', ip=u'10.1.0.0/24', name=u'', descr=u'')
    fvRsCustQosPol = cobra.model.fv.RsCustQosPol(l3extInstP, tnQosCustomPolName=u'')
    ospfExtP = cobra.model.ospf.ExtP(l3extOut, areaCtrl=u'redistribute,summary', areaId=u'backbone', areaType=u'regular', areaCost=u'1', descr=u'')


    # build the request using cobra syntax
    l3extOut = cobra.model.l3ext.Out(fvTenant, ownerKey=u'', name=u'wan-out', descr=u'', targetDscp=u'unspecified', enforceRtctrl=u'export', ownerTag=u'')
    l3extRsEctx = cobra.model.l3ext.RsEctx(l3extOut, tnFvCtxName=u'vrf%snet' % pod_num)
    l3extLNodeP = cobra.model.l3ext.LNodeP(l3extOut, ownerKey=u'', name=u'leafnp', descr=u'', targetDscp=u'unspecified', tag=u'yellow-green', ownerTag=u'')
    l3extRsNodeL3OutAtt = cobra.model.l3ext.RsNodeL3OutAtt(l3extLNodeP, rtrIdLoopBack=u'no', rtrId=u'101.0.0.1', tDn=u'topology/pod-1/node-101')
    l3extLIfP = cobra.model.l3ext.LIfP(l3extLNodeP, ownerKey=u'', tag=u'yellow-green', name=u'leafip', descr=u'', ownerTag=u'')
    ospfIfP = cobra.model.ospf.IfP(l3extLIfP, authKeyId=u'1', authType=u'none', name=u'', descr=u'')
    ospfRsIfPol = cobra.model.ospf.RsIfPol(ospfIfP, tnOspfIfPolName=u'')
    l3extRsNdIfPol = cobra.model.l3ext.RsNdIfPol(l3extLIfP, tnNdIfPolName=u'')
    l3extRsIngressQosDppPol = cobra.model.l3ext.RsIngressQosDppPol(l3extLIfP, tnQosDppPolName=u'')
    l3extRsEgressQosDppPol = cobra.model.l3ext.RsEgressQosDppPol(l3extLIfP, tnQosDppPolName=u'')
    l3extRsPathL3OutAtt = cobra.model.l3ext.RsPathL3OutAtt(l3extLIfP, addr=u'10.60.0.1/24', descr=u'', encapScope=u'local', targetDscp=u'unspecified', llAddr=u'::', mac=u'00:22:BD:F8:19:FF', mode=u'regular', encap=u'vlan-%d' % out_vlan, ifInstT=u'ext-svi', mtu=u'1500', tDn=u'topology/pod-1/paths-101/pathep-[eth1/16]')
    l3extRsL3DomAtt = cobra.model.l3ext.RsL3DomAtt(l3extOut, tDn=u'uni/l3dom-out-l3out')
    l3extInstP = cobra.model.l3ext.InstP(l3extOut, prio=u'unspecified', matchT=u'AtleastOne', name=u'out-l3out3', descr=u'', targetDscp=u'unspecified')
    fvRsCons = cobra.model.fv.RsCons(l3extInstP, tnVzBrCPName=u'out-to-web', prio=u'unspecified')
    l3extSubnet = cobra.model.l3ext.Subnet(l3extInstP, aggregate=u'', ip=u'10.70.0.0/24', name=u'', descr=u'')
    fvRsCustQosPol = cobra.model.fv.RsCustQosPol(l3extInstP, tnQosCustomPolName=u'')
    ospfExtP = cobra.model.ospf.ExtP(l3extOut, areaCtrl=u'redistribute,summary', areaId=u'0.0.0.2', areaType=u'regular', areaCost=u'1', descr=u'')


# commit the generated code to APIC
print toXMLStr(fvTenant)
c = cobra.mit.request.ConfigRequest()
c.addMo(fvTenant)
md.commit(c)

