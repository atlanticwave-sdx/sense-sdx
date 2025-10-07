import argparse
import json
from sense_sdx.client import call_services
from sense_sdx.translate import *


def main():
    parser = argparse.ArgumentParser(description="Sense-SDX Client CLI")
    subparsers = parser.add_subparsers(dest="command")

    service_parser = subparsers.add_parser("client", help="Call service operations")
    service_parser.add_argument("--service", required=True, help="service name")
    service_parser.add_argument("--domain", required=False, help="domain id")
    service_parser.add_argument("--service-json", required=False, help="Path to service definition JSON")

    translate_parser = subparsers.add_parser("translate", help="Translate topology JSON")
    translate_parser.add_argument("--topology-json", required=True, help="Path to topology JSON")
    translate_parser.add_argument("--schema", required=True, help="Path to JSON schema")

    args = parser.parse_args()

    if args.command == "client":
        response = call_services(args.service, args.domain, args.service_json)
        if len(response) == 0 or "ERROR" in response:
            raise ValueError(f"Discover query failed with option `{args.discover}`")
        print(response)
    elif args.command == "translate":
        with open(args.topology_json) as f:
            topology_json = json.load(f)
        translated = Topologytranslator.to_sdx(topology_json)
        print("Translated Topology:", json.dumps(translated, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()