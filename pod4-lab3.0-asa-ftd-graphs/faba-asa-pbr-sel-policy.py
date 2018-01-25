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
	vnsLDevCtx = cobra.model.vns.LDevCtx(fvTenant, name=u'', descr=u'', ctrctNameOrLbl=u'web-to-app', graphNameOrLbl=u'asa-pbr-graph', nodeNameOrLbl=u'asa-pbr')
	vnsRsLDevCtxToLDev = cobra.model.vns.RsLDevCtxToLDev(vnsLDevCtx, tDn=u'uni/tn-pod%d/lDevVip-pod%d-asa-pbr-fover' % (pod_num, pod_num))
	vnsLIfCtx = cobra.model.vns.LIfCtx(vnsLDevCtx, permitLog=u'no', name=u'', descr=u'', connNameOrLbl=u'provider')
	vnsRsLIfCtxToSvcRedirectPol = cobra.model.vns.RsLIfCtxToSvcRedirectPol(vnsLIfCtx, tDn=u'uni/tn-pod%d/svcCont/svcRedirectPol-pbr' % pod_num)
	vnsRsLIfCtxToBD = cobra.model.vns.RsLIfCtxToBD(vnsLIfCtx, tDn=u'uni/tn-pod%d/BD-pbr-bd' % pod_num)
	vnsRsLIfCtxToLIf = cobra.model.vns.RsLIfCtxToLIf(vnsLIfCtx, tDn=u'uni/tn-pod%d/lDevVip-pod%d-asa-pbr-fover/lIf-consumer' % (pod_num, pod_num))
	vnsLIfCtx2 = cobra.model.vns.LIfCtx(vnsLDevCtx, permitLog=u'no', name=u'', descr=u'', connNameOrLbl=u'consumer')
	vnsRsLIfCtxToSvcRedirectPol2 = cobra.model.vns.RsLIfCtxToSvcRedirectPol(vnsLIfCtx2, tDn=u'uni/tn-pod%d/svcCont/svcRedirectPol-pbr' % pod_num)
	vnsRsLIfCtxToBD2 = cobra.model.vns.RsLIfCtxToBD(vnsLIfCtx2, tDn=u'uni/tn-pod%d/BD-pbr-bd' % pod_num)
	vnsRsLIfCtxToLIf2 = cobra.model.vns.RsLIfCtxToLIf(vnsLIfCtx2, tDn=u'uni/tn-pod%d/lDevVip-pod%d-asa-pbr-fover/lIf-consumer' % (pod_num, pod_num))


	# commit the generated code to APIC
	print toXMLStr(fvTenant)
	c = cobra.mit.request.ConfigRequest()
	c.addMo(fvTenant)
	md.commit(c)

