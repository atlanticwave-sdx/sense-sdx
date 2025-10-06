import argparse
import json
from sense_sdx.client import call_services
from sense_sdx.translate import translate_topology


def main():
    parser = argparse.ArgumentParser(description="Sense-SDX Client CLI")
    subparsers = parser.add_subparsers(dest="command")

    service_parser = subparsers.add_parser("service", help="Call service operations")
    service_parser.add_argument("--network", required=True, help="Network name")
    service_parser.add_argument("--service-json", required=True, help="Path to service definition JSON")

    translate_parser = subparsers.add_parser("translate", help="Translate topology JSON")
    translate_parser.add_argument("--topology-json", required=True, help="Path to topology JSON")
    translate_parser.add_argument("--schema", required=True, help="Path to JSON schema")

    args = parser.parse_args()

    if args.command == "service":
        topology, status = call_services(args.network, args.service_json)
        print("Topology:", json.dumps(topology, indent=2))
        print("Service Status:", status)
    elif args.command == "translate":
        with open(args.topology_json) as f:
            topology_json = json.load(f)
        translated = translate_topology(topology_json, args.schema)
        print("Translated Topology:", json.dumps(translated, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()