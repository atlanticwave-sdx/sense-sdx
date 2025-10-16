import json

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
            with open("./tests/data/domain_ids.json", "w") as f:
                json.dump(response, f, indent=2)
        elif arg == "all":
            print("Discovering all domains...")
            domain_ids = discoverApi.discover_domains_get()
            domains = domain_ids["domains"]
            domain_list = [
                discoverApi.discover_domain_id_get(domain_uri)
                for domain_uri, _ in domains
            ]
            response["domains"] = domain_list
            with open("./tests/data/domains.json", "w") as f:
                json.dump(response, f, indent=2)
        else:
            print(f"Discovering domain: {arg}")
            response = discoverApi.discover_domain_id_get(arg)
            domain_uri = response.get("domain_uri", "")
            domain_name = domain_uri.split(":")[3] if domain_uri else "unknown"
            with open(f"./tests/data/{domain_name}.json", "w") as f:
                json.dump(response, f, indent=2)

    return response


def topology_translate():
    domains = call_services(service=TOPOLOGY, arg="all")
    d_t = Topologytranslator()
    topology = d_t.to_sdx_topology_json(domains["domains"])
    return topology
