#!/usr/bin/env python3

import argparse
import datetime
import re
import socket
import sys


def read_license_file() -> str:
    with open("LICENSE", "r", newline="") as license_file:
        contents = license_file.read()
    return contents


def valid_ipv4_address(addr: str) -> str:
    ipv4_chunk = r'([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])'
    ipv4_pattern = re.compile(fr'^({ipv4_chunk}\.){{3}}{ipv4_chunk}$')

    if ipv4_pattern.match(addr):
        return addr
    else:
        raise argparse.ArgumentTypeError(f"Not a valid IPv4 address: {addr}")


def scan_for_ports(target: str) -> None:
    """
    Performs a very rudimentary scan to determine what ports are open on the given target machine.
    """
    print('-' * 60)
    print(f"Scanning target: {target}")
    print(f"Scanning commenced at {str(datetime.datetime.now())}")
    print('-' * 60)

    try:
        for port in range(1, 1 << 16):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if sock.connect_ex((target, port)) == 0:
                print(f"Port {port} is open and accessible")
            sock.close()
    except KeyboardInterrupt:
        print("\n\nExperienced keyboard interrupt, exiting.")
        sys.exit(130)
    except socket.gaierror:
        print(f"\n\nHostname for target {target} could not be resolved, exiting.")
        sys.exit(1)
    except socket.error:
        print(f"\n\nTarget {target} not responding, exiting.")
        sys.exit(1)


def scanner():
    socket.setdefaulttimeout(0.5)
    parser = argparse.ArgumentParser(
        prog='scanner',
        description=(
            "Scans for open ports on a given target machine."
        ),
        epilog=read_license_file(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        'target',
        help='IPv4 address of the target machine',
        type=valid_ipv4_address,
    )
    args = parser.parse_args()

    scan_for_ports(args.target)


if __name__ == "__main__":
    scanner()