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
Script uses a wizard to apply the service graph and create out-to-web contract,
filter, and apply the service graph.
"""

# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.fv
import cobra.model.l3ext
import cobra.model.pol
import cobra.model.vns
import cobra.model.vz
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

    # build the request using cobra syntax
    polUni = cobra.model.pol.Uni('')
    fvTenant = cobra.model.fv.Tenant(polUni, 'pod%s' % pod_num)
    fvAp = cobra.model.fv.Ap(fvTenant,prio=u'unspecified', name=u'aprof')
    fvAEPg = cobra.model.fv.AEPg(fvAp,matchT=u'AtleastOne', name=u'web')

    fvRsProv = cobra.model.fv.RsProv(fvAEPg, tnVzBrCPName=u'out-to-web')
    vzBrCP = cobra.model.vz.BrCP(fvTenant, name=u'out-to-web', scope=u'tenant')

    vzSubj = cobra.model.vz.Subj(vzBrCP, name=u'Subject')
    vns = cobra.model.vns.RtrCfg(fvTenant, ownerKey=u'', name=u'asa-cluster', descr=u'ASA cluster routerID', ownerTag=u'', rtrId=u'103.0.0.1')

    vzRsSubjFiltAtt = cobra.model.vz.RsSubjFiltAtt(vzSubj, tnVzFilterName=u'default')
    vzRsSubjGraphAtt = cobra.model.vz.RsSubjGraphAtt(vzSubj, tnVnsAbsGraphName=u'asa-clu-graph')
    vnsLDevCtx = cobra.model.vns.LDevCtx(fvTenant, ctrctNameOrLbl=u'out-to-web', graphNameOrLbl=u'asa-clu-graph', nodeNameOrLbl=u'FIREWALL')
    vnsLIfCtx = cobra.model.vns.LIfCtx(vnsLDevCtx, connNameOrLbl=u'consumer')
    vnsRsLIfCtxToInstP = cobra.model.vns.RsLIfCtxToInstP(vnsLIfCtx, tDn=u'uni/tn-pod%s/out-asa-clu-external/instP-l3out2-epg' % pod_num)
    vnsRsLIfCtxToLIf = cobra.model.vns.RsLIfCtxToLIf(vnsLIfCtx, tDn=u'uni/tn-pod%s/lDevVip-pod%s-asa-clu/lIf-external' % (pod_num,pod_num))
    vnsLIfCtx2 = cobra.model.vns.LIfCtx(vnsLDevCtx, connNameOrLbl=u'provider')
    vnsRsLIfCtxToInstP2 = cobra.model.vns.RsLIfCtxToInstP(vnsLIfCtx2, tDn=u'uni/tn-pod%s/out-asa-clu-internal/instP-l3out1-epg' % pod_num)
    vnsRsLIfCtxToLIf2 = cobra.model.vns.RsLIfCtxToLIf(vnsLIfCtx2, tDn=u'uni/tn-pod%s/lDevVip-pod%s-asa-clu/lIf-internal' % (pod_num,pod_num))
    vnsRsLDevCtxToLDev = cobra.model.vns.RsLDevCtxToLDev(vnsLDevCtx, tDn=u'uni/tn-pod%s/lDevVip-pod%s-asa-clu' % (pod_num,pod_num))
    vnsRsLDevCtxToRtrCfg = cobra.model.vns.RsLDevCtxToRtrCfg(vnsLDevCtx, tnVnsRtrCfgName=u'asa-cluster')

    l3extOut = cobra.model.l3ext.Out(fvTenant, name=u'wan-out')
    l3extInstP = cobra.model.l3ext.InstP(l3extOut, name=u'out-l3out3')

    fvRsCons = cobra.model.fv.RsCons(l3extInstP, tnVzBrCPName=u'out-to-web')


# commit the generated code to APIC
print toXMLStr(fvTenant)
c = cobra.mit.request.ConfigRequest()
c.addMo(fvTenant)
md.commit(c)

