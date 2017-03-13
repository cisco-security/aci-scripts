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
ctx_ip_standby = 80
ctx_ip_active = 80
admin_ip = 22

# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://10.10.35.10', 'pod%s' % pod_num_end, 'cisco')
md = cobra.mit.access.MoDirectory(ls)
md.login()

for pod_num in range(pod_num_start, (1 + pod_num_end)):
    # the top level object on which operations will be made
    polUni = cobra.model.pol.Uni('')
    fvTenant = cobra.model.fv.Tenant(polUni, 'pod%d' % pod_num)
    if pod_num >= 21:
        admin_ip = 26

    vnsLDevVip = cobra.model.vns.LDevVip(fvTenant, isCopy=u'no', managed=u'yes', name=u'pod%d-vFTD-l3fw' % pod_num, svcType=u'FW', funcType=u'GoTo', devtype=u'VIRTUAL', packageModel=u'VIRTUAL', contextAware=u'single-Context', trunking=u'no', mode=u'legacy-Mode')
    vnsRsMDevAtt = cobra.model.vns.RsMDevAtt(vnsLDevVip, tDn=u'uni/infra/mDev-Cisco-FTD-1.0')
    vnsCCred = cobra.model.vns.CCred(vnsLDevVip, name=u'username', value=u'apiuser')
    vnsCCredSecret = cobra.model.vns.CCredSecret(vnsLDevVip, name=u'password', value=u'cisco')
    vnsRsALDevToDomP = cobra.model.vns.RsALDevToDomP(vnsLDevVip, tDn=u'uni/vmmp-VMware/dom-lab_vmm1')
    vnsCMgmt = cobra.model.vns.CMgmt(vnsLDevVip, host=u'10.10.30.%d' % pod_num, name=u'', port=u'443')
    vnsRsALDevToDevMgr = cobra.model.vns.RsALDevToDevMgr(vnsLDevVip, tnVnsDevMgrName=u'fmc62')
    vnsCDev = cobra.model.vns.CDev(vnsLDevVip, vcenterName=u'VC1', vmName=u'ACISEC-vFTD1-pod%d' % pod_num, name=u'Device1', devCtxLbl=u'')
    vnsCCred2 = cobra.model.vns.CCred(vnsCDev, name=u'username', value=u'apiuser')
    vnsCCredSecret2 = cobra.model.vns.CCredSecret(vnsCDev, name=u'password', value=u'cisco')
    vnsCMgmt2 = cobra.model.vns.CMgmt(vnsCDev, host=u'10.0.0.51', name=u'', port=u'443')
    vnsCIf = cobra.model.vns.CIf(vnsCDev, name=u'GigabitEthernet0/1', vnicName=u'Network adapter 3')
    vnsCIf2 = cobra.model.vns.CIf(vnsCDev, name=u'GigabitEthernet0/2', vnicName=u'Network adapter 4')
    vnsRsCDevToCtrlrP = cobra.model.vns.RsCDevToCtrlrP(vnsCDev, tDn=u'uni/vmmp-VMware/dom-lab_vmm1/ctrlr-VC1')
    vnsLIf = cobra.model.vns.LIf(vnsLDevVip, name=u'app', encap=u'unknown')
    vnsRsMetaIf = cobra.model.vns.RsMetaIf(vnsLIf, isConAndProv=u'no', tDn=u'uni/infra/mDev-Cisco-FTD-1.0/mIfLbl-external')
    vnsRsCIfAttN = cobra.model.vns.RsCIfAttN(vnsLIf, tDn=u'uni/tn-pod%d/lDevVip-pod%d-vFTD-l3fw/cDev-Device1/cIf-[GigabitEthernet0/1]' % (pod_num, pod_num))
    vnsLIf2 = cobra.model.vns.LIf(vnsLDevVip, name=u'db', encap=u'unknown')
    vnsRsMetaIf2 = cobra.model.vns.RsMetaIf(vnsLIf2, isConAndProv=u'no', tDn=u'uni/infra/mDev-Cisco-FTD-1.0/mIfLbl-internal')
    vnsRsCIfAttN2 = cobra.model.vns.RsCIfAttN(vnsLIf2, tDn=u'uni/tn-pod%d/lDevVip-pod%d-vFTD-l3fw/cDev-Device1/cIf-[GigabitEthernet0/2]'% (pod_num, pod_num))




    # commit the generated code to APIC
    print toXMLStr(fvTenant)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(fvTenant)
    md.commit(c)

