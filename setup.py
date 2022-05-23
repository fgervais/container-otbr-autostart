import json
import requests


SERVER_URL = "http://172.17.0.1:8090"

r = requests.get(f"{SERVER_URL}/get_properties")
print(r)
print(json.dumps(r.json(), indent=4, sort_keys=True))
# {
#  "error": 0,
#  "result": {
#      "IPv6:LinkLocalAddress": "fe80:0:0:0:8414:f874:4d21:4a8a",
#      "IPv6:LocalAddress": "fd11:22:0:0:dc95:c18a:c980:a51c",
#      "IPv6:MeshLocalAddress": "fdb3:fbff:f658:533c:e9f8:2592:6746:d2ed",
#      "IPv6:MeshLocalPrefix": "fdb3:fbff:f658:533c:",
#      "Network:Name": "> OpenThreadDemo",
#      "Network:PANID": "> 0xabcd",
#      "Network:PartitionID": "> 125390837",
#      "Network:XPANID": "> 202b057ee33d275c",
#      "OpenThread:Version": "OPENTHREAD/3b79cb0; POSIX; Feb  2 2022 18:44:57",
#      "OpenThread:Version API": "> 190",
#      "RCP:Channel": "> 15",
#      "RCP:EUI64": "> f4ce36ad82508c30",
#      "RCP:State": "leader",
#      "RCP:TxPower": "> 0 dBm",
#      "RCP:Version": "> OPENTHREAD/thread-reference-20200818-1510-g3b79cb0d0; NRF52840; Feb  4 2022 14:50:10",
#      "WPAN service": "associated"
#  }
# }



# curl --header "Content-Type: application/json" --request POST --data \
#     "{\"networkKey\":\"${OT_NETWORK_KEY}\",\
#     \"prefix\":\"fd11:22::\",\
#     \"defaultRoute\":true,\
#     \"extPanId\":\"${OT_XPANID}\",\
#     \"panId\":\"${OT_PANID}\",\
#     \"passphrase\":\"${OT_AGENT_PASSPHRASE}\",\
#     \"channel\":${OT_CHANNEL},\
#     \"networkName\":\"${OT_NETWORK_NAME}\"}" \
#     "${OTBR_WEB_URL}"/form_network | grep "success"
