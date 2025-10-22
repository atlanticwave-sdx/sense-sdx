import json
import sys

from sense.client.address_api import AddressApi
from sense.client.discover_api import DiscoverApi
from sense.client.workflow_combined_api import WorkflowCombinedApi

from sense_sdx.models.domain import Domain, Peer_point
from sense_sdx.translate import Topologytranslator

TOPOLOGY = "topology"
INTENT = "intent"
INSTANCE = "instance"


def call_services(service=TOPOLOGY, arg=None, arg_json=None):
    discoverApi = DiscoverApi()
    response = {}
    if service == TOPOLOGY:
        if arg is None:
            print("Discovering all domains...")
            response = discoverApi.discover_domains_get()
        elif arg == "all":
            print("Discovering all domains...")
            domain_ids = discoverApi.discover_domains_get()
            domains = domain_ids["domains"]
            domain_list = [
                discoverApi.discover_domain_id_get(domain["domain_uri"])
                for domain in domains
            ]
            response["domains"] = domain_list
        else:
            print(f"Discovering domain: {arg}")
            response = discoverApi.discover_domain_id_get(arg)

    return response

def topology_translate():
    domains = call_services(service=TOPOLOGY, arg="all")
    d_t = Topologytranslator()
    topology = d_t.to_sdx_topology_json(domains["domains"])
    return topology

if __name__ == "__main__":
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])
