import json

from sense.client.address_api import AddressApi
from sense.client.discover_api import DiscoverApi
from sense.client.workflow_combined_api import WorkflowCombinedApi

from sense_sdx.models.domain import Domain, Peer_point

TOPOLOGY = "topology"
INTENT = "intent"
INSTANCE = "instance"


def sense_parse(aDomain) -> dict:
    # Assuming the input is a dictionary representing a domain
    node = Domain(aDomain)
    return node


def topology_assembly(domains={}):
    topology = []
    for _, domain in domains:  # each domain is represented by a node
        node = sense_parse(domain)
        topology.append(node)
    return topology


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
