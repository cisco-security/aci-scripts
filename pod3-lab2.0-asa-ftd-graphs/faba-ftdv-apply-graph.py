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
# list of packages that should be imported for this code to workimport cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.fv
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

for pod_num in range(pod_num_start, (1 + pod_num_end)):    
# the top level object on which operations will be made
    polUni = cobra.model.pol.Uni('')
    #topMo = cobra.model.pol.Uni('')
    
    
# build the request using cobra syntax
    fvTenant = cobra.model.fv.Tenant(polUni, 'pod%s' % pod_num)

    #fvAp = cobra.model.fv.Ap(fvTenant)
    #fvAEPg = cobra.model.fv.AEPg(fvAp)
    #fvRsCons = cobra.model.fv.RsCons(fvAEPg, tnVzBrCPName=u'app-to-db')
    #fvAEPg2 = cobra.model.fv.AEPg(fvAp)

    fvAp = cobra.model.fv.Ap(fvTenant, prio=u'unspecified', name=u'aprof')
    fvAEPg = cobra.model.fv.AEPg(fvAp, matchT=u'AtleastOne', name=u'app')
    fvRsCons = cobra.model.fv.RsCons(fvAEPg, tnVzBrCPName=u'app-to-db')
    fvAEPg2 = cobra.model.fv.AEPg(fvAp, matchT=u'AtleastOne', name=u'db')

    vnsFolderInst = cobra.model.vns.FolderInst(fvAEPg2, graphNameOrLbl=u'l3fw-ftdv-graph', ctrctNameOrLbl=u'app-to-db', key=u'ExIntfConfigRelFolder', nodeNameOrLbl=u'l3fw', name=u'ExtConfig')
    vnsCfgRelInst = cobra.model.vns.CfgRelInst(vnsFolderInst, targetName=u'externalInterface', name=u'ExtConfigrel', key=u'ExIntfConfigRel')
    vnsFolderInst2 = cobra.model.vns.FolderInst(fvAEPg2, graphNameOrLbl=u'l3fw-ftdv-graph', ctrctNameOrLbl=u'app-to-db', key=u'InIntfConfigRelFolder', nodeNameOrLbl=u'l3fw', name=u'IntConfig')
    vnsCfgRelInst2 = cobra.model.vns.CfgRelInst(vnsFolderInst2, targetName=u'internalInterface', name=u'InConfigrel', key=u'InIntfConfigRel')
    vnsFolderInst3 = cobra.model.vns.FolderInst(fvAEPg2, graphNameOrLbl=u'l3fw-ftdv-graph', ctrctNameOrLbl=u'app-to-db', key=u'SecurityZone', nodeNameOrLbl=u'l3fw', name=u'app-zone')
    vnsParamInst = cobra.model.vns.ParamInst(vnsFolderInst3, value=u'ROUTED', name=u'type', key=u'type')
    vnsFolderInst4 = cobra.model.vns.FolderInst(fvAEPg2, graphNameOrLbl=u'l3fw-ftdv-graph', ctrctNameOrLbl=u'app-to-db', key=u'SecurityZone', nodeNameOrLbl=u'l3fw', name=u'db-zone')
    vnsParamInst2 = cobra.model.vns.ParamInst(vnsFolderInst4, value=u'ROUTED', name=u'type', key=u'type')
    vnsFolderInst5 = cobra.model.vns.FolderInst(fvAEPg2, graphNameOrLbl=u'l3fw-ftdv-graph', ctrctNameOrLbl=u'app-to-db', key=u'InterfaceConfig', nodeNameOrLbl=u'l3fw', name=u'externalInterface')
    vnsFolderInst6 = cobra.model.vns.FolderInst(vnsFolderInst5, graphNameOrLbl=u'l3fw-ftdv-graph', ctrctNameOrLbl=u'app-to-db', key=u'IPv4Config', nodeNameOrLbl=u'l3fw', name=u'IPv4Config')
    vnsFolderInst7 = cobra.model.vns.FolderInst(vnsFolderInst6, graphNameOrLbl=u'l3fw-ftdv-graph', ctrctNameOrLbl=u'app-to-db', key=u'static', nodeNameOrLbl=u'l3fw', name=u'static')
    vnsParamInst3 = cobra.model.vns.ParamInst(vnsFolderInst7, value=u'10.1.0.1/16', name=u'address', key=u'address')
    vnsFolderInst8 = cobra.model.vns.FolderInst(vnsFolderInst5, graphNameOrLbl=u'l3fw-ftdv-graph', ctrctNameOrLbl=u'app-to-db', key=u'int_security_zone', nodeNameOrLbl=u'l3fw', name=u'int_security_zone')
    vnsCfgRelInst3 = cobra.model.vns.CfgRelInst(vnsFolderInst8, targetName=u'app-zone', name=u'security_zone', key=u'security_zone')
    vnsParamInst4 = cobra.model.vns.ParamInst(vnsFolderInst5, value=u'true', name=u'enabled', key=u'enabled')
    vnsParamInst5 = cobra.model.vns.ParamInst(vnsFolderInst5, value=u'appnic', name=u'ifname', key=u'ifname')
    vnsFolderInst9 = cobra.model.vns.FolderInst(fvAEPg2, graphNameOrLbl=u'l3fw-ftdv-graph', ctrctNameOrLbl=u'app-to-db', key=u'InterfaceConfig', nodeNameOrLbl=u'l3fw', name=u'internalInterface')
    vnsFolderInst10 = cobra.model.vns.FolderInst(vnsFolderInst9, graphNameOrLbl=u'l3fw-ftdv-graph', ctrctNameOrLbl=u'app-to-db', key=u'IPv4Config', nodeNameOrLbl=u'l3fw', name=u'IPv4Config')
    vnsFolderInst11 = cobra.model.vns.FolderInst(vnsFolderInst10, graphNameOrLbl=u'l3fw-ftdv-graph', ctrctNameOrLbl=u'app-to-db', key=u'static', nodeNameOrLbl=u'l3fw', name=u'static')
    vnsParamInst6 = cobra.model.vns.ParamInst(vnsFolderInst11, value=u'10.2.0.1/24', name=u'address', key=u'address')
    vnsFolderInst12 = cobra.model.vns.FolderInst(vnsFolderInst9, graphNameOrLbl=u'l3fw-ftdv-graph', ctrctNameOrLbl=u'app-to-db', key=u'int_security_zone', nodeNameOrLbl=u'l3fw', name=u'int_security_zone')
    vnsCfgRelInst4 = cobra.model.vns.CfgRelInst(vnsFolderInst12, targetName=u'db-zone', name=u'security_zone', key=u'security_zone')
    vnsParamInst7 = cobra.model.vns.ParamInst(vnsFolderInst9, value=u'true', name=u'enabled', key=u'enabled')
    vnsParamInst8 = cobra.model.vns.ParamInst(vnsFolderInst9, value=u'dbnic', name=u'ifname', key=u'ifname')
    fvRsProv = cobra.model.fv.RsProv(fvAEPg2, tnVzBrCPName=u'app-to-db')
    vzBrCP = cobra.model.vz.BrCP(fvTenant, name=u'app-to-db')
    vzSubj = cobra.model.vz.Subj(vzBrCP, name=u'Subject')
    vzRsSubjFiltAtt = cobra.model.vz.RsSubjFiltAtt(vzSubj, tnVzFilterName=u'default')
    vzRsSubjGraphAtt = cobra.model.vz.RsSubjGraphAtt(vzSubj, tnVnsAbsGraphName=u'l3fw-ftdv-graph')
    vnsLDevCtx = cobra.model.vns.LDevCtx(fvTenant, ctrctNameOrLbl=u'app-to-db', graphNameOrLbl=u'l3fw-ftdv-graph', nodeNameOrLbl=u'l3fw')
    vnsLIfCtx = cobra.model.vns.LIfCtx(vnsLDevCtx, connNameOrLbl=u'consumer')
    vnsRsLIfCtxToBD = cobra.model.vns.RsLIfCtxToBD(vnsLIfCtx, tDn=u'uni/tn-pod%d/BD-web' % pod_num)
    vnsRsLIfCtxToLIf = cobra.model.vns.RsLIfCtxToLIf(vnsLIfCtx, tDn=u'uni/tn-pod%d/lDevVip-pod%d-vFTD-l3fw/lIf-app' % (pod_num,pod_num))
    vnsLIfCtx2 = cobra.model.vns.LIfCtx(vnsLDevCtx, connNameOrLbl=u'provider')
    vnsRsLIfCtxToBD2 = cobra.model.vns.RsLIfCtxToBD(vnsLIfCtx2, tDn=u'uni/tn-pod%d/BD-db' % pod_num)
    vnsRsLIfCtxToLIf2 = cobra.model.vns.RsLIfCtxToLIf(vnsLIfCtx2, tDn=u'uni/tn-pod%d/lDevVip-pod%d-vFTD-l3fw/lIf-db' % (pod_num,pod_num))
    vnsRsLDevCtxToLDev = cobra.model.vns.RsLDevCtxToLDev(vnsLDevCtx, tDn=u'uni/tn-pod%d/lDevVip-pod%d-vFTD-l3fw' % (pod_num,pod_num))
    
    
    # commit the generated code to APIC
    print toXMLStr(fvTenant)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(fvTenant)
    md.commit(c)


