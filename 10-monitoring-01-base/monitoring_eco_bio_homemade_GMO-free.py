#!/usr/bin/env python3

import json
import time
import psutil

my_metrics = {}

# require for accurate measuring CPU %
time.sleep(0.1)

my_metrics["Timestamp"] = int(time.time())

# Get CPU metrics
my_metrics["CPU usage %"] = psutil.cpu_percent()
my_metrics["Load Average last minute"] = psutil.getloadavg()[0]

my_metrics["CPU Temperature"] = {}
coretemp = psutil.sensors_temperatures()["coretemp"]
for cpu in coretemp:
    my_metrics["CPU Temperature"][cpu.label] = cpu.current

# Get memory metrics
my_metrics["Memory usage %"] = psutil.virtual_memory().percent
my_metrics["Swap usage %"] = psutil.swap_memory().percent

# Get disk metrics
my_metrics["Disk usage %"] = {}
for partition in psutil.disk_partitions():
    my_metrics["Disk usage %"][partition.mountpoint] = psutil.disk_usage(partition.mountpoint).percent

# Get network metrics
network_counters = psutil.net_io_counters()
my_metrics["Network"] = {}
my_metrics["Network"]["Bytes sent"] = network_counters.bytes_sent
my_metrics["Network"]["Bytes received"] = network_counters.bytes_recv
my_metrics["Network"]["Packets sent"] = network_counters.packets_sent
my_metrics["Network"]["Packets received"] = network_counters.packets_recv

logfile = f"/var/log/{time.strftime('%y-%m-%d')}-awesome-monitoring.log"

with open(logfile, 'a') as f:
    json.dump(my_metrics, f)
    f.write("\n")
