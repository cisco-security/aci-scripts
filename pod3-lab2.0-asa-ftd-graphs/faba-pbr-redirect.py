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
    vnsSvcCont = cobra.model.vns.SvcCont(fvTenant)

    # build the request using cobra syntax
    vnsSvcRedirectPol = cobra.model.vns.SvcRedirectPol(vnsSvcCont, ownerKey=u'', name=u'pbr', descr=u'', ownerTag=u'')
    vnsRedirectDest = cobra.model.vns.RedirectDest(vnsSvcRedirectPol, ip=u'10.3.0.1', mac=u'00:10:00:03:00:01', name=u'', descr=u'')


    # commit the generated code to APIC
    print toXMLStr(vnsSvcCont)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(vnsSvcCont)
    md.commit(c)

