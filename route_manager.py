import argparse
import os
import subprocess
import re
import urllib.request
import pwd
from ip_resolver import (
    get_domain_list,
    resolve_domain_all_ips,
    write_ips_to_file
)

DEFAULT_DIR = '.dynamic-route'


def get_original_home():
    sudo_user = os.environ.get('SUDO_USER')
    if sudo_user:
        home_dir = os.path.expanduser(f"~{sudo_user}")
    else:
        home_dir = os.path.expanduser("~")
    return home_dir


def ensure_directory(path, uid=None, gid=None):
    if not os.path.exists(path):
        os.makedirs(path)
        if uid is not None and gid is not None:
            os.chown(path, uid, gid)


def download_file(url, dest):
    try:
        urllib.request.urlretrieve(url, dest)
        print(f"Downloaded {url} to {dest}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


def get_route_info(ip_address):
    try:
        result = subprocess.run(['route', '-n', 'get', ip_address], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error getting route info: {result.stderr}")
            return None, None

        gateway = re.search(r'gateway: (\S+)', result.stdout)
        interface = re.search(r'interface: (\S+)', result.stdout)

        if gateway and interface:
            return gateway.group(1), interface.group(1)
        else:
            return None, None

    except subprocess.CalledProcessError as e:
        print(f"Error checking route: {e}")
        return None, None


def read_resolved_ips(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        return []


def add_route(gateway, resolved_file):
    ips = read_resolved_ips(resolved_file)
    if not ips:
        print(f"No IP addresses found in {resolved_file}")
        return

    for ip in ips:
        command = f'route add -host {ip} {gateway}'
        subprocess.run(command, shell=True, check=True)


def delete_route(resolved_file):
    ips = read_resolved_ips(resolved_file)
    if not ips:
        print(f"No IP addresses found in {resolved_file}")
        return

    for ip in ips:
        command = f'route delete -host {ip}'
        subprocess.run(command, shell=True, check=True)


def check_vpn_connected(ip_address):
    gateway, interface = get_route_info(ip_address)
    if gateway and 'utun' in interface:
        return gateway, interface
    return None, None


def refresh_ips(output_file, uid, gid):
    domains = get_domain_list()

    all_ip_addresses = []
    for domain in domains:
        ip_addresses = resolve_domain_all_ips(domain)
        all_ip_addresses.extend(ip_addresses)

    resolved_ips = write_ips_to_file(output_file, all_ip_addresses)
    os.chown(output_file, uid, gid)

    print(f"Resolved {len(domains)} domains to {len(resolved_ips)} IPs")
    print(f"IP addresses resolved and written to {output_file}")


def update_routing_table(ip_address):
    # Check if the script is run with root permissions
    if os.geteuid() != 0:
        print("This script must be run as root. Please use sudo.")
        return

    # Ensure correct ownership for directories and files
    original_user = os.environ.get('SUDO_USER')
    if not original_user:
        print("Error: SUDO_USER is not set. This script must be run with sudo.")
        return

    original_user_info = pwd.getpwnam(original_user)
    original_uid = original_user_info.pw_uid
    original_gid = original_user_info.pw_gid

    original_home = get_original_home()
    default_dir_path = os.path.join(original_home, DEFAULT_DIR)
    ensure_directory(default_dir_path, original_uid, original_gid)

    default_resolved_file = os.path.join(default_dir_path, 'resolved.txt')
    if not os.path.exists(default_resolved_file):
        print(f"{default_resolved_file} not found. Please execute the 'resolved-ips' command first.")
        return

    # Check if VPN is connected
    gateway, interface = check_vpn_connected(ip_address)
    if gateway and interface:
        print(f"VPN is connected.\nInterface (dev): {interface}\nGateway: {gateway}")
        add_route(gateway, default_resolved_file)
    else:
        # print("VPN is not connected. Deleting extra routes.")
        # delete_route(default_resolved_file)
        print("VPN is not connected. Skip to update.")


def main():
    parser = argparse.ArgumentParser(description='Manage VPN routes and resolve IP addresses.')
    subparsers = parser.add_subparsers(dest='command')

    parser_resolved_ips = subparsers.add_parser('resolved-ips', help='Refresh IP list from domains.txt')
    parser_route = subparsers.add_parser('route', help='Update routing table')
    parser_route.add_argument('ip_address', help='IP address to check route for VPN connection')

    args = parser.parse_args()

    if args.command == 'resolved-ips':
        original_home = get_original_home()
        default_dir_path = os.path.join(original_home, DEFAULT_DIR)
        ensure_directory(default_dir_path)

        default_resolved_file = os.path.join(default_dir_path, 'resolved.txt')

        original_user = os.environ.get('SUDO_USER') or os.environ.get('USER')
        original_user_info = pwd.getpwnam(original_user)
        original_uid = original_user_info.pw_uid
        original_gid = original_user_info.pw_gid

        refresh_ips(default_resolved_file, original_uid, original_gid)
    elif args.command == 'route':
        update_routing_table(args.ip_address)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
