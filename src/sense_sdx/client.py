from sense.client.workflow_combined_api import WorkflowCombinedApi
from sense.client.address_api import AddressApi
from sense.client.discover_api import DiscoverApi

TOPOLOGY = "topology"
INTENT = "intent"
INSTANCE = "instance"
DOMAIN = "domain"

def call_services(service=TOPOLOGY, arg = None, arg_json = None):
    discoverApi = DiscoverApi()
    response = None
    if service == TOPOLOGY:
        response = discoverApi.discover_domains_get()

    if service == DOMAIN:
        response = discoverApi.discover_domain_id_get(arg)

    print(f"Response type: {type(response)}")

    return response

