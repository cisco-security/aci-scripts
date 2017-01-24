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
import cobra.model.aaa
import cobra.model.fv
import cobra.model.pol
import cobra.model.vz
from cobra.internal.codec.xmlcodec import toXMLStr
import sys
pod_num_start = int(sys.argv[1])
pod_num_end = int(sys.argv[2])

# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://10.10.35.10', 'admin', 'aciSEC2015')

md = cobra.mit.access.MoDirectory(ls)
md.login()

# the top level object on which operations will be made
for x in range(pod_num_start, (1 + pod_num_end)):
    polUni = cobra.model.pol.Uni('')
    # build the request using cobra syntax
    fvTenant = cobra.model.fv.Tenant(polUni, ownerKey=u'', name=u'pod%s' % x, descr=u'', ownerTag=u'')
    aaaDomainRef = cobra.model.aaa.DomainRef(fvTenant, ownerKey=u'', name=u'pod%s' % x, descr=u'', ownerTag=u'')
    fvCtx = cobra.model.fv.Ctx(fvTenant, ownerKey=u'', name=u'pod%snet' % x, descr=u'', knwMcastAct=u'permit', ownerTag=u'', pcEnfPref=u'enforced')
    fvRsCtxToExtRouteTagPol = cobra.model.fv.RsCtxToExtRouteTagPol(fvCtx, tnL3extRouteTagPolName=u'')
    fvRsBgpCtxPol = cobra.model.fv.RsBgpCtxPol(fvCtx, tnBgpCtxPolName=u'')
    vzAny = cobra.model.vz.Any(fvCtx, matchT=u'AtleastOne', name=u'', descr=u'')
    fvRsOspfCtxPol = cobra.model.fv.RsOspfCtxPol(fvCtx, tnOspfCtxPolName=u'')
    fvRsCtxToEpRet = cobra.model.fv.RsCtxToEpRet(fvCtx, tnFvEpRetPolName=u'')
    fvBD = cobra.model.fv.BD(fvTenant, ownerKey=u'', name=u'db', descr=u'', unkMacUcastAct=u'flood', arpFlood=u'yes', limitIpLearnToSubnets=u'no', llAddr=u'::', mac=u'00:22:BD:F8:19:FF', epMoveDetectMode=u'', unicastRoute=u'yes', ownerTag=u'', multiDstPktAct=u'bd-flood', unkMcastAct=u'flood')
    fvRsBDToNdP = cobra.model.fv.RsBDToNdP(fvBD, tnNdIfPolName=u'')
    fvRsCtx = cobra.model.fv.RsCtx(fvBD, tnFvCtxName=u'pod%snet' % x)
    fvRsIgmpsn = cobra.model.fv.RsIgmpsn(fvBD, tnIgmpSnoopPolName=u'')
    fvRsBdToEpRet = cobra.model.fv.RsBdToEpRet(fvBD, resolveAct=u'resolve', tnFvEpRetPolName=u'')
    fvBD2 = cobra.model.fv.BD(fvTenant, ownerKey=u'', name=u'app', descr=u'', unkMacUcastAct=u'flood', arpFlood=u'yes', limitIpLearnToSubnets=u'no', llAddr=u'::', mac=u'00:22:BD:F8:19:FF', epMoveDetectMode=u'', unicastRoute=u'yes', ownerTag=u'', multiDstPktAct=u'bd-flood', unkMcastAct=u'flood')
    fvRsBDToNdP2 = cobra.model.fv.RsBDToNdP(fvBD2, tnNdIfPolName=u'')
    fvRsCtx2 = cobra.model.fv.RsCtx(fvBD2, tnFvCtxName=u'pod%snet' % x)
    fvRsIgmpsn2 = cobra.model.fv.RsIgmpsn(fvBD2, tnIgmpSnoopPolName=u'')
    fvRsBdToEpRet2 = cobra.model.fv.RsBdToEpRet(fvBD2, resolveAct=u'resolve', tnFvEpRetPolName=u'')
    fvBD3 = cobra.model.fv.BD(fvTenant, ownerKey=u'', name=u'web', descr=u'', unkMacUcastAct=u'flood', arpFlood=u'yes', limitIpLearnToSubnets=u'no', llAddr=u'::', mac=u'00:22:BD:F8:19:FF', epMoveDetectMode=u'', unicastRoute=u'yes', ownerTag=u'', multiDstPktAct=u'bd-flood', unkMcastAct=u'flood')
    fvRsBDToNdP3 = cobra.model.fv.RsBDToNdP(fvBD3, tnNdIfPolName=u'')
    fvRsCtx3 = cobra.model.fv.RsCtx(fvBD3, tnFvCtxName=u'pod%snet' % x)
    fvRsIgmpsn3 = cobra.model.fv.RsIgmpsn(fvBD3, tnIgmpSnoopPolName=u'')
    fvSubnet = cobra.model.fv.Subnet(fvBD3, name=u'', descr=u'', ctrl=u'', ip=u'10.1.0.2/24', preferred=u'no')
    fvRsBdToEpRet3 = cobra.model.fv.RsBdToEpRet(fvBD3, resolveAct=u'resolve', tnFvEpRetPolName=u'')
    fvRsTenantMonPol = cobra.model.fv.RsTenantMonPol(fvTenant, tnMonEPGPolName=u'')
    fvAp = cobra.model.fv.Ap(fvTenant, ownerKey=u'', prio=u'unspecified', name=u'aprof', descr=u'', ownerTag=u'')
    fvAEPg = cobra.model.fv.AEPg(fvAp, prio=u'unspecified', matchT=u'AtleastOne', name=u'app', descr=u'')
    fvRsDomAtt = cobra.model.fv.RsDomAtt(fvAEPg, instrImedcy=u'lazy', resImedcy=u'lazy', encap=u'unknown', tDn=u'uni/vmmp-VMware/dom-lab_vmm1')
    fvRsCustQosPol = cobra.model.fv.RsCustQosPol(fvAEPg, tnQosCustomPolName=u'')
    fvRsBd = cobra.model.fv.RsBd(fvAEPg, tnFvBDName=u'web')
    fvAEPg2 = cobra.model.fv.AEPg(fvAp, prio=u'unspecified', matchT=u'AtleastOne', name=u'web', descr=u'')
    fvRsDomAtt2 = cobra.model.fv.RsDomAtt(fvAEPg2, instrImedcy=u'lazy', resImedcy=u'lazy', encap=u'unknown', tDn=u'uni/vmmp-VMware/dom-lab_vmm1')
    fvRsCustQosPol2 = cobra.model.fv.RsCustQosPol(fvAEPg2, tnQosCustomPolName=u'')
    fvRsBd2 = cobra.model.fv.RsBd(fvAEPg2, tnFvBDName=u'web')
    fvAEPg3 = cobra.model.fv.AEPg(fvAp, prio=u'unspecified', matchT=u'AtleastOne', name=u'db', descr=u'')
    fvRsDomAtt3 = cobra.model.fv.RsDomAtt(fvAEPg3, instrImedcy=u'lazy', resImedcy=u'lazy', encap=u'unknown', tDn=u'uni/vmmp-VMware/dom-lab_vmm1')
    fvRsCustQosPol3 = cobra.model.fv.RsCustQosPol(fvAEPg3, tnQosCustomPolName=u'')
    fvRsBd3 = cobra.model.fv.RsBd(fvAEPg3, tnFvBDName=u'db')


    # commit the generated code to APIC
    print toXMLStr(polUni)
    c = cobra.mit.request.ConfigRequest()
    #c.addMo(polUni)
    c.addMo(fvTenant)
    md.commit(c)

