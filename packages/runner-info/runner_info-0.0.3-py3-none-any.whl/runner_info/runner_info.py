#!/usr/bin/env python
import getpass
import json
import os
import platform
import socket
import sys
import uuid
import urllib.request
import urllib.error
from datetime import datetime
from pprint import pprint

import humanize
import psutil


def is_docker():
    cgroup_path = "/proc/self/cgroup"
    return (
        os.path.exists("./dockerenv")
        or os.path.isfile(cgroup_path)
        and any("docker" in line for line in open(cgroup_path))
    )


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

    # network
    interfaces = {}
    for interface_name, interface_addresses in psutil.net_if_addrs().items():
        interfaces[interface_name] = [
            address._asdict() for address in interface_addresses
        ]

    info["network-interfaces"] = interfaces
    info["network-connections"] = psutil.net_connections()

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
    }

    for name, data in pipeline_data.items():
        write_json(data, name)


if __name__ == "__main__":
    main()
