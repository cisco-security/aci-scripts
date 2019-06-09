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

echo -e "\nWelcome to your demo1 build-out under ACI tenant $tenant_name\n";
echo -e "Please follow these steps to orchestrate security and networking for your tenant.\n";
echo -e "- If any of these steps fail with python errors, please contact your proctor with a step that failed.";
echo -e "- Note that we are applying a whole tenant in one step using a script. Script will dump xml code being applied to your APIC tenant.";
echo -e "- Press Enter to continue and execute each step script.";

echo -e "\n1. Create demo1 topology with app profiles, epgs, bd, vrf, ftd pbr graph and all contracts used by it: [continue]"; read go
python pbr-tenant.py $pod_num $tenant_name $csr_ip 

