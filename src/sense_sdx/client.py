from sense.client.workflow_combined_api import WorkflowCombinedApi
from sense.client.address_api import AddressApi
from sense.client.discover_api import DiscoverApi

from sense_sdx.models import domain,peer_point, instance,intent

TOPOLOGY = "topology"
INTENT = "intent"
INSTANCE = "instance"
DOMAIN = "domain"


def sense_parse(aDomain) -> dict:
    # Assuming the input is a dictionary representing a domain
    node = domain(aDomain)
    return node

def topology_assembly(domains={}):
    topology=[]
    for _, domain in domains:  #each domain is represented by a node
        node = sense_parse(domain)
        topology.append(node)
    return topology

def call_services(service=TOPOLOGY, arg = None, arg_json = None):
    discoverApi = DiscoverApi()
    response = {}
    if service == TOPOLOGY:
        domain_ids = discoverApi.discover_domains_get()
        domains=domain_ids["domains"]
        domain_list = [discoverApi.discover_domain_id_get(domain_uri) for domain_uri, _ in domains]
        response["domains"] = domain_list

    if service == DOMAIN:
        response = discoverApi.discover_domain_id_get(arg)

    print(f"Response type: {type(response)}")

    return response




