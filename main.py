import os
import time
import random
import argparse
from dotenv import load_dotenv
import requests

load_dotenv()

WEBEX_TOKEN = os.getenv('WEBEX_ACCESS_TOKEN')
WEBEX_ROOM_ID = os.getenv('WEBEX_ROOM_ID')
WEBEX_API_URL = "https://webexapis.com/v1/messages"

def send_webex_message(message):
    if not WEBEX_TOKEN or not WEBEX_ROOM_ID:
        print("Error: Webex credentials not set.")
        return

    headers = {
        "Authorization": f"Bearer {WEBEX_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "roomId": WEBEX_ROOM_ID,
        "text": message
    }
    response = requests.post(WEBEX_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        print("Notification sent to Webex.")
    else:
        print(f"Error sending to Webex: {response.text}")

def simulate_network_config():
    interfaces = ["eth0", "eth1", "eth2"]
    config = {}
    for iface in interfaces:
        config[iface] = {
            "ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "status": random.choice(["up", "down"])
        }
    return config

def detect_changes(old_config, new_config):
    changes = []
    for key in new_config:
        if old_config.get(key) != new_config.get(key):
            changes.append(f"Change in {key}: {old_config.get(key)} -> {new_config.get(key)}")
    return changes

def main(demo_mode, runtime, interval):
    start_time = time.time()
    previous_config = simulate_network_config()
    print("Initial network config:", previous_config)

    while time.time() - start_time < runtime:
        time.sleep(interval)
        current_config = simulate_network_config()
        changes = detect_changes(previous_config, current_config)
        
        if changes:
            change_msg = "Network configuration change detected:\n" + "\n".join(changes)
            print(change_msg)
            if not demo_mode:
                send_webex_message(change_msg)
        
        previous_config = current_config

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Network Config Change Bot")
    parser.add_argument("-d", "--demo", action="store_true", help="Run in demo mode (no Webex notifications)")
    parser.add_argument("-t", "--time", type=int, default=60, help="Runtime in seconds (default: 60)")
    parser.add_argument("-i", "--interval", type=int, default=5, help="Check interval in seconds (default: 5)")
    args = parser.parse_args()

    main(args.demo, args.time, args.interval)