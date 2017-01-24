#!/bin/bash
################################################################################
#                                                                              #
# Copyright (c) 2017 Cisco Systems                                             #
# All Rights Reserved.                                                         #
#                                                                              #
#    Licensed under the Apache License, Version 2.0 (the "License"); you may   #
#    not use this file except in compliance with the License. You may obtain   #
#    a copy of the License at                                                  #
#                                                                              #
#         http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                              #
#    Unless required by applicable law or agreed to in writing, software       #
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT #
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the  #
#    License for the specific language governing permissions and limitations   #
#    under the License.                                                        #
#                                                                              #
################################################################################
#
# youtube Demo
#
#
#path="$HOME/demo/aci-scripts/"
path=""
for i in {2..2};
   do
   echo "Please delete pod$i tenant now to allow us to recreate it;:  [continue]"; read go
      
   echo "Create pod$i tenant app profile, EPGs, vrfs, BDs:  [continue]"; read go
   python ${path}faba-tenant-apps.py $i $i
   
   echo "Create asa failover pbr bridge domain: [continue]"; read go
   python ${path}faba-asa-fover-pbr-bd.py $i $i

   echo "Create pbr protocol redirect (ASA device IP and MAC to send traffic to): [continue]"; read go
   python ${path}faba-pbr-redirect.py $i $i

   echo "Create and register an ASA pbr L4-L7 device: [continue]"; read go
   python ${path}faba-asa-pbr-device.py $i $i
   
   echo "Create an ASA function profile (Note: ASA MAC is set to match pbr redirect MAC): [continue]"; read go
   python ${path}faba-pbr-fprof.py $i $i

   echo "Add pbr service graph: [continue]"; read go
   python ${path}faba-asa-pbr-graph.py $i $i
   
   echo "Apply asa-fover SG and create web-to-app contract: [continue]"; read go
   python ${path}faba-asa-pbr-apply-graph.py $i $i
   
   echo "Add arp subject to web-to-app contract and avoide ARP redirect: [continue]"; read go
   python ${path}faba-arp-subject.py $i $i
   
   echo "Update asa pbr graph selection policy to reflect one consumer interface (can not be done w/ wizard): [continue]"; read go
   python ${path}faba-asa-pbr-sel-policy.py $i $i

   echo "We are done, now review pod$i tenant and ping out->web and app->db: [continue]"; read go
   done
