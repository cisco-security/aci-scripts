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
import sys
from cobra.internal.codec.xmlcodec import toXMLStr

pod_num_start = int(sys.argv[1])
pod_num_end = int(sys.argv[2])
ctx_ip_standby = 140
ctx_ip_active = 30

# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://10.10.35.10', 'pod%s' % pod_num_end, 'cisco')

md = cobra.mit.access.MoDirectory(ls)
md.login()

for pod_num in range(pod_num_start, (1 + pod_num_end)):
    # the top level object on which operations will be made
    polUni = cobra.model.pol.Uni('')
    fvTenant = cobra.model.fv.Tenant(polUni, 'pod%d' % pod_num)
    
    # build the request using cobra syntax
    vnsLDevVip = cobra.model.vns.LDevVip(fvTenant, name=u'pod%d-asa-clu' % pod_num, funcType=u'GoTo', devtype=u'PHYSICAL', contextAware=u'single-Context', mode=u'legacy-Mode')
    vnsRsMDevAtt = cobra.model.vns.RsMDevAtt(vnsLDevVip, tDn=u'uni/infra/mDev-CISCO-ASA-1.2')
    vnsCCred = cobra.model.vns.CCred(vnsLDevVip, name=u'username', value=u'aciadmin')
    vnsCCredSecret = cobra.model.vns.CCredSecret(vnsLDevVip, name=u'password', value=u'cisco')
    vnsCMgmt = cobra.model.vns.CMgmt(vnsLDevVip, host=u'10.10.10.20', name=u'', port=u'443')
    vnsRsALDevToPhysDomP = cobra.model.vns.RsALDevToPhysDomP(vnsLDevVip, tDn=u'uni/phys-asa_phys')
    vnsChkr = cobra.model.vns.Chkr(vnsLDevVip, name=u'')
    vnsCDev2 = cobra.model.vns.CDev(vnsLDevVip, vcenterName=u'', vmName=u'', name=u'pod%d-asa-clu_Device_1'% pod_num, devCtxLbl=u'')  
    vnsCCred3 = cobra.model.vns.CCred(vnsCDev2, name=u'username', value=u'aciadmin')
    vnsCCredSecret3 = cobra.model.vns.CCredSecret(vnsCDev2, name=u'password', value=u'cisco')
    vnsCMgmt3 = cobra.model.vns.CMgmt(vnsCDev2, host=u'10.10.10.%d' % (ctx_ip_active + pod_num), name=u'', port=u'443') 
    vnsCIf2 = cobra.model.vns.CIf(vnsCDev2, name=u'p10', vnicName=u'')
    vnsRsCIfPathAtt2 = cobra.model.vns.RsCIfPathAtt(vnsCIf2, tDn=u'topology/pod-1/protpaths-101-102/pathep-[vpc_aaep_asa1-asa2]' ) 
    vnsDevFolder2 = cobra.model.vns.DevFolder(vnsCDev2, name=u'ClusterConfig', key=u'ClusterConfig')
    vnsDevParam2 = cobra.model.vns.DevParam(vnsDevFolder2, value=u'in-cluster', name=u'cluster_role', key=u'cluster_role')
    vnsLIf = cobra.model.vns.LIf(vnsLDevVip, name=u'external')
    vnsRsMetaIf = cobra.model.vns.RsMetaIf(vnsLIf, tDn=u'uni/infra/mDev-CISCO-ASA-1.2/mIfLbl-external')

    setting = 'uni/tn-pod%d/lDevVip-pod%d-asa-clu/cDev-pod%d-asa-clu_Device_1/cIf-[p10]' % (pod_num, pod_num, pod_num)
    vnsRsCIfAtt2 = cobra.model.vns.RsCIfAtt(vnsLIf, tDn=u'%s' % setting) 

    vnsLIf2 = cobra.model.vns.LIf(vnsLDevVip, name=u'internal')

    vnsRsMetaIf2 = cobra.model.vns.RsMetaIf(vnsLIf2, tDn=u'uni/infra/mDev-CISCO-ASA-1.2/mIfLbl-internal')

    setting =  'uni/tn-pod%d/lDevVip-pod%d-asa-clu/cDev-pod%d-asa-clu_Device_1/cIf-[p10]' % (pod_num, pod_num, pod_num)
    vnsRsCIfAtt4 = cobra.model.vns.RsCIfAtt(vnsLIf2, tDn=u'%s' % setting) 


    # commit the generated code to APIC
    print toXMLStr(fvTenant)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(fvTenant)
    md.commit(c)

