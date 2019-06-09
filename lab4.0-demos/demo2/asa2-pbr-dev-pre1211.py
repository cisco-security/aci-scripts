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
vnsLDevVip = cobra.model.vns.LDevVip(fvTenant, isCopy=u'no', managed=u'yes', name=u'asa2-pbr', svcType=u'FW', funcType=u'GoTo', promMode=u'no', devtype=u'PHYSICAL', packageModel=u'ASA5525', contextAware=u'single-Context', nameAlias=u'', trunking=u'no', mode=u'legacy-Mode')
vnsRsALDevToPhysDomP = cobra.model.vns.RsALDevToPhysDomP(vnsLDevVip, tDn=u'uni/phys-ASA5525-X-1-2-DATA')


vnsLIf = cobra.model.vns.LIf(vnsLDevVip, name=u'external', encap=u'unknown', nameAlias=u'')
vnsRsMetaIf = cobra.model.vns.RsMetaIf(vnsLIf, isConAndProv=u'no', tDn=u'uni/infra/mDev-CISCO-ASA-1.2/mIfLbl-external')
vnsRsCIfAttN = cobra.model.vns.RsCIfAttN(vnsLIf, tDn=u'uni/tn-%s/lDevVip-asa2-pbr/cDev-_ASA_CNTXT_Active:pod%d/cIf-[p1]' % (tenant_name,pod_num))
vnsLIf2 = cobra.model.vns.LIf(vnsLDevVip, name=u'internal', encap=u'unknown', nameAlias=u'')
vnsRsMetaIf2 = cobra.model.vns.RsMetaIf(vnsLIf2, isConAndProv=u'no', tDn=u'uni/infra/mDev-CISCO-ASA-1.2/mIfLbl-internal')
vnsRsCIfAttN2 = cobra.model.vns.RsCIfAttN(vnsLIf2, tDn=u'uni/tn-%s/lDevVip-asa2-pbr/cDev-_ASA_CNTXT_Active:pod%d/cIf-[p1]' % (tenant_name,pod_num))
vnsCMgmt = cobra.model.vns.CMgmt(vnsLDevVip, host=u'198.19.254.173', name=u'', nameAlias=u'', port=u'443')
vnsCDev = cobra.model.vns.CDev(vnsLDevVip, vcenterName=u'', vmName=u'', name=u'_ASA_CNTXT_Active:pod%d' % pod_num, nameAlias=u'', devCtxLbl=u'')
vnsDevFolder = cobra.model.vns.DevFolder(vnsCDev, name=u'ClusterConfig', key=u'ClusterConfig', nameAlias=u'')
vnsDevParam = cobra.model.vns.DevParam(vnsDevFolder, value=u'in-cluster', name=u'cluster_role', key=u'cluster_role', nameAlias=u'')
vnsCMgmt2 = cobra.model.vns.CMgmt(vnsCDev, host=u'%s' % csr_ip, name=u'', nameAlias=u'', port=u'44361')
vnsCIf = cobra.model.vns.CIf(vnsCDev, name=u'p1', nameAlias=u'', vnicName=u'')
vnsRsCIfPathAtt2 = cobra.model.vns.RsCIfPathAtt(vnsCIf, tDn=u'topology/pod-1/protpaths-101-102/pathep-[ASA5525-X-1-2-DATA]')
vnsCCredSecret = cobra.model.vns.CCredSecret(vnsCDev, value=u'cisco', name=u'password', nameAlias=u'')
vnsCCred = cobra.model.vns.CCred(vnsCDev, value=u'aciadmin', name=u'username', nameAlias=u'')
vnsCCredSecret2 = cobra.model.vns.CCredSecret(vnsLDevVip, value=u'cisco', name=u'password', nameAlias=u'')
vnsRsMDevAtt = cobra.model.vns.RsMDevAtt(vnsLDevVip, tDn=u'uni/infra/mDev-CISCO-ASA-1.2')
vnsCCred2 = cobra.model.vns.CCred(vnsLDevVip, value=u'aciadmin', name=u'username', nameAlias=u'')
vnsDevFolder = cobra.model.vns.DevFolder(vnsLDevVip, name=u'SameSecurityTraffic', key=u'SameSecurityTraffic')
vnsDevParam = cobra.model.vns.DevParam(vnsDevFolder, name=u'Intra-interface', key=u'intra_interface', value=u'permit')




# commit the generated code to APIC
print toXMLStr(fvTenant)
c = cobra.mit.request.ConfigRequest()
c.addMo(fvTenant)
md.commit(c)

