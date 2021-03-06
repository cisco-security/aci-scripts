#!/usr/bin/env python

# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.aaa
import cobra.model.fv
import cobra.model.igmp
import cobra.model.l3ext
import cobra.model.ospf
import cobra.model.pol
import cobra.model.vns
import cobra.model.vz
from cobra.internal.codec.xmlcodec import toXMLStr

import sys
pod_num = int(sys.argv[1])
tenant_name = sys.argv[2]
csr_ip = sys.argv[3]

out_vlan = pod_num + 2050

lab_prefix,owner,ownersid,ownerpod = tenant_name.split("-")
tenant_login = '%s' % tenant_name
# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://198.19.254.61', '%s' % tenant_login, 'p%s' % tenant_login)


md = cobra.mit.access.MoDirectory(ls)
md.login()

# the top level object on which operations will be made
polUni = cobra.model.pol.Uni('')

# build the request using cobra syntax
fvTenant = cobra.model.fv.Tenant(polUni, ownerKey='', name='%s' % tenant_name, descr='', nameAlias='', ownerTag='')
vzFilter = cobra.model.vz.Filter(fvTenant, ownerKey='', ownerTag='', name='udp_5001', descr='', nameAlias='')
vzEntry = cobra.model.vz.Entry(vzFilter, tcpRules='', arpOpc='unspecified', applyToFrag='no', dToPort='5001', descr='', nameAlias='', matchDscp='unspecified', prot='udp', icmpv4T='unspecified', sFromPort='unspecified', stateful='no', icmpv6T='unspecified', sToPort='unspecified', etherT='ip', dFromPort='5001', name='udp_5001')
vzFilter2 = cobra.model.vz.Filter(fvTenant, ownerKey='', ownerTag='', name='ssh', descr='', nameAlias='')
vzEntry2 = cobra.model.vz.Entry(vzFilter2, tcpRules='', arpOpc='unspecified', applyToFrag='no', dToPort='22', descr='', nameAlias='', matchDscp='unspecified', prot='tcp', icmpv4T='unspecified', sFromPort='unspecified', stateful='no', icmpv6T='unspecified', sToPort='unspecified', etherT='ip', dFromPort='22', name='ssh')
vzFilter3 = cobra.model.vz.Filter(fvTenant, ownerKey='', ownerTag='', name='http', descr='', nameAlias='')
vzEntry3 = cobra.model.vz.Entry(vzFilter3, tcpRules='', arpOpc='unspecified', applyToFrag='no', dToPort='http', descr='', nameAlias='', matchDscp='unspecified', prot='tcp', icmpv4T='unspecified', sFromPort='unspecified', stateful='no', icmpv6T='unspecified', sToPort='unspecified', etherT='ip', dFromPort='http', name='http')
vzBrCP = cobra.model.vz.BrCP(fvTenant, ownerKey='', name='app-to-db', prio='unspecified', targetDscp='unspecified', descr='', nameAlias='', ownerTag='')
vzSubj = cobra.model.vz.Subj(vzBrCP, revFltPorts='yes', name='fabric_only', prio='unspecified', targetDscp='unspecified', nameAlias='', descr='', consMatchT='AtleastOne', provMatchT='AtleastOne')
vzRsSubjFiltAtt = cobra.model.vz.RsSubjFiltAtt(vzSubj, directives='', tnVzFilterName='arp')
vzSubj2 = cobra.model.vz.Subj(vzBrCP, revFltPorts='yes', name='fabric_to_fw', prio='unspecified', targetDscp='unspecified', nameAlias='', descr='', consMatchT='AtleastOne', provMatchT='AtleastOne')
vzRsSubjGraphAtt = cobra.model.vz.RsSubjGraphAtt(vzSubj2, directives='', tnVnsAbsGraphName='l3-fw-ftdvha')
vzRsSubjFiltAtt2 = cobra.model.vz.RsSubjFiltAtt(vzSubj2, directives='', tnVzFilterName='ssh')
vzRsSubjFiltAtt3 = cobra.model.vz.RsSubjFiltAtt(vzSubj2, directives='', tnVzFilterName='http')
vzRsSubjFiltAtt4 = cobra.model.vz.RsSubjFiltAtt(vzSubj2, directives='', tnVzFilterName='udp_5001')
vzRsSubjFiltAtt5 = cobra.model.vz.RsSubjFiltAtt(vzSubj2, directives='', tnVzFilterName='icmp')
vzBrCP2 = cobra.model.vz.BrCP(fvTenant, ownerKey='', name='web-to-app', prio='unspecified', targetDscp='unspecified', descr='', nameAlias='', ownerTag='')
vzSubj3 = cobra.model.vz.Subj(vzBrCP2, revFltPorts='yes', name='fabric_only', prio='unspecified', targetDscp='unspecified', nameAlias='', descr='', consMatchT='AtleastOne', provMatchT='AtleastOne')
vzRsSubjFiltAtt6 = cobra.model.vz.RsSubjFiltAtt(vzSubj3, directives='', tnVzFilterName='arp')
vzSubj4 = cobra.model.vz.Subj(vzBrCP2, revFltPorts='yes', name='fabric_to_fw', prio='unspecified', targetDscp='unspecified', nameAlias='', descr='', consMatchT='AtleastOne', provMatchT='AtleastOne')
vzRsSubjGraphAtt2 = cobra.model.vz.RsSubjGraphAtt(vzSubj4, directives='', tnVnsAbsGraphName='l3-fw-ftdvha')
vzRsSubjFiltAtt7 = cobra.model.vz.RsSubjFiltAtt(vzSubj4, directives='', tnVzFilterName='ssh')
vzRsSubjFiltAtt8 = cobra.model.vz.RsSubjFiltAtt(vzSubj4, directives='', tnVzFilterName='icmp')
vzRsSubjFiltAtt9 = cobra.model.vz.RsSubjFiltAtt(vzSubj4, directives='', tnVzFilterName='http')
vzRsSubjFiltAtt10 = cobra.model.vz.RsSubjFiltAtt(vzSubj4, directives='', tnVzFilterName='udp_5001')
vzBrCP3 = cobra.model.vz.BrCP(fvTenant, ownerKey='', name='out-to-web', prio='unspecified', targetDscp='unspecified', descr='', nameAlias='', ownerTag='')
vzSubj5 = cobra.model.vz.Subj(vzBrCP3, revFltPorts='yes', name='fabric_to_fw', prio='unspecified', targetDscp='unspecified', nameAlias='', descr='', consMatchT='AtleastOne', provMatchT='AtleastOne')
vzRsSubjGraphAtt3 = cobra.model.vz.RsSubjGraphAtt(vzSubj5, directives='', tnVnsAbsGraphName='l3-fw-ftdvha')
vzRsSubjFiltAtt11 = cobra.model.vz.RsSubjFiltAtt(vzSubj5, directives='', tnVzFilterName='udp_5001')
vzRsSubjFiltAtt12 = cobra.model.vz.RsSubjFiltAtt(vzSubj5, directives='', tnVzFilterName='ssh')
vzRsSubjFiltAtt13 = cobra.model.vz.RsSubjFiltAtt(vzSubj5, directives='', tnVzFilterName='http')
vzRsSubjFiltAtt14 = cobra.model.vz.RsSubjFiltAtt(vzSubj5, directives='', tnVzFilterName='icmp')
vzSubj6 = cobra.model.vz.Subj(vzBrCP3, revFltPorts='yes', name='fabric_only', prio='unspecified', targetDscp='unspecified', nameAlias='', descr='', consMatchT='AtleastOne', provMatchT='AtleastOne')
vzRsSubjFiltAtt15 = cobra.model.vz.RsSubjFiltAtt(vzSubj6, directives='', tnVzFilterName='arp')
vnsLDevVip = cobra.model.vns.LDevVip(fvTenant, isCopy='no', managed='yes', name='vFTD-l3fw', svcType='FW', funcType='GoTo', promMode='no', devtype='VIRTUAL', packageModel='VIRTUAL', contextAware='single-Context', nameAlias='', trunking='no', mode='legacy-Mode')
vnsLIf = cobra.model.vns.LIf(vnsLDevVip, name='prov-nic', encap='unknown', nameAlias='')
vnsRsMetaIf = cobra.model.vns.RsMetaIf(vnsLIf, isConAndProv='no', tDn='uni/infra/mDev-CISCO-FTD_FI-1.0/mIfLbl-internal')
vnsRsCIfAttN = cobra.model.vns.RsCIfAttN(vnsLIf, tDn='uni/tn-%s/lDevVip-vFTD-l3fw/cDev-Device1/cIf-[GigabitEthernet0/1]' % tenant_name)
vnsRsCIfAttN2 = cobra.model.vns.RsCIfAttN(vnsLIf, tDn='uni/tn-%s/lDevVip-vFTD-l3fw/cDev-Device2/cIf-[GigabitEthernet0/1]' % tenant_name)
vnsLIf2 = cobra.model.vns.LIf(vnsLDevVip, name='cons-nic', encap='unknown', nameAlias='')
vnsRsMetaIf2 = cobra.model.vns.RsMetaIf(vnsLIf2, isConAndProv='no', tDn='uni/infra/mDev-CISCO-FTD_FI-1.0/mIfLbl-external')
vnsRsCIfAttN3 = cobra.model.vns.RsCIfAttN(vnsLIf2, tDn='uni/tn-%s/lDevVip-vFTD-l3fw/cDev-Device1/cIf-[GigabitEthernet0/1]' % tenant_name)
vnsRsCIfAttN4 = cobra.model.vns.RsCIfAttN(vnsLIf2, tDn='uni/tn-%s/lDevVip-vFTD-l3fw/cDev-Device2/cIf-[GigabitEthernet0/1]' % tenant_name)
vnsRsALDevToDomP = cobra.model.vns.RsALDevToDomP(vnsLDevVip, tDn='uni/vmmp-VMware/dom-vmware60-hybridcloud')
vnsCMgmt = cobra.model.vns.CMgmt(vnsLDevVip, host='10.0.0.30', name='', nameAlias='', port='443')
vnsRsALDevToDevMgr = cobra.model.vns.RsALDevToDevMgr(vnsLDevVip, tnVnsDevMgrName='fmc63')
vnsCDev = cobra.model.vns.CDev(vnsLDevVip, vcenterName='vc60-aci-1', vmName='acisec-vftd2-%s-%d' % (ownersid,pod_num), name='Device2', nameAlias='', devCtxLbl='')
vnsCMgmt2 = cobra.model.vns.CMgmt(vnsCDev, host='10.0.0.52', name='', nameAlias='', port='443')
vnsCIf = cobra.model.vns.CIf(vnsCDev, name='GigabitEthernet0/1', nameAlias='', vnicName='Network adapter 3')
vnsCCredSecret = cobra.model.vns.CCredSecret(vnsCDev, value='cisco', name='password', nameAlias='')
vnsCCred = cobra.model.vns.CCred(vnsCDev, value='apiuser', name='username', nameAlias='')
vnsCDev2 = cobra.model.vns.CDev(vnsLDevVip, vcenterName='vc60-aci-1', vmName='acisec-vftd1-%s-%d' % (ownersid,pod_num), name='Device1', nameAlias='', devCtxLbl='')
vnsCMgmt3 = cobra.model.vns.CMgmt(vnsCDev2, host='10.0.0.51', name='', nameAlias='', port='443')
vnsCIf2 = cobra.model.vns.CIf(vnsCDev2, name='GigabitEthernet0/1', nameAlias='', vnicName='Network adapter 3')
vnsCCredSecret2 = cobra.model.vns.CCredSecret(vnsCDev2, value='cisco', name='password', nameAlias='')
vnsCCred2 = cobra.model.vns.CCred(vnsCDev2, value='apiuser', name='username', nameAlias='')
vnsCCredSecret3 = cobra.model.vns.CCredSecret(vnsLDevVip, value='cisco', name='password', nameAlias='')
vnsRsMDevAtt = cobra.model.vns.RsMDevAtt(vnsLDevVip, tDn='uni/infra/mDev-CISCO-FTD_FI-1.0')
vnsCCred3 = cobra.model.vns.CCred(vnsLDevVip, value='apiuser', name='username', nameAlias='')
aaaDomainRef = cobra.model.aaa.DomainRef(fvTenant, ownerKey='', ownerTag='', name='ACI-Security-Integration', descr='', nameAlias='')
aaaDomainRef2 = cobra.model.aaa.DomainRef(fvTenant, ownerKey='', ownerTag='', name='SecDo-%s' % tenant_name, descr='', nameAlias='')
fvAp = cobra.model.fv.Ap(fvTenant, ownerKey='', name='aProf', prio='unspecified', descr='', nameAlias='', ownerTag='')
fvAEPg = cobra.model.fv.AEPg(fvAp, isAttrBasedEPg='no', matchT='AtleastOne', name='app', descr='', fwdCtrl='', prefGrMemb='exclude', floodOnEncap='disabled', nameAlias='', prio='unspecified', pcEnfPref='unenforced')
fvRsProv = cobra.model.fv.RsProv(fvAEPg, tnVzBrCPName='web-to-app', matchT='AtleastOne', prio='unspecified')
fvRsDomAtt = cobra.model.fv.RsDomAtt(fvAEPg, tDn='uni/vmmp-VMware/dom-vmware60-hybridcloud', netflowDir='both', epgCos='Cos0', classPref='useg', primaryEncap='unknown', secondaryEncapInner='unknown', resImedcy='immediate', delimiter='', instrImedcy='immediate', primaryEncapInner='unknown', encap='unknown', switchingMode='native', encapMode='auto', netflowPref='disabled', epgCosPref='disabled')
fvRsCons = cobra.model.fv.RsCons(fvAEPg, tnVzBrCPName='app-to-db', prio='unspecified')
fvRsCustQosPol = cobra.model.fv.RsCustQosPol(fvAEPg, tnQosCustomPolName='')
fvRsBd = cobra.model.fv.RsBd(fvAEPg, tnFvBDName='BD1')
fvAEPg2 = cobra.model.fv.AEPg(fvAp, isAttrBasedEPg='no', matchT='AtleastOne', name='failover', descr='', fwdCtrl='', prefGrMemb='exclude', floodOnEncap='disabled', nameAlias='', prio='unspecified', pcEnfPref='unenforced')
fvRsDomAtt2 = cobra.model.fv.RsDomAtt(fvAEPg2, tDn='uni/vmmp-VMware/dom-vmware60-hybridcloud', netflowDir='both', epgCos='Cos0', classPref='encap', primaryEncap='unknown', secondaryEncapInner='unknown', resImedcy='lazy', delimiter='', instrImedcy='lazy', primaryEncapInner='unknown', encap='unknown', switchingMode='native', encapMode='auto', netflowPref='disabled', epgCosPref='disabled')
fvRsCustQosPol2 = cobra.model.fv.RsCustQosPol(fvAEPg2, tnQosCustomPolName='')
fvRsBd2 = cobra.model.fv.RsBd(fvAEPg2, tnFvBDName='failover-BD')
fvAEPg3 = cobra.model.fv.AEPg(fvAp, isAttrBasedEPg='no', matchT='AtleastOne', name='web', descr='', fwdCtrl='', prefGrMemb='exclude', floodOnEncap='disabled', nameAlias='', prio='unspecified', pcEnfPref='unenforced')
fvRsProv2 = cobra.model.fv.RsProv(fvAEPg3, tnVzBrCPName='out-to-web', matchT='AtleastOne', prio='unspecified')
fvRsDomAtt3 = cobra.model.fv.RsDomAtt(fvAEPg3, tDn='uni/vmmp-VMware/dom-vmware60-hybridcloud', netflowDir='both', epgCos='Cos0', classPref='encap', primaryEncap='unknown', secondaryEncapInner='unknown', resImedcy='lazy', delimiter='', instrImedcy='lazy', primaryEncapInner='unknown', encap='unknown', switchingMode='native', encapMode='auto', netflowPref='disabled', epgCosPref='disabled')
fvRsCons2 = cobra.model.fv.RsCons(fvAEPg3, tnVzBrCPName='web-to-app', prio='unspecified')
fvRsCustQosPol3 = cobra.model.fv.RsCustQosPol(fvAEPg3, tnQosCustomPolName='')
fvRsBd3 = cobra.model.fv.RsBd(fvAEPg3, tnFvBDName='BD1')
fvAEPg4 = cobra.model.fv.AEPg(fvAp, isAttrBasedEPg='no', matchT='AtleastOne', name='db', descr='', fwdCtrl='', prefGrMemb='exclude', floodOnEncap='disabled', nameAlias='', prio='unspecified', pcEnfPref='unenforced')
fvRsProv3 = cobra.model.fv.RsProv(fvAEPg4, tnVzBrCPName='app-to-db', matchT='AtleastOne', prio='unspecified')
fvRsDomAtt4 = cobra.model.fv.RsDomAtt(fvAEPg4, tDn='uni/vmmp-VMware/dom-vmware60-hybridcloud', netflowDir='both', epgCos='Cos0', classPref='encap', primaryEncap='unknown', secondaryEncapInner='unknown', resImedcy='lazy', delimiter='', instrImedcy='lazy', primaryEncapInner='unknown', encap='unknown', switchingMode='native', encapMode='auto', netflowPref='disabled', epgCosPref='disabled')
fvRsCustQosPol4 = cobra.model.fv.RsCustQosPol(fvAEPg4, tnQosCustomPolName='')
fvRsBd4 = cobra.model.fv.RsBd(fvAEPg4, tnFvBDName='BD1')
fvRsTenantMonPol = cobra.model.fv.RsTenantMonPol(fvTenant, tnMonEPGPolName='')
vnsAbsFuncProfContr = cobra.model.vns.AbsFuncProfContr(fvTenant, ownerKey='', ownerTag='', name='', descr='', nameAlias='')
vnsAbsFuncProfGrp = cobra.model.vns.AbsFuncProfGrp(vnsAbsFuncProfContr, ownerKey='', ownerTag='', name='ftd-group', descr='', nameAlias='')
vnsAbsFuncProf = cobra.model.vns.AbsFuncProf(vnsAbsFuncProfGrp, ownerKey='', name='ftdv-onearm', descr='', srcMode='', nameAlias='', ownerTag='')
vnsRsProfToMFunc = cobra.model.vns.RsProfToMFunc(vnsAbsFuncProf, tDn='uni/infra/mDev-CISCO-FTD_FI-1.0/mFunc-FTD')
vnsAbsFuncCfg = cobra.model.vns.AbsFuncCfg(vnsAbsFuncProf, ownerKey='', ownerTag='', name='funcConfig', descr='', nameAlias='')
vnsAbsFolder = cobra.model.vns.AbsFolder(vnsAbsFuncCfg, srcRef='', locked='no', name='IntConfig', devCtxLbl='', scopedBy='epg', auxInfo='', profileBehaviorShared='yes', key='InIntfConfigRelFolder', cardinality='unspecified', nameAlias='')
vnsAbsCfgRel = cobra.model.vns.AbsCfgRel(vnsAbsFolder, mandatory='no', name='InConfigrel', nameAlias='', key='InIntfConfigRel', locked='no', cardinality='unspecified', targetName='oneinterface')
vnsAbsFolder2 = cobra.model.vns.AbsFolder(vnsAbsFuncCfg, srcRef='', locked='no', name='ExtConfig', devCtxLbl='', scopedBy='epg', auxInfo='', profileBehaviorShared='yes', key='ExIntfConfigRelFolder', cardinality='unspecified', nameAlias='')
vnsAbsCfgRel2 = cobra.model.vns.AbsCfgRel(vnsAbsFolder2, mandatory='no', name='ExtConfigrel', nameAlias='', key='ExIntfConfigRel', locked='no', cardinality='unspecified', targetName='oneinterface')
vnsAbsFolder3 = cobra.model.vns.AbsFolder(vnsAbsFuncCfg, srcRef='', locked='no', name='AccessPolicyFolder', devCtxLbl='', scopedBy='epg', auxInfo='', profileBehaviorShared='yes', key='AccessPolicyFolder', cardinality='unspecified', nameAlias='')
vnsAbsCfgRel3 = cobra.model.vns.AbsCfgRel(vnsAbsFolder3, mandatory='no', name='InAccessPolicyRel', nameAlias='', key='InAccessPolicyRel', locked='no', cardinality='unspecified', targetName='ftd-policy')
vnsAbsDevCfg = cobra.model.vns.AbsDevCfg(vnsAbsFuncProf, ownerKey='', ownerTag='', name='devConfig', descr='', nameAlias='')
vnsAbsFolder4 = cobra.model.vns.AbsFolder(vnsAbsDevCfg, srcRef='', locked='no', name='oneinterface', devCtxLbl='', scopedBy='epg', auxInfo='', profileBehaviorShared='yes', key='InterfaceConfig', cardinality='unspecified', nameAlias='')
vnsAbsParam = cobra.model.vns.AbsParam(vnsAbsFolder4, validation='', mandatory='no', name='enabled', nameAlias='', srcRef='', auxInfo='', value='true', key='enabled', locked='no', cardinality='unspecified')
vnsAbsParam2 = cobra.model.vns.AbsParam(vnsAbsFolder4, validation='', mandatory='no', name='activeMACAddress', nameAlias='', srcRef='', auxInfo='', value='0050.5611.1111', key='activeMACAddress', locked='no', cardinality='unspecified')
vnsAbsParam3 = cobra.model.vns.AbsParam(vnsAbsFolder4, validation='', mandatory='no', name='ifname', nameAlias='', srcRef='', auxInfo='', value='Consumer', key='ifname', locked='no', cardinality='unspecified')
vnsAbsFolder5 = cobra.model.vns.AbsFolder(vnsAbsFolder4, srcRef='', locked='no', name='StaticRoute', devCtxLbl='', scopedBy='epg', auxInfo='', profileBehaviorShared='no', key='StaticRoute', cardinality='unspecified', nameAlias='')
vnsAbsFolder6 = cobra.model.vns.AbsFolder(vnsAbsFolder5, srcRef='', locked='no', name='IPv4StaticRoute', devCtxLbl='', scopedBy='epg', auxInfo='', profileBehaviorShared='no', key='IPv4StaticRoute', cardinality='unspecified', nameAlias='')
vnsAbsParam4 = cobra.model.vns.AbsParam(vnsAbsFolder6, validation='', mandatory='no', name='isTunneled', nameAlias='', srcRef='', auxInfo='', value='false', key='isTunneled', locked='no', cardinality='unspecified')
vnsAbsParam5 = cobra.model.vns.AbsParam(vnsAbsFolder6, validation='', mandatory='yes', name='network', nameAlias='', srcRef='', auxInfo='', value='0.0.0.0/0.0.0.0', key='network', locked='no', cardinality='unspecified')
vnsAbsParam6 = cobra.model.vns.AbsParam(vnsAbsFolder6, validation='', mandatory='no', name='metric', nameAlias='', srcRef='', auxInfo='', value='1', key='metric', locked='no', cardinality='unspecified')
vnsAbsParam7 = cobra.model.vns.AbsParam(vnsAbsFolder6, validation='', mandatory='yes', name='gateway', nameAlias='', srcRef='', auxInfo='', value='10.1.0.2', key='gateway', locked='no', cardinality='unspecified')
vnsAbsFolder7 = cobra.model.vns.AbsFolder(vnsAbsFolder4, srcRef='', locked='no', name='IPv4Config', devCtxLbl='', scopedBy='epg', auxInfo='', profileBehaviorShared='no', key='IPv4Config', cardinality='unspecified', nameAlias='')
vnsAbsFolder8 = cobra.model.vns.AbsFolder(vnsAbsFolder7, srcRef='', locked='no', name='static', devCtxLbl='', scopedBy='epg', auxInfo='', profileBehaviorShared='no', key='static', cardinality='unspecified', nameAlias='')
vnsAbsParam8 = cobra.model.vns.AbsParam(vnsAbsFolder8, validation='', mandatory='yes', name='address', nameAlias='', srcRef='', auxInfo='', value='10.1.0.1/16', key='address', locked='no', cardinality='unspecified')
vnsAbsFolder9 = cobra.model.vns.AbsFolder(vnsAbsFolder4, srcRef='', locked='no', name='int_security_zone', devCtxLbl='', scopedBy='epg', auxInfo='', profileBehaviorShared='no', key='int_security_zone', cardinality='unspecified', nameAlias='')
vnsAbsCfgRel4 = cobra.model.vns.AbsCfgRel(vnsAbsFolder9, mandatory='no', name='security_zone', nameAlias='', key='security_zone', locked='no', cardinality='unspecified', targetName='fw-zone')
vnsAbsFolder10 = cobra.model.vns.AbsFolder(vnsAbsDevCfg, srcRef='', locked='no', name='ftd-policy', devCtxLbl='', scopedBy='epg', auxInfo='', profileBehaviorShared='yes', key='AccessPolicy', cardinality='unspecified', nameAlias='')
vnsAbsFolder11 = cobra.model.vns.AbsFolder(vnsAbsFolder10, srcRef='', locked='no', name='ftd-rule1', devCtxLbl='', scopedBy='epg', auxInfo='', profileBehaviorShared='no', key='AccessRule', cardinality='unspecified', nameAlias='')
vnsAbsParam9 = cobra.model.vns.AbsParam(vnsAbsFolder11, validation='', mandatory='no', name='Bi-Directional', nameAlias='', srcRef='', auxInfo='', value='true', key='bidirectional', locked='no', cardinality='unspecified')
vnsAbsFolder12 = cobra.model.vns.AbsFolder(vnsAbsFolder11, srcRef='', locked='no', name='AccSourceZones', devCtxLbl='', scopedBy='epg', auxInfo='', profileBehaviorShared='no', key='AccSourceZones', cardinality='unspecified', nameAlias='')
vnsAbsCfgRel5 = cobra.model.vns.AbsCfgRel(vnsAbsFolder12, mandatory='no', name='SourceZone', nameAlias='', key='SourceZones', locked='no', cardinality='unspecified', targetName='oneinterface/int_security_zone')
vnsAbsFolder13 = cobra.model.vns.AbsFolder(vnsAbsFolder11, srcRef='', locked='no', name='AccDestinationZones', devCtxLbl='', scopedBy='epg', auxInfo='', profileBehaviorShared='no', key='AccDestinationZones', cardinality='unspecified', nameAlias='')
vnsAbsCfgRel6 = cobra.model.vns.AbsCfgRel(vnsAbsFolder13, mandatory='no', name='DestinationZone', nameAlias='', key='DestinationZones', locked='no', cardinality='unspecified', targetName='oneinterface/int_security_zone')
vnsAbsFolder14 = cobra.model.vns.AbsFolder(vnsAbsDevCfg, srcRef='', locked='no', name='fw-zone', devCtxLbl='', scopedBy='epg', auxInfo='', profileBehaviorShared='yes', key='SecurityZone', cardinality='unspecified', nameAlias='')
vnsAbsParam10 = cobra.model.vns.AbsParam(vnsAbsFolder14, validation='', mandatory='no', name='type', nameAlias='', srcRef='', auxInfo='', value='ROUTED', key='type', locked='no', cardinality='unspecified')
fvCtx = cobra.model.fv.Ctx(fvTenant, ownerKey='', bdEnforcedEnable='no', descr='', knwMcastAct='permit', pcEnfDir='ingress', nameAlias='', ownerTag='', pcEnfPref='enforced', name='internalVRF')
fvRsVrfValidationPol = cobra.model.fv.RsVrfValidationPol(fvCtx, tnL3extVrfValidationPolName='')
vzAny = cobra.model.vz.Any(fvCtx, prefGrMemb='disabled', matchT='AtleastOne', name='', descr='', nameAlias='')
fvRsOspfCtxPol = cobra.model.fv.RsOspfCtxPol(fvCtx, tnOspfCtxPolName='')
fvRsCtxToEpRet = cobra.model.fv.RsCtxToEpRet(fvCtx, tnFvEpRetPolName='')
fvRsCtxToExtRouteTagPol = cobra.model.fv.RsCtxToExtRouteTagPol(fvCtx, tnL3extRouteTagPolName='')
fvRsBgpCtxPol = cobra.model.fv.RsBgpCtxPol(fvCtx, tnBgpCtxPolName='')
l3extOut = cobra.model.l3ext.Out(fvTenant, ownerKey='', name='outside-L3Out3', descr='', targetDscp='unspecified', enforceRtctrl='export', nameAlias='', ownerTag='')
ospfExtP = cobra.model.ospf.ExtP(l3extOut, areaCtrl='redistribute,summary', areaId='0.0.0.2', areaType='regular', descr='', multipodInternal='no', nameAlias='', areaCost='1')
l3extRsL3DomAtt = cobra.model.l3ext.RsL3DomAtt(l3extOut, tDn='uni/l3dom-ACI-Sec-Lab-L3Out3')
l3extRsEctx = cobra.model.l3ext.RsEctx(l3extOut, tnFvCtxName='internalVRF')
l3extLNodeP = cobra.model.l3ext.LNodeP(l3extOut, ownerKey='', name='leafnp', descr='', targetDscp='unspecified', tag='yellow-green', nameAlias='', ownerTag='')
l3extRsNodeL3OutAtt = cobra.model.l3ext.RsNodeL3OutAtt(l3extLNodeP, rtrIdLoopBack='no', rtrId='102.0.0.1', tDn='topology/pod-1/node-102')
l3extLIfP = cobra.model.l3ext.LIfP(l3extLNodeP, ownerKey='', name='leafip', descr='', tag='yellow-green', nameAlias='', ownerTag='')
ospfIfP = cobra.model.ospf.IfP(l3extLIfP, authKeyId='1', authType='none', name='', descr='', nameAlias='')
ospfRsIfPol = cobra.model.ospf.RsIfPol(ospfIfP, tnOspfIfPolName='')
l3extRsPathL3OutAtt = cobra.model.l3ext.RsPathL3OutAtt(l3extLIfP, addr='10.60.0.1/24', descr='', encapScope='local', targetDscp='unspecified', llAddr='::', autostate='disabled', mac='00:22:BD:F8:19:FF', mode='regular', encap='vlan-%s' % out_vlan, ifInstT='ext-svi', mtu='1500', tDn='topology/pod-1/paths-102/pathep-[eth1/46]')
l3extRsNdIfPol = cobra.model.l3ext.RsNdIfPol(l3extLIfP, tnNdIfPolName='')
l3extRsIngressQosDppPol = cobra.model.l3ext.RsIngressQosDppPol(l3extLIfP, tnQosDppPolName='')
l3extRsEgressQosDppPol = cobra.model.l3ext.RsEgressQosDppPol(l3extLIfP, tnQosDppPolName='')
l3extInstP = cobra.model.l3ext.InstP(l3extOut, matchT='AtleastOne', name='out-l3out3', descr='', targetDscp='unspecified', prefGrMemb='exclude', floodOnEncap='disabled', nameAlias='', prio='unspecified')
l3extSubnet = cobra.model.l3ext.Subnet(l3extInstP, name='', descr='', ip='10.70.0.0/24', nameAlias='', aggregate='')
fvRsCustQosPol5 = cobra.model.fv.RsCustQosPol(l3extInstP, tnQosCustomPolName='')
fvRsCons3 = cobra.model.fv.RsCons(l3extInstP, tnVzBrCPName='out-to-web', prio='unspecified')
fvBD = cobra.model.fv.BD(fvTenant, multiDstPktAct='bd-flood', mcastAllow='no', limitIpLearnToSubnets='yes', unicastRoute='yes', unkMcastAct='flood', descr='', llAddr='::', nameAlias='', type='regular', ipLearning='yes', vmac='not-applicable', mac='00:22:BD:F8:19:FF', epMoveDetectMode='', ownerTag='', intersiteBumTrafficAllow='no', ownerKey='', name='BD1', epClear='no', unkMacUcastAct='proxy', arpFlood='no', intersiteL2Stretch='no', OptimizeWanBandwidth='no')
fvSubnet = cobra.model.fv.Subnet(fvBD, name='', descr='', ctrl='', ip='10.2.0.1/24', preferred='no', virtual='no', nameAlias='', scope='public')
fvSubnet2 = cobra.model.fv.Subnet(fvBD, name='', descr='', ctrl='', ip='10.1.0.2/16', preferred='no', virtual='no', nameAlias='', scope='public')
fvRsIgmpsn = cobra.model.fv.RsIgmpsn(fvBD, tnIgmpSnoopPolName='')
fvRsCtx = cobra.model.fv.RsCtx(fvBD, tnFvCtxName='internalVRF')
fvRsBdToEpRet = cobra.model.fv.RsBdToEpRet(fvBD, resolveAct='resolve', tnFvEpRetPolName='')
fvRsBDToOut = cobra.model.fv.RsBDToOut(fvBD, tnL3extOutName='outside-L3Out3')
fvRsBDToNdP = cobra.model.fv.RsBDToNdP(fvBD, tnNdIfPolName='')
fvBD2 = cobra.model.fv.BD(fvTenant, multiDstPktAct='bd-flood', mcastAllow='no', limitIpLearnToSubnets='yes', unicastRoute='yes', unkMcastAct='flood', descr='', llAddr='::', nameAlias='', type='regular', ipLearning='yes', vmac='not-applicable', mac='00:22:BD:F8:19:FF', epMoveDetectMode='', ownerTag='', intersiteBumTrafficAllow='no', ownerKey='', name='failover-BD', epClear='no', unkMacUcastAct='flood', arpFlood='yes', intersiteL2Stretch='no', OptimizeWanBandwidth='no')
igmpIfP = cobra.model.igmp.IfP(fvBD2, name='', descr='', nameAlias='')
fvRsIgmpsn2 = cobra.model.fv.RsIgmpsn(fvBD2, tnIgmpSnoopPolName='')
fvRsCtx2 = cobra.model.fv.RsCtx(fvBD2, tnFvCtxName='internalVRF')
fvRsBdToEpRet2 = cobra.model.fv.RsBdToEpRet(fvBD2, resolveAct='resolve', tnFvEpRetPolName='')
fvRsBDToNdP2 = cobra.model.fv.RsBDToNdP(fvBD2, tnNdIfPolName='')
vnsAbsGraph = cobra.model.vns.AbsGraph(fvTenant, ownerKey='', name='l3-fw-ftdvha', descr='', nameAlias='', ownerTag='', uiTemplateType='UNSPECIFIED')
vnsAbsTermNodeProv = cobra.model.vns.AbsTermNodeProv(vnsAbsGraph, ownerKey='', ownerTag='', name='T2', descr='', nameAlias='')
vnsOutTerm = cobra.model.vns.OutTerm(vnsAbsTermNodeProv, name='', descr='', nameAlias='')
vnsInTerm = cobra.model.vns.InTerm(vnsAbsTermNodeProv, name='', descr='', nameAlias='')
vnsAbsTermConn = cobra.model.vns.AbsTermConn(vnsAbsTermNodeProv, ownerKey='', attNotify='no', name='1', descr='', nameAlias='', ownerTag='')
vnsAbsTermNodeCon = cobra.model.vns.AbsTermNodeCon(vnsAbsGraph, ownerKey='', ownerTag='', name='T1', descr='', nameAlias='')
vnsOutTerm2 = cobra.model.vns.OutTerm(vnsAbsTermNodeCon, name='', descr='', nameAlias='')
vnsInTerm2 = cobra.model.vns.InTerm(vnsAbsTermNodeCon, name='', descr='', nameAlias='')
vnsAbsTermConn2 = cobra.model.vns.AbsTermConn(vnsAbsTermNodeCon, ownerKey='', attNotify='no', name='1', descr='', nameAlias='', ownerTag='')
vnsAbsNode = cobra.model.vns.AbsNode(vnsAbsGraph, funcTemplateType='FW_ROUTED', isCopy='no', ownerKey='', managed='yes', name='N1', descr='', funcType='GoTo', shareEncap='no', sequenceNumber='0', routingMode='Redirect', nameAlias='', ownerTag='')
vnsRsNodeToMFunc = cobra.model.vns.RsNodeToMFunc(vnsAbsNode, tDn='uni/infra/mDev-CISCO-FTD_FI-1.0/mFunc-FTD')
vnsRsNodeToLDev = cobra.model.vns.RsNodeToLDev(vnsAbsNode, tDn='uni/tn-%s/lDevVip-vFTD-l3fw' % tenant_name)
vnsRsNodeToAbsFuncProf = cobra.model.vns.RsNodeToAbsFuncProf(vnsAbsNode, tDn='uni/tn-%s/absFuncProfContr/absFuncProfGrp-ftd-group/absFuncProf-ftdv-onearm' % tenant_name)
vnsAbsFuncConn = cobra.model.vns.AbsFuncConn(vnsAbsNode, ownerKey='', attNotify='no', name='consumer', descr='', nameAlias='', ownerTag='')
vnsRsMConnAtt = cobra.model.vns.RsMConnAtt(vnsAbsFuncConn, tDn='uni/infra/mDev-CISCO-FTD_FI-1.0/mFunc-FTD/mConn-external')
vnsAbsFuncConn2 = cobra.model.vns.AbsFuncConn(vnsAbsNode, ownerKey='', attNotify='no', name='provider', descr='', nameAlias='', ownerTag='')
vnsRsMConnAtt2 = cobra.model.vns.RsMConnAtt(vnsAbsFuncConn2, tDn='uni/infra/mDev-CISCO-FTD_FI-1.0/mFunc-FTD/mConn-internal')
vnsAbsConnection = cobra.model.vns.AbsConnection(vnsAbsGraph, adjType='L3', ownerKey='', name='C2', descr='', connDir='provider', connType='external', nameAlias='', ownerTag='', directConnect='no', unicastRoute='yes')
vnsRsAbsConnectionConns = cobra.model.vns.RsAbsConnectionConns(vnsAbsConnection, tDn='uni/tn-%s/AbsGraph-l3-fw-ftdvha/AbsNode-N1/AbsFConn-provider' % tenant_name)
vnsRsAbsConnectionConns2 = cobra.model.vns.RsAbsConnectionConns(vnsAbsConnection, tDn='uni/tn-%s/AbsGraph-l3-fw-ftdvha/AbsTermNodeProv-T2/AbsTConn' % tenant_name)
vnsAbsConnection2 = cobra.model.vns.AbsConnection(vnsAbsGraph, adjType='L3', ownerKey='', name='C1', descr='', connDir='provider', connType='external', nameAlias='', ownerTag='', directConnect='no', unicastRoute='yes')
vnsRsAbsConnectionConns3 = cobra.model.vns.RsAbsConnectionConns(vnsAbsConnection2, tDn='uni/tn-%s/AbsGraph-l3-fw-ftdvha/AbsTermNodeCon-T1/AbsTConn' % tenant_name)
vnsRsAbsConnectionConns4 = cobra.model.vns.RsAbsConnectionConns(vnsAbsConnection2, tDn='uni/tn-%s/AbsGraph-l3-fw-ftdvha/AbsNode-N1/AbsFConn-consumer' % tenant_name)
vnsDevMgr = cobra.model.vns.DevMgr(fvTenant, ownerKey='', ownerTag='', name='fmc63', descr='', nameAlias='')
vnsRsDevMgrToMDevMgr = cobra.model.vns.RsDevMgrToMDevMgr(vnsDevMgr, tDn='uni/infra/mDevMgr-CISCO-FTDmgr_FI-1.0')
vnsCMgmts = cobra.model.vns.CMgmts(vnsDevMgr, host='%s' % csr_ip, name='', nameAlias='', port='44330')
vnsCCredSecret4 = cobra.model.vns.CCredSecret(vnsDevMgr, value='cisco', name='password', nameAlias='')
vnsCCred4 = cobra.model.vns.CCred(vnsDevMgr, value='apiuser', name='username', nameAlias='')
vnsSvcCont = cobra.model.vns.SvcCont(fvTenant)
vnsSvcRedirectPol = cobra.model.vns.SvcRedirectPol(vnsSvcCont, maxThresholdPercent='0', ownerKey='', thresholdEnable='no', thresholdDownAction='permit', name='pbr', descr='', ownerTag='', nameAlias='', hashingAlgorithm='sip-dip-prototype', programLocalPodOnly='no', minThresholdPercent='0')
vnsRedirectDest = cobra.model.vns.RedirectDest(vnsSvcRedirectPol, name='', descr='', podId='1', ip='10.1.0.1', ip2='0.0.0.0', mac='00:50:56:11:11:11', nameAlias='')
vnsLDevCtx = cobra.model.vns.LDevCtx(fvTenant, context='', name='', descr='', ctrctNameOrLbl='any', nameAlias='', nodeNameOrLbl='N1', graphNameOrLbl='l3-fw-ftdvha')
vnsRsLDevCtxToLDev = cobra.model.vns.RsLDevCtxToLDev(vnsLDevCtx, tDn='uni/tn-%s/lDevVip-vFTD-l3fw' % tenant_name)
vnsLIfCtx = cobra.model.vns.LIfCtx(vnsLDevCtx, permitLog='no', nameAlias='', name='consumer', descr='', connNameOrLbl='consumer')
vnsRsLIfCtxToSvcRedirectPol = cobra.model.vns.RsLIfCtxToSvcRedirectPol(vnsLIfCtx, tDn='uni/tn-%s/svcCont/svcRedirectPol-pbr' % tenant_name)
vnsRsLIfCtxToLIf = cobra.model.vns.RsLIfCtxToLIf(vnsLIfCtx, tDn='uni/tn-%s/lDevVip-vFTD-l3fw/lIf-cons-nic' % tenant_name)
vnsRsLIfCtxToBD = cobra.model.vns.RsLIfCtxToBD(vnsLIfCtx, tDn='uni/tn-%s/BD-BD1' % tenant_name)
vnsLIfCtx2 = cobra.model.vns.LIfCtx(vnsLDevCtx, permitLog='no', nameAlias='', name='provider', descr='', connNameOrLbl='provider')
vnsRsLIfCtxToSvcRedirectPol2 = cobra.model.vns.RsLIfCtxToSvcRedirectPol(vnsLIfCtx2, tDn='uni/tn-%s/svcCont/svcRedirectPol-pbr' % tenant_name)
vnsRsLIfCtxToLIf2 = cobra.model.vns.RsLIfCtxToLIf(vnsLIfCtx2, tDn='uni/tn-%s/lDevVip-vFTD-l3fw/lIf-prov-nic' % tenant_name)
vnsRsLIfCtxToBD2 = cobra.model.vns.RsLIfCtxToBD(vnsLIfCtx2, tDn='uni/tn-%s/BD-BD1' % tenant_name)


# commit the generated code to APIC
print toXMLStr(polUni)
c = cobra.mit.request.ConfigRequest()
c.addMo(polUni)
md.commit(c)

