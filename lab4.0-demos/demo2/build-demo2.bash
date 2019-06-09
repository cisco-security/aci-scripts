#!/bin/bash
#
# dCloud ACISEC training/demo lab
#

#dCloud session parameters
session_file="/home/aciadmin/session.xml"
session_id="$(/bin/sed -n '0,/.*<id>/s/.*<id>\(.*\)<\/id>/\1/p' $session_file)"
username="$(/bin/sed -n '0,/.*<owner>/s/.*<owner>\(.*\)<\/owner>/\1/p' $session_file)"
csr_ip="$(/bin/sed -n '0,/.*<csrIP>/s/.*<csrIP>\(.*\)<\/csrIP>/\1/p' $session_file)"
pod_num="$(/bin/sed -n '0,/.*<asaContext>/s/.*<asaContext>\(.*\)<\/asaContext>/\1/p' $session_file)"
#tenant_name=ACISEC-${username}-${session_id}-${pod_num}
tenant_name=${username}

echo -e "\nWelcome to your demo2 build-out under ACI tenant $tenant_name\n";
echo -e "Please follow these steps to orchestrate security and networking for your tenant.\n";
echo -e "- If any of these steps fail with python errors, please contact your proctor with a step that failed.";
echo -e "- Note that each step script will dump xml code being applied to your APIC tenant.";
echo -e "- To bring your tenant $tenant_name to a baseline config, you can run the following cli:";
echo -e "- Press Enter to continue and execute each step script.";

echo -e "\n1. Create tenant, app profiles, epgs, bd, vrf: [continue]"; read go
python tenant-apps.py $pod_num $tenant_name $csr_ip

echo -e "\n2. Create FMC device mgr and ftdv L4-L7 device: [continue]"; read go
python fmcv-mgr.py $pod_num $tenant_name $csr_ip
python ftdv-dev.py $pod_num $tenant_name $csr_ip $session_id

echo -e "\n3. Create ftdv L3FW function profile: [continue]"; read go
python ftdv-l3fw-fprof.py $pod_num $tenant_name $csr_ip

echo -e "\n4. Add ftdv service graph: [continue]"; read go
python ftdv-graph.py $pod_num $tenant_name $csr_ip

echo -e "\n5. Apply ftdv SG and create app-to-db contract: [continue]"; read go
python ftdv-apply-graph.py $pod_num $tenant_name $csr_ip

echo -e "\n6. Create PBR BD for ASA2 context device: [continue]"; read go
python asa2-pbr-bd.py $pod_num $tenant_name $csr_ip

echo -e "\n7. Create ASA2 PBR redirect IP/MAC info: [continue]"; read go
python asa2-pbr-redirect.py $pod_num $tenant_name $csr_ip

echo -e "\n8. Create/Register ASA2 device (context): [continue]"; read go
python asa2-pbr-dev.py $pod_num $tenant_name $csr_ip

echo -e "\n9. Create ASA2 device L3FW PBR config (function profile): [continue]"; read go
python asa2-pbr-l3fw-fprof.py $pod_num $tenant_name $csr_ip

echo -e "\n10. Create ASA2 device PBR service graph: [continue]"; read go
python asa2-graph.py $pod_num $tenant_name $csr_ip

echo -e "\n11. Apply ASA2 SG and create web-to-app contract: [continue]"; read go
python asa2-apply-graph.py $pod_num $tenant_name $csr_ip

echo -e "\n12. Add ARP no redirect subject to the contract: [continue]"; read go
python asa2-arp-subject.py $pod_num $tenant_name $csr_ip

echo -e "\n13. Update ASA2 selection policy w/ one-arm information: [continue]"; read go
python asa2-pbr-sel-policy.py $pod_num $tenant_name $csr_ip

echo -e "\n14. Create ASA1 context as L4-L7 device: [continue]"; read go
python asa1-l3out-device.py $pod_num $tenant_name $csr_ip

echo -e "\n15. Create ASA1 context L3FW config / function profile: [continue]"; read go
python asa1-fprof.py $pod_num $tenant_name $csr_ip

echo -e "\n16. Create ASA1 and fabric to ASAv-outside L3outs: [continue]"; read go
python asa1-asav-l3outs.py $pod_num $tenant_name $csr_ip

echo -e "\n17. Add ASA1 service graph: [continue]"; read go
python asa1-graph.py $pod_num $tenant_name $csr_ip

echo -e "\n18. Apply ASA1 SG and create out-to-web contract: [continue]"; read go
python asa1-apply-graph.py $pod_num $tenant_name $csr_ip

echo -e "\n19. We are done!  Now test your tenant EPG connectivity using these scripts on respective linux hosts:\n";
echo -e "outside lnx: out-to-web_ping (also wget, ssh, udp)\n";
echo -e "web lnx: out-to-web_ping web-to-app_ping (also wget, ssh, udp)\n";
echo -e "app lnx: web-to-app_ping app-to-db_ping (also wget, ssh, udp)\n";
echo -e "db lnx: app-to-db_ping (also wget, ssh, udp)\n";
echo -e "Feel free to look into all scripts for your reference[continue]"; read go

