import json
import logging
import os
import requests
import signal
import sys
import time

from util.yaml import SECRET_YAML, Secrets, load_yaml


SERVER_URL = "http://otbr:80"

RETRY_DELAY_SEC = 10
INIT_DELAY_SEC = 10


# Used by docker-compose down
def sigterm_handler(signal, frame):
    logger.info("💥 Reacting to SIGTERM")
    teardown()
    sys.exit(0)


def teardown():
    pass


logging.basicConfig(
    format="[%(asctime)s] %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

if "DEBUG" in os.environ:
    logger.setLevel(logging.DEBUG)

signal.signal(signal.SIGTERM, sigterm_handler)

logger.debug("🐷 Ready!")

config = load_yaml("config.yaml", Secrets("."))
logger.debug(config)

time.sleep(INIT_DELAY_SEC)

while True:
    try:
        r = requests.get(f"{SERVER_URL}/get_properties")
        logger.debug(r)
        logger.debug(json.dumps(r.json(), indent=4, sort_keys=True))

        http_error = r.json()["error"]
        logger.debug(http_error)

        if http_error != 0:
            logger.debug("❌ HTTP error")
            time.sleep(RETRY_DELAY_SEC)
            continue

        wpan_state = r.json()["result"]["WPAN service"]
        logger.debug(wpan_state)

        if wpan_state != "offline":
            logger.debug("✔️ Already connected")
            time.sleep(RETRY_DELAY_SEC)
            continue

        time.sleep(1)
        break

    except requests.exceptions.ConnectionError:
        logger.debug("💀 Could not connect")
        time.sleep(RETRY_DELAY_SEC)


from http.client import HTTPConnection

HTTPConnection.debuglevel = 1

logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

r = requests.post(f"{SERVER_URL}/form_network", json=config)
logger.debug(r)
logger.debug(json.dumps(r.json(), indent=4, sort_keys=True))

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
