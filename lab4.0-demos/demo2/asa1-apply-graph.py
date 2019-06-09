#!/usr/bin/env python

# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.fv
import cobra.model.l3ext
import cobra.model.pol
import cobra.model.vns
import cobra.model.vz
from cobra.internal.codec.xmlcodec import toXMLStr
import sys
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

# build the request using cobra syntax
polUni = cobra.model.pol.Uni('')
fvTenant = cobra.model.fv.Tenant(polUni, '%s' % tenant_name)

fvAp = cobra.model.fv.Ap(fvTenant,prio=u'unspecified', name=u'aProf')
fvAEPg = cobra.model.fv.AEPg(fvAp,matchT=u'AtleastOne', name=u'web')

fvRsProv = cobra.model.fv.RsProv(fvAEPg, tnVzBrCPName=u'out-to-web')
vzBrCP = cobra.model.vz.BrCP(fvTenant, name=u'out-to-web', scope=u'tenant')

vzSubj = cobra.model.vz.Subj(vzBrCP, name=u'Subject')
vns = cobra.model.vns.RtrCfg(fvTenant, ownerKey=u'', name=u'asa-cluster', descr=u'ASA cluster routerID', ownerTag=u'', rtrId=u'103.0.0.1')

vzRsSubjFiltAtt = cobra.model.vz.RsSubjFiltAtt(vzSubj, tnVzFilterName=u'default')
vzRsSubjGraphAtt = cobra.model.vz.RsSubjGraphAtt(vzSubj, tnVnsAbsGraphName=u'asa1-graph')
vnsLDevCtx = cobra.model.vns.LDevCtx(fvTenant, ctrctNameOrLbl=u'out-to-web', graphNameOrLbl=u'asa1-graph', nodeNameOrLbl=u'FIREWALL')
vnsLIfCtx = cobra.model.vns.LIfCtx(vnsLDevCtx, connNameOrLbl=u'consumer')

vnsRsLIfCtxToInstP = cobra.model.vns.RsLIfCtxToInstP(vnsLIfCtx, tDn=u'uni/tn-%s/out-asa-clu-external/instP-l3out2-epg' % tenant_name)
vnsRsLIfCtxToLIf = cobra.model.vns.RsLIfCtxToLIf(vnsLIfCtx, tDn=u'uni/tn-%s/lDevVip-asa1-l3out/lIf-external' % tenant_name)
vnsLIfCtx2 = cobra.model.vns.LIfCtx(vnsLDevCtx, connNameOrLbl=u'provider')
vnsRsLIfCtxToInstP2 = cobra.model.vns.RsLIfCtxToInstP(vnsLIfCtx2, tDn=u'uni/tn-%s/out-asa-clu-internal/instP-l3out1-epg' % tenant_name)
vnsRsLIfCtxToLIf2 = cobra.model.vns.RsLIfCtxToLIf(vnsLIfCtx2, tDn=u'uni/tn-%s/lDevVip-asa1-l3out/lIf-internal' % tenant_name)
vnsRsLDevCtxToLDev = cobra.model.vns.RsLDevCtxToLDev(vnsLDevCtx, tDn=u'uni/tn-%s/lDevVip-asa1-l3out' % tenant_name)
vnsRsLDevCtxToRtrCfg = cobra.model.vns.RsLDevCtxToRtrCfg(vnsLDevCtx, tnVnsRtrCfgName=u'asa-cluster')

l3extOut = cobra.model.l3ext.Out(fvTenant, name=u'outside-L3Out3')
l3extInstP = cobra.model.l3ext.InstP(l3extOut, name=u'out-l3out3')

fvRsCons = cobra.model.fv.RsCons(l3extInstP, tnVzBrCPName=u'out-to-web')


# commit the generated code to APIC
print toXMLStr(fvTenant)
c = cobra.mit.request.ConfigRequest()
c.addMo(fvTenant)
md.commit(c)

