import requests
import json
import os
import argparse

# Load station codes from stations.json in the same folder
with open(os.path.join(os.path.dirname(__file__), "stations.json"), "r") as f:
    stations = json.load(f)

headers = {"User-Agent": "okhttp/3.12.1"}

def fetch_trains(station_code, platform):
    """Fetch train data for a given station + platform."""
    url = f"https://metro-rti.nexus.org.uk/api/times/{station_code}/{platform}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {station_code} platform {platform}: {e}")
        return []

def display_trains(station_name, station_code, platform, trains):
    """Display the next few trains for a given station platform."""
    print(f"\n{station_name} ({station_code}) - Platform {platform}")
    if not trains:
        print("  No trains found.")
        return
    for train in trains[:3]:  # show first 3 trains
        print(f"  Train {train['trn']} → {train['destination']} "
              f"({train['line']} line) - Due in {train['dueIn']} min "
              f"[{train['lastEvent']} at {train['lastEventLocation']}]")

def list_stations():
    """Print all stations and their codes."""
    print("Available stations:")
    for code, name in stations.items():
        print(f"  {code} → {name}")

def show_station(station_code):
    """Fetch and display trains for a specific station."""
    station_code = station_code.upper()
    if station_code not in stations:
        print(f"Error: Unknown station code '{station_code}'")
        return
    station_name = stations[station_code]
    for platform in [1, 2]:
        trains = fetch_trains(station_code, platform)
        display_trains(station_name, station_code, platform, trains)

def main():
    parser = argparse.ArgumentParser(description="Metro train times CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: list stations
    subparsers.add_parser("list", help="List all stations with their codes")

    # Subcommand: show trains for a station
    show_parser = subparsers.add_parser("show", help="Show trains for a station")
    show_parser.add_argument("station", help="Station code (e.g. JES, MON, HEB)")

    args = parser.parse_args()

    if args.command == "list":
        list_stations()
    elif args.command == "show":
        show_station(args.station)

if __name__ == "__main__":
    main()

