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

# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://10.10.35.10', 'pod%s' % pod_num_end, 'cisco')
md = cobra.mit.access.MoDirectory(ls)
md.login()

for pod_num in range(pod_num_start, (1 + pod_num_end)):

    # the top level object on which operations will be made
    polUni = cobra.model.pol.Uni('')
    fvTenant = cobra.model.fv.Tenant(polUni, 'pod%s' % pod_num)

    # build the request using cobra syntax
    vnsDevMgr = cobra.model.vns.DevMgr(fvTenant, ownerKey=u'', name=u'fmc62', descr=u'', ownerTag=u'')
    vnsCCred = cobra.model.vns.CCred(vnsDevMgr, name=u'username', value=u'apiuser')
    vnsCCredSecret = cobra.model.vns.CCredSecret(vnsDevMgr, name=u'password', value=u'cisco')
    vnsCMgmts = cobra.model.vns.CMgmts(vnsDevMgr, host=u'10.10.30.%d' % pod_num, name=u'', port=u'443')
    vnsRsDevMgrToMDevMgr = cobra.model.vns.RsDevMgrToMDevMgr(vnsDevMgr, tDn=u'uni/infra/mDevMgr-Cisco-FTDmgr-1.0')
    

    # commit the generated code to APIC
    print toXMLStr(fvTenant)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(fvTenant)
    md.commit(c)

