#!usr/bin/env python

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
session_id = sys.argv[4]

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
vnsLDevVip = cobra.model.vns.LDevVip(fvTenant, isCopy=u'no', managed=u'yes', name=u'vFTD-l3fw', svcType=u'FW', funcType=u'GoTo', devtype=u'VIRTUAL', packageModel=u'VIRTUAL', contextAware=u'single-Context', nameAlias=u'', trunking=u'no', mode=u'legacy-Mode')
vnsLIf = cobra.model.vns.LIf(vnsLDevVip, name=u'db', encap=u'unknown', nameAlias=u'')
vnsRsMetaIf = cobra.model.vns.RsMetaIf(vnsLIf, isConAndProv=u'no', tDn=u'uni/infra/mDev-CISCO-FTD_FI-1.0/mIfLbl-internal')
vnsRsCIfAttN = cobra.model.vns.RsCIfAttN(vnsLIf, tDn=u'uni/tn-%s/lDevVip-vFTD-l3fw/cDev-Device2/cIf-[GigabitEthernet0/2]' % tenant_name)
vnsRsCIfAttN2 = cobra.model.vns.RsCIfAttN(vnsLIf, tDn=u'uni/tn-%s/lDevVip-vFTD-l3fw/cDev-Device1/cIf-[GigabitEthernet0/2]' % tenant_name)
vnsLIf2 = cobra.model.vns.LIf(vnsLDevVip, name=u'app', encap=u'unknown', nameAlias=u'')
vnsRsMetaIf2 = cobra.model.vns.RsMetaIf(vnsLIf2, isConAndProv=u'no', tDn=u'uni/infra/mDev-CISCO-FTD_FI-1.0/mIfLbl-external')
vnsRsCIfAttN3 = cobra.model.vns.RsCIfAttN(vnsLIf2, tDn=u'uni/tn-%s/lDevVip-vFTD-l3fw/cDev-Device2/cIf-[GigabitEthernet0/1]' % tenant_name)
vnsRsCIfAttN4 = cobra.model.vns.RsCIfAttN(vnsLIf2, tDn=u'uni/tn-%s/lDevVip-vFTD-l3fw/cDev-Device1/cIf-[GigabitEthernet0/1]' % tenant_name)
vnsRsALDevToDomP = cobra.model.vns.RsALDevToDomP(vnsLDevVip, tDn=u'uni/vmmp-VMware/dom-vmware60-hybridcloud')
vnsCMgmt = cobra.model.vns.CMgmt(vnsLDevVip, host=u'%s' % csr_ip, name=u'', nameAlias=u'', port=u'44330')
vnsRsALDevToDevMgr = cobra.model.vns.RsALDevToDevMgr(vnsLDevVip, tnVnsDevMgrName=u'fmc62')
vnsCDev = cobra.model.vns.CDev(vnsLDevVip, vcenterName=u'vc60-aci-1', vmName=u'acisec-vftd1-%s-%s' % (session_id, pod_num), name=u'Device1', nameAlias=u'', devCtxLbl=u'' )
vnsRsCDevToCtrlrP = cobra.model.vns.RsCDevToCtrlrP(vnsCDev, tDn=u'uni/vmmp-VMware/dom-vmware60-hybridcloud/ctrlr-vc60-aci-1')
vnsCMgmt2 = cobra.model.vns.CMgmt(vnsCDev, host=u'10.0.0.51', name=u'', nameAlias=u'', port=u'443')
vnsCIf = cobra.model.vns.CIf(vnsCDev, name=u'GigabitEthernet0/1', nameAlias=u'', vnicName=u'Network adapter 3')
vnsCIf2 = cobra.model.vns.CIf(vnsCDev, name=u'GigabitEthernet0/2', nameAlias=u'', vnicName=u'Network adapter 4')
vnsCCredSecret = cobra.model.vns.CCredSecret(vnsCDev, name=u'password', nameAlias=u'')
vnsCCred = cobra.model.vns.CCred(vnsCDev, value=u'aciadmin', name=u'username', nameAlias=u'')
vnsCDev2 = cobra.model.vns.CDev(vnsLDevVip, vcenterName=u'vc60-aci-1', vmName=u'acisec-vftd2-%s-%s' % (session_id, pod_num), name=u'Device2', nameAlias=u'', devCtxLbl=u'' )
vnsRsCDevToCtrlrP2 = cobra.model.vns.RsCDevToCtrlrP(vnsCDev2, tDn=u'uni/vmmp-VMware/dom-vmware60-hybridcloud/ctrlr-vc60-aci-1')
vnsCMgmt3 = cobra.model.vns.CMgmt(vnsCDev2, host=u'10.0.0.52', name=u'', nameAlias=u'', port=u'443')
vnsCIf3 = cobra.model.vns.CIf(vnsCDev2, name=u'GigabitEthernet0/1', nameAlias=u'', vnicName=u'Network adapter 3')
vnsCIf4 = cobra.model.vns.CIf(vnsCDev2, name=u'GigabitEthernet0/2', nameAlias=u'', vnicName=u'Network adapter 4')
vnsCCredSecret2 = cobra.model.vns.CCredSecret(vnsCDev2, name=u'password', nameAlias=u'')
vnsCCred2 = cobra.model.vns.CCred(vnsCDev2, value=u'aciadmin', name=u'username', nameAlias=u'')
vnsCCredSecret3 = cobra.model.vns.CCredSecret(vnsLDevVip, name=u'password', nameAlias=u'')
vnsRsMDevAtt = cobra.model.vns.RsMDevAtt(vnsLDevVip, tDn=u'uni/infra/mDev-CISCO-FTD_FI-1.0')
vnsCCred3 = cobra.model.vns.CCred(vnsLDevVip, value=u'aciadmin', name=u'username', nameAlias=u'')


# commit the generated code to APIC
print toXMLStr(fvTenant)
c = cobra.mit.request.ConfigRequest()
c.addMo(fvTenant)
md.commit(c)

