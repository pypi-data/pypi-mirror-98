#!/usr/bin/env python
import errno
import getpass
import json
import os
import platform
import socket
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime

import humanize
import psutil

from scapy.all import sr, IP, TCP, RandShort, conf


def is_docker():
    cgroup_path = "/proc/self/cgroup"
    return (
        os.path.exists("./dockerenv")
        or os.path.isfile(cgroup_path)
        and any("docker" in line for line in open(cgroup_path))
    )


def is_root():
    if os.getuid() == 0:
        return True
    return False


def is_sudo_nopasswd():
    command = ["sudo", "-v"]
    try:
        cmd1 = subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=False,
        )
        cmd1.communicate(timeout=2)
    except subprocess.TimeoutExpired:
        # sudo requires password
        cmd1.terminate()
        return False
    except FileNotFoundError:
        # sudo not installed
        return False
    return True


def get_geoip_info() -> dict:
    print("Gathering GeoIP information")
    req = urllib.request.Request("http://ip-api.com/json/")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        resp = urllib.request.urlopen(req)
        result = resp.read().decode()
        return json.loads(result)
    except urllib.error.HTTPError:
        return {}


def get_platform_info() -> dict:
    print("Gathering platform information")
    info = {}
    info["platform"] = platform.system()
    info["platform-release"] = platform.release()
    info["platform-version"] = platform.version()
    info["architecture"] = platform.machine()
    info["is-docker"] = is_docker()
    info["hostname"] = socket.gethostname()
    info["processor"] = platform.processor()

    boot_time = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time)
    info["boot-time"] = bt.isoformat()

    # cpuinfo
    info["physical_cores"] = psutil.cpu_count(logical=False)
    info["total_cores"] = psutil.cpu_count(logical=True)
    info["load-avg"] = os.getloadavg()

    # memory
    virtual_mem = psutil.virtual_memory()
    info["memory_total"] = humanize.naturalsize(virtual_mem.total)
    info["memory_available"] = humanize.naturalsize(virtual_mem.available)
    info["memory_used"] = humanize.naturalsize(virtual_mem.used)
    info["memory_percentage"] = virtual_mem.percent

    swap = psutil.virtual_memory()
    info["swap_total"] = humanize.naturalsize(swap.total)
    info["swap_available"] = humanize.naturalsize(swap.available)
    info["swap_used"] = humanize.naturalsize(swap.used)
    info["swap_percentage"] = swap.percent

    return info


def get_network_info() -> dict:
    info = {}
    interfaces = {}
    for interface_name, interface_addresses in psutil.net_if_addrs().items():
        interfaces[interface_name] = [
            address._asdict() for address in interface_addresses
        ]

    info["network-interfaces"] = interfaces
    info["network-connections"] = psutil.net_connections()
    routes = str(conf.route).split("\n")
    headers = routes[0]
    info["routes"] = [
        dict(zip(headers.split(), route.split())) for route in routes[:0:-1]
    ]
    if is_root():
        ans, unans = sr(IP(dst="1.1.1.1", ttl=(4, 25), id=RandShort()) / TCP(flags=0x2))
        info["traceroute"] = ans
    return info


def get_runtime_info() -> dict:
    print("Gathering runtime information")
    info = {}
    info["login"] = getpass.getuser()
    info["uid"] = os.getuid()
    info["gid"] = os.getgid()
    info["groups"] = os.getgroups()
    info["args"] = sys.argv
    info["python-version"] = platform.python_version()
    info["executable"] = sys.executable
    info["paths"] = sys.path
    info["is_root"] = is_root()
    info["is_sudo_nopasswd"] = is_sudo_nopasswd()

    info["users"] = []
    if "Linux" in platform.platform():
        with open("/etc/passwd", "r", encoding="utf-8") as infile:
            info["users"] = [line.rstrip() for line in infile]

        info["homedirs"] = os.listdir("/home")

    info["executables"] = []
    for path in os.getenv("PATH").split(":"):
        try:
            info["executables"].extend(os.listdir(path))
        except FileNotFoundError:
            continue

    return info


def get_filesystem_info() -> dict:
    print("Gathering filesystem information")
    info = {}
    info["disks"] = {}

    # Get partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        part = {}
        part["mountpoint"] = partition.mountpoint
        part["fstype"] = partition.fstype
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            part["total-size"] = humanize.naturalsize(partition_usage.total)
            part["used"] = humanize.naturalsize(partition_usage.used)
            part["free"] = humanize.naturalsize(partition_usage.free)
            part["percentage"] = partition_usage.percent
        except PermissionError:
            continue

        info["disks"][partition.device] = part

    # Get all mounts
    info["mounts"] = []
    if "Linux" in platform.platform():
        with open("/proc/mounts", "r", encoding="utf-8") as infile:
            info["mounts"] = [line.rstrip() for line in infile]

    info["cwd"] = os.getcwd()
    return info


def get_environment_info() -> dict:
    print("Gathering environment information")
    return dict(os.environ)


def write_json(data, filename):
    if not os.path.exists("output"):
        os.makedirs("output")
    with open(f"output/{filename}.json", "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4)


def main():
    pipeline_data = {
        "platform_info": get_platform_info(),
        "runtime_info": get_runtime_info(),
        "env_variables": get_environment_info(),
        "filesystem_info": get_filesystem_info(),
        "geoip_info": get_geoip_info(),
        "network_info": get_network_info(),
    }

    for name, data in pipeline_data.items():
        write_json(data, name)


if __name__ == "__main__":
    main()
