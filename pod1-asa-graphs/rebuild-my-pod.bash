#!/bin/bash
myip=$(curl 10.10.35.5/myip.php | grep -o '[0-9]\+[.][0-9]\+[.][0-9]\+[.][0-9]\+')

arr=(${myip//./ })
declare -i pod
pod=${arr[3]}
echo " ##You are in POD${pod}##"
#
# youtube Demo
#
# fabric a is pods 1-20
# fabric b is pods 21-$i
#
#path="$HOME/demo/aci-scripts/"
path=""
for i in $(eval echo " {$pod..$pod}");
   do
   echo " Delete pod$i tenant items (app profile,EPGs,BDs,contract,l3outs,vrfs,L4-L7 items:  [continue]"; read go
   python ${path}faba-tenant-delete.py $i $i
   echo " Create pod$i tenant app profile, EPGs, vrfs, BDs:  [continue]"; read go
   python ${path}faba-tenant-apps.py $i $i
   echo " Create asa failover context as L4-L7 device: [continue]"; read go

   python ${path}faba-asa-fover-pods.py $i $i
   echo " Create context config - function profile: [continue]"; read go
   python ${path}faba-asa-fover-fprof.py $i $i
   echo " Add service graph: [continue]"; read go
   python ${path}faba-asa-fover-graph.py $i $i
   echo " Apply asa-fover SG and create app-to-db contract: [continue]"; read go
   python ${path}faba-asa-fover-apply-graph.py $i $i
   echo " Create asa cluster context as L4-L7 device: [continue]"; read go
   python ${path}faba-asa-cluster-pods-new.py $i $i
   
   echo " Create context config - function profile: [continue]"; read go
   python ${path}faba-asa-cluster-fprof.py $i $i
   echo " Add service graph: [continue]"; read go
   python ${path}faba-asa-cluster-graph.py $i $i
   echo " Create L3outs for fabric and ASA cluster context: [continue]"; read go
   python ${path}faba-l3out.py $i $i
   echo " Apply asa-cluster SG and create out-to-web contract: [continue]"; read go
   python ${path}faba-asa-cluster-apply-graph.py $i $i
   echo " We are done, now review pod$i tenant and ping out->web and app->db: [continue]"; read go
   done
