import json
import sys

from sense.client.address_api import AddressApi
from sense.client.discover_api import DiscoverApi
from sense.client.workflow_combined_api import WorkflowCombinedApi

from sense_sdx.models.domain import Domain, Peer_point
from sense_sdx.translate import Responsetranslator, Topologytranslator

TOPOLOGY = "topology"
INTENT = "intent"
INSTANCE = "instance"
STATUS = "status"
CANCEL = "cancel"


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
    elif service == INTENT:
        workflowApi = WorkflowCombinedApi()
        if arg_json is not None:
            print(f"Submitting intent with JSON: {arg_json}")
            response = workflowApi.instance_create(arg_json)
            workflowApi.instance_operate("provision", sync="true")
            status = workflowApi.instance_get_status()
            print(f"provision status={status}")
    elif service == INSTANCE:
        workflowApi = WorkflowCombinedApi()
        if arg is not None and arg_json is not None:
            if arg == STATUS:
                print(f"Operating instance {arg} with JSON: {arg_json}")
                workflowApi.si_uuid = arg_json.get("instance_id")
                response = workflowApi.instance_get_status()
            if arg == CANCEL:
                print(f"Cancelling instance {arg_json.get('instance_id')}")
                workflowApi.si_uuid = arg_json.get("instance_id")
                response = workflowApi.instance_operate(
                    "cancel", si_uuid=arg_json.get("instance_id"), sync="true"
                )
        else:
            print("No intent JSON provided.")

    return response


def topology_translate():
    domains = call_services(service=TOPOLOGY, arg="all")
    d_t = Topologytranslator()
    topology = d_t.to_sdx_topology_json(domains["domains"])
    return topology


def intent_translate(connection_json: str):
    from sense_sdx.translate import Intenttranslator

    i_t = Intenttranslator()
    intent = i_t.from_sdx_request_json(connection_json)

    response = call_services(service=INTENT, arg_json=intent)

    r_t = Responsetranslator()
    response = r_t.to_sdx_response_json(response)
    return response


def instance_translate(uuid: str, action: str):
    response = call_services(
        service=INSTANCE, arg=action, arg_json={"instance_id": uuid}
    )

    r_t = Responsetranslator()
    response = r_t.to_sdx_response_json(response)

    return response


if __name__ == "__main__":
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])
