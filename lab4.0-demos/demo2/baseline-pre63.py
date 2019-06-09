#!/usr/bin/env python
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.aaa
import cobra.model.fv
import cobra.model.l3ext
import cobra.model.pol
import cobra.model.vns
import cobra.model.vz
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


# build the request using cobra syntax



def createAciSecLabTenant(md,l3outVlan="2050", tenantName="ACISEC-myuser-123456-9"):

    polUni = cobra.model.pol.Uni('')

    fvTenant = cobra.model.fv.Tenant(polUni, ownerKey=u'', name=str(tenantName), descr=u'', nameAlias=u'', ownerTag=u'')

    #Security Domain
    aaaDomainRef = cobra.model.aaa.DomainRef(fvTenant, ownerKey=u'', ownerTag=u'', name=u'ACI-Security-Integration', descr=u'', nameAlias=u'')

    #Application Profile
    fvAp = cobra.model.fv.Ap(fvTenant, ownerKey=u'', name=u'aProf', prio=u'unspecified', descr=u'', nameAlias=u'', ownerTag=u'')

    #EPG: App
    fvAEPg = cobra.model.fv.AEPg(fvAp, isAttrBasedEPg=u'no', matchT=u'AtleastOne', name=u'app', descr=u'', fwdCtrl=u'', prefGrMemb=u'exclude', floodOnEncap=u'disabled', nameAlias=u'', prio=u'unspecified', pcEnfPref=u'unenforced')
    fvRsBd = cobra.model.fv.RsBd(fvAEPg, tnFvBDName=u'BD1')
    fvRsCustQosPol = cobra.model.fv.RsCustQosPol(fvAEPg, tnQosCustomPolName=u'')
    fvRsDomAtt = cobra.model.fv.RsDomAtt(fvAEPg, tDn=u'uni/vmmp-VMware/dom-vmware60-hybridcloud', netflowDir=u'both', epgCos=u'Cos0', classPref=u'encap', primaryEncap=u'unknown', secondaryEncapInner=u'unknown', resImedcy=u'lazy', delimiter=u'', instrImedcy=u'lazy', primaryEncapInner=u'unknown', encap=u'unknown', switchingMode=u'native', encapMode=u'auto', netflowPref=u'disabled', epgCosPref=u'disabled')

    #EPG: Db
    fvAEPg2 = cobra.model.fv.AEPg(fvAp, isAttrBasedEPg=u'no', matchT=u'AtleastOne', name=u'db', descr=u'', fwdCtrl=u'', prefGrMemb=u'exclude', floodOnEncap=u'disabled', nameAlias=u'', prio=u'unspecified', pcEnfPref=u'unenforced')
    fvRsBd2 = cobra.model.fv.RsBd(fvAEPg2, tnFvBDName=u'BD2')
    fvRsCustQosPol2 = cobra.model.fv.RsCustQosPol(fvAEPg2, tnQosCustomPolName=u'')
    fvRsDomAtt2 = cobra.model.fv.RsDomAtt(fvAEPg2, tDn=u'uni/vmmp-VMware/dom-vmware60-hybridcloud', netflowDir=u'both', epgCos=u'Cos0', classPref=u'encap', primaryEncap=u'unknown', secondaryEncapInner=u'unknown', resImedcy=u'lazy', delimiter=u'', instrImedcy=u'lazy', primaryEncapInner=u'unknown', encap=u'unknown', switchingMode=u'native', encapMode=u'auto', netflowPref=u'disabled', epgCosPref=u'disabled')

    #EPG: Web
    fvAEPg3 = cobra.model.fv.AEPg(fvAp, isAttrBasedEPg=u'no', matchT=u'AtleastOne', name=u'web', descr=u'', fwdCtrl=u'', prefGrMemb=u'exclude', floodOnEncap=u'disabled', nameAlias=u'', prio=u'unspecified', pcEnfPref=u'unenforced')
    fvRsBd3 = cobra.model.fv.RsBd(fvAEPg3, tnFvBDName=u'BD1')
    fvRsCustQosPol3 = cobra.model.fv.RsCustQosPol(fvAEPg3, tnQosCustomPolName=u'')
    fvRsDomAtt3 = cobra.model.fv.RsDomAtt(fvAEPg3, tDn=u'uni/vmmp-VMware/dom-vmware60-hybridcloud', netflowDir=u'both', epgCos=u'Cos0', classPref=u'encap', primaryEncap=u'unknown', secondaryEncapInner=u'unknown', resImedcy=u'lazy', delimiter=u'', instrImedcy=u'lazy', primaryEncapInner=u'unknown', encap=u'unknown', switchingMode=u'native', encapMode=u'auto', netflowPref=u'disabled', epgCosPref=u'disabled')

    #
    fvRsTenantMonPol = cobra.model.fv.RsTenantMonPol(fvTenant, tnMonEPGPolName=u'')

    #BD: BD1
    fvBD = cobra.model.fv.BD(fvTenant, multiDstPktAct=u'bd-flood', mcastAllow=u'no', limitIpLearnToSubnets=u'yes', unicastRoute=u'yes', unkMcastAct=u'flood', descr=u'', llAddr=u'::', nameAlias=u'', type=u'regular', ipLearning=u'yes', vmac=u'not-applicable', mac=u'00:22:BD:F8:19:FF', epMoveDetectMode=u'', ownerTag=u'', intersiteBumTrafficAllow=u'no', ownerKey=u'', name=u'BD1', epClear=u'no', unkMacUcastAct=u'proxy', arpFlood=u'no', intersiteL2Stretch=u'no', OptimizeWanBandwidth=u'no')
    fvRsBDToNdP = cobra.model.fv.RsBDToNdP(fvBD, tnNdIfPolName=u'')
    fvRsBdToEpRet = cobra.model.fv.RsBdToEpRet(fvBD, resolveAct=u'resolve', tnFvEpRetPolName=u'')
    fvRsCtx = cobra.model.fv.RsCtx(fvBD, tnFvCtxName=u'internalVRF')
    fvRsIgmpsn = cobra.model.fv.RsIgmpsn(fvBD, tnIgmpSnoopPolName=u'')

    #BD: BD2
    fvBD2 = cobra.model.fv.BD(fvTenant, multiDstPktAct=u'bd-flood', mcastAllow=u'no', limitIpLearnToSubnets=u'yes', unicastRoute=u'yes', unkMcastAct=u'flood', descr=u'', llAddr=u'::', nameAlias=u'', type=u'regular', ipLearning=u'yes', vmac=u'not-applicable', mac=u'00:22:BD:F8:19:FF', epMoveDetectMode=u'', ownerTag=u'', intersiteBumTrafficAllow=u'no', ownerKey=u'', name=u'BD2', epClear=u'no', unkMacUcastAct=u'proxy', arpFlood=u'no', intersiteL2Stretch=u'no', OptimizeWanBandwidth=u'no')
    fvRsBDToNdP2 = cobra.model.fv.RsBDToNdP(fvBD2, tnNdIfPolName=u'')
    fvRsBdToEpRet2 = cobra.model.fv.RsBdToEpRet(fvBD2, resolveAct=u'resolve', tnFvEpRetPolName=u'')
    fvRsCtx2 = cobra.model.fv.RsCtx(fvBD2, tnFvCtxName=u'internalVRF')
    fvRsIgmpsn2 = cobra.model.fv.RsIgmpsn(fvBD2, tnIgmpSnoopPolName=u'')

    #BD: BD3
    fvBD3 = cobra.model.fv.BD(fvTenant, multiDstPktAct=u'bd-flood', mcastAllow=u'no', limitIpLearnToSubnets=u'yes', unicastRoute=u'yes', unkMcastAct=u'flood', descr=u'', llAddr=u'::', nameAlias=u'', type=u'regular', ipLearning=u'yes', vmac=u'not-applicable', mac=u'00:22:BD:F8:19:FF', epMoveDetectMode=u'', ownerTag=u'', intersiteBumTrafficAllow=u'no', ownerKey=u'', name=u'BD3', epClear=u'no', unkMacUcastAct=u'proxy', arpFlood=u'no', intersiteL2Stretch=u'no', OptimizeWanBandwidth=u'no')
    fvRsBDToNdP3 = cobra.model.fv.RsBDToNdP(fvBD3, tnNdIfPolName=u'')
    fvRsBdToEpRet3 = cobra.model.fv.RsBdToEpRet(fvBD3, resolveAct=u'resolve', tnFvEpRetPolName=u'')
    fvRsCtx3 = cobra.model.fv.RsCtx(fvBD3, tnFvCtxName=u'internalVRF')
    fvRsIgmpsn3 = cobra.model.fv.RsIgmpsn(fvBD3, tnIgmpSnoopPolName=u'')

    #VRF: Internal
    fvCtx = cobra.model.fv.Ctx(fvTenant, ownerKey=u'', bdEnforcedEnable=u'no', descr=u'', knwMcastAct=u'permit', pcEnfDir=u'ingress', nameAlias=u'', ownerTag=u'', pcEnfPref=u'enforced', name=u'internalVRF')
    fvRsBgpCtxPol = cobra.model.fv.RsBgpCtxPol(fvCtx, tnBgpCtxPolName=u'')
    fvRsCtxToExtRouteTagPol = cobra.model.fv.RsCtxToExtRouteTagPol(fvCtx, tnL3extRouteTagPolName=u'')
    fvRsCtxToEpRet = cobra.model.fv.RsCtxToEpRet(fvCtx, tnFvEpRetPolName=u'')
    fvRsOspfCtxPol = cobra.model.fv.RsOspfCtxPol(fvCtx, tnOspfCtxPolName=u'')
    vzAny = cobra.model.vz.Any(fvCtx, prefGrMemb=u'disabled', matchT=u'AtleastOne', name=u'', descr=u'', nameAlias=u'')
#    fvRsVrfValidationPol = cobra.model.fv.RsVrfValidationPol(fvCtx, tnL3extVrfValidationPolName=u'')

    #VRF: External
    fvCtx2 = cobra.model.fv.Ctx(fvTenant, ownerKey=u'', bdEnforcedEnable=u'no', descr=u'', knwMcastAct=u'permit', pcEnfDir=u'ingress', nameAlias=u'', ownerTag=u'', pcEnfPref=u'enforced', name=u'externalVRF')
    fvRsBgpCtxPol2 = cobra.model.fv.RsBgpCtxPol(fvCtx2, tnBgpCtxPolName=u'')
    fvRsCtxToExtRouteTagPol2 = cobra.model.fv.RsCtxToExtRouteTagPol(fvCtx2, tnL3extRouteTagPolName=u'')
    fvRsCtxToEpRet2 = cobra.model.fv.RsCtxToEpRet(fvCtx2, tnFvEpRetPolName=u'')
    fvRsOspfCtxPol2 = cobra.model.fv.RsOspfCtxPol(fvCtx2, tnOspfCtxPolName=u'')
    vzAny2 = cobra.model.vz.Any(fvCtx2, prefGrMemb=u'disabled', matchT=u'AtleastOne', name=u'', descr=u'', nameAlias=u'')
#    fvRsVrfValidationPol2 = cobra.model.fv.RsVrfValidationPol(fvCtx2, tnL3extVrfValidationPolName=u'')


    vnsSvcCont = cobra.model.vns.SvcCont(fvTenant)


    # commit the generated code to APIC
    print toXMLStr(polUni)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(polUni)
    md.commit(c)


#VLAN Range for L3Out3 is 2051-2090.    Example: l3outVlan= POD# + 2050
#TENANT NAME ACISEC-$USERID-$SESSIONID  Example: tenantName=ACISEC-mgarcias-123456

pod_l3outVlan = 2050 + pod_num
createAciSecLabTenant(md,l3outVlan="%s" % pod_l3outVlan, tenantName="%s" % tenant_name)
