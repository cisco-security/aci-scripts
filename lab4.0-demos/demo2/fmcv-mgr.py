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
vnsDevMgr = cobra.model.vns.DevMgr(fvTenant, ownerKey=u'', name=u'fmc62', descr=u'', ownerTag=u'')
vnsCCred = cobra.model.vns.CCred(vnsDevMgr, name=u'username', value=u'apiuser')
vnsCCredSecret = cobra.model.vns.CCredSecret(vnsDevMgr, name=u'password', value=u'cisco')
vnsCMgmts = cobra.model.vns.CMgmts(vnsDevMgr, host=u'%s' % csr_ip, name=u'', port=u'44330')
vnsRsDevMgrToMDevMgr = cobra.model.vns.RsDevMgrToMDevMgr(vnsDevMgr, tDn=u'uni/infra/mDevMgr-CISCO-FTDmgr_FI-1.0')


# commit the generated code to APIC
print toXMLStr(fvTenant)
c = cobra.mit.request.ConfigRequest()
c.addMo(fvTenant)
md.commit(c)

