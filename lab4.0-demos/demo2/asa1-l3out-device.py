#!/usr/bin/env python

# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.fv
import cobra.model.pol
import cobra.model.vns
import sys
from cobra.internal.codec.xmlcodec import toXMLStr


pod_num = int(sys.argv[1])
tenant_name = sys.argv[2]
csr_ip = sys.argv[3]

lab_prefix,owner,ownersid,ownerpod = tenant_name.split("-")
tenant_login = '%s' % tenant_name

# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://198.19.254.61', '%s' % tenant_login, 'p%s' % tenant_login)

md = cobra.mit.access.MoDirectory(ls)
md.login()

# the top level object on which operations will be made
polUni = cobra.model.pol.Uni('')
fvTenant = cobra.model.fv.Tenant(polUni, '%s' % tenant_name)

# build the request using cobra syntax
vnsLDevVip = cobra.model.vns.LDevVip(fvTenant, isCopy='no', managed='yes', name='asa1-l3out', svcType='ADC', funcType='GoTo', promMode='no', devtype='PHYSICAL', packageModel='ASA5525', contextAware='single-Context', nameAlias='', trunking='no', mode='legacy-Mode')
vnsCCred = cobra.model.vns.CCred(vnsLDevVip, value='aciadmin', name='username', nameAlias='')
vnsRsMDevAtt = cobra.model.vns.RsMDevAtt(vnsLDevVip, tDn='uni/infra/mDev-CISCO-ASA-1.2')
vnsCCredSecret = cobra.model.vns.CCredSecret(vnsLDevVip, value=u'cisco', name='password', nameAlias='')
vnsCDev = cobra.model.vns.CDev(vnsLDevVip, vcenterName='', vmName='', name='_ASA_CNTXT_Active:pod%d' % pod_num, nameAlias='', devCtxLbl='')
vnsCCred2 = cobra.model.vns.CCred(vnsCDev, value='aciadmin', name='username', nameAlias='')
vnsCCredSecret2 = cobra.model.vns.CCredSecret(vnsCDev, value=u'cisco', name='password', nameAlias='')
vnsCIf = cobra.model.vns.CIf(vnsCDev, name='p1', nameAlias='', vnicName='')
vnsRsCIfPathAtt = cobra.model.vns.RsCIfPathAtt(vnsCIf, tDn='topology/pod-1/protpaths-101-102/pathep-[ASA5525-X-3-4-DATA]')
vnsCMgmt = cobra.model.vns.CMgmt(vnsCDev, host='%s' % csr_ip, name='', nameAlias='', port='44371')
vnsCMgmt2 = cobra.model.vns.CMgmt(vnsLDevVip, host='198.19.254.176', name='', nameAlias='', port='443')
vnsLIf = cobra.model.vns.LIf(vnsLDevVip, name='external', encap='unknown', nameAlias='')
vnsRsCIfAttN = cobra.model.vns.RsCIfAttN(vnsLIf, tDn='uni/tn-%s/lDevVip-asa1-l3out/cDev-_ASA_CNTXT_Active:pod%d/cIf-[p1]' % (tenant_name,pod_num))
vnsRsMetaIf = cobra.model.vns.RsMetaIf(vnsLIf, isConAndProv='no', tDn='uni/infra/mDev-CISCO-ASA-1.2/mIfLbl-external')
vnsLIf2 = cobra.model.vns.LIf(vnsLDevVip, name='internal', encap='unknown', nameAlias='')
vnsRsCIfAttN2 = cobra.model.vns.RsCIfAttN(vnsLIf2, tDn='uni/tn-%s/lDevVip-asa1-l3out/cDev-_ASA_CNTXT_Active:pod%d/cIf-[p1]' % (tenant_name,pod_num))
vnsRsMetaIf2 = cobra.model.vns.RsMetaIf(vnsLIf2, isConAndProv='no', tDn='uni/infra/mDev-CISCO-ASA-1.2/mIfLbl-internal')
vnsRsALDevToPhysDomP = cobra.model.vns.RsALDevToPhysDomP(vnsLDevVip, tDn='uni/phys-ASA5525-X-3-4-DATA')


# commit the generated code to APIC
print toXMLStr(fvTenant)
c = cobra.mit.request.ConfigRequest()
c.addMo(fvTenant)
md.commit(c)

