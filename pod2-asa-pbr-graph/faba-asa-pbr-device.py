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

    # build the request using cobra syntax
    vnsLDevVip = cobra.model.vns.LDevVip(fvTenant, isCopy=u'no', managed=u'yes', name=u'pod%d-asa-pbr-fover' % pod_num, svcType=u'FW', funcType=u'GoTo', devtype=u'PHYSICAL', packageModel=u'ASA5525', contextAware=u'single-Context', trunking=u'no', mode=u'legacy-Mode')
    vnsRsMDevAtt = cobra.model.vns.RsMDevAtt(vnsLDevVip, tDn=u'uni/infra/mDev-CISCO-ASA-1.2')
    vnsCCred = cobra.model.vns.CCred(vnsLDevVip, name=u'username', value=u'aciadmin')
    vnsCCredSecret = cobra.model.vns.CCredSecret(vnsLDevVip, name=u'password', value=u'cisco')
    vnsCMgmt = cobra.model.vns.CMgmt(vnsLDevVip, host=u'10.10.10.%d' % admin_ip, name=u'', port=u'443')
    vnsRsALDevToPhysDomP = cobra.model.vns.RsALDevToPhysDomP(vnsLDevVip, tDn=u'uni/phys-asa_fover')
    vnsDevFolder = cobra.model.vns.DevFolder(vnsLDevVip, name=u'SameSecurityTraffic', key=u'SameSecurityTraffic')
    vnsDevParam = cobra.model.vns.DevParam(vnsDevFolder, name=u'Intra-interface', key=u'intra_interface', value=u'permit')
    vnsCDev = cobra.model.vns.CDev(vnsLDevVip, vcenterName=u'', vmName=u'', name=u'Device2', devCtxLbl=u'')
    vnsCCred2 = cobra.model.vns.CCred(vnsCDev, name=u'username', value=u'aciadmin')
    vnsCCredSecret2 = cobra.model.vns.CCredSecret(vnsCDev, name=u'password', value=u'cisco')
    vnsCMgmt2 = cobra.model.vns.CMgmt(vnsCDev, host=u'10.10.11.%d' % (ctx_ip_standby + pod_num), name=u'', port=u'443')
    vnsCIf = cobra.model.vns.CIf(vnsCDev, name=u'GigabitEthernet0/4', vnicName=u'')
    vnsRsCIfPathAtt = cobra.model.vns.RsCIfPathAtt(vnsCIf, tDn=u'topology/pod-1/paths-102/pathep-[eth1/29]')
    vnsCDev2 = cobra.model.vns.CDev(vnsLDevVip, vcenterName=u'', vmName=u'', name=u'Device1', devCtxLbl=u'')
    vnsCCred3 = cobra.model.vns.CCred(vnsCDev2, name=u'username', value=u'aciadmin')
    vnsCCredSecret3 = cobra.model.vns.CCredSecret(vnsCDev2, name=u'password', value=u'cisco')
    vnsCMgmt3 = cobra.model.vns.CMgmt(vnsCDev2, host=u'10.10.10.%d' % (ctx_ip_active + pod_num), name=u'', port=u'443')
    vnsCIf2 = cobra.model.vns.CIf(vnsCDev2, name=u'GigabitEthernet0/4', vnicName=u'')
    vnsRsCIfPathAtt2 = cobra.model.vns.RsCIfPathAtt(vnsCIf2, tDn=u'topology/pod-1/paths-102/pathep-[eth1/25]')
    vnsLIf = cobra.model.vns.LIf(vnsLDevVip, name=u'provider', encap=u'unknown')
    vnsRsMetaIf = cobra.model.vns.RsMetaIf(vnsLIf, isConAndProv=u'no', tDn=u'uni/infra/mDev-CISCO-ASA-1.2/mIfLbl-internal')
    vnsRsCIfAttN = cobra.model.vns.RsCIfAttN(vnsLIf, tDn=u'uni/tn-pod%d/lDevVip-pod%d-asa-pbr-fover/cDev-Device2/cIf-[GigabitEthernet0/4]' % (pod_num, pod_num))
    vnsRsCIfAttN2 = cobra.model.vns.RsCIfAttN(vnsLIf, tDn=u'uni/tn-pod%d/lDevVip-pod%d-asa-pbr-fover/cDev-Device1/cIf-[GigabitEthernet0/4]' % (pod_num, pod_num))
    vnsLIf2 = cobra.model.vns.LIf(vnsLDevVip, name=u'consumer', encap=u'unknown')
    vnsRsMetaIf2 = cobra.model.vns.RsMetaIf(vnsLIf2, isConAndProv=u'no', tDn=u'uni/infra/mDev-CISCO-ASA-1.2/mIfLbl-external')
    vnsRsCIfAttN3 = cobra.model.vns.RsCIfAttN(vnsLIf2, tDn=u'uni/tn-pod%d/lDevVip-pod%d-asa-pbr-fover/cDev-Device2/cIf-[GigabitEthernet0/4]' % (pod_num, pod_num))
    vnsRsCIfAttN4 = cobra.model.vns.RsCIfAttN(vnsLIf2, tDn=u'uni/tn-pod%d/lDevVip-pod%d-asa-pbr-fover/cDev-Device1/cIf-[GigabitEthernet0/4]' % (pod_num, pod_num))


    # commit the generated code to APIC
    print toXMLStr(fvTenant)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(fvTenant)
    md.commit(c)

