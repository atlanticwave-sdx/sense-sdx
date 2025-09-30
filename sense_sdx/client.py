from sense.client.workflow_combined_api import WorkflowCombinedApi
from sense.client.address_api import AddressApi
from sense.client.discover_api import DiscoverApi

def call_services(network_name, service_json_path):
    username, password, secret = load_credentials()
    client = sense_o_client_library.Client(username, password, secret)
    topology = client.get_topology(network_name)
    with open(service_json_path) as f:
        service_def = f.read()
    service_id = client.create_service(service_def)
    status = client.check_service_status(service_id)
    client.delete_service(service_id)
    return topology, status