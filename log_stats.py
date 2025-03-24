#!/usr/bin/env python3

import re
import sys
from collections import defaultdict, Counter

def main(log_file):
    if not os.path.isfile(log_file):
        print(f"Error: {log_file} not found.")
        sys.exit(1)

    with open(log_file, 'r') as f:
        lines = f.readlines()

if __name__ == "__main__":
    main(sys.argv[1])

log_pattern = re.compile(
    r'(?P<host>\S+) \S+ \S+ \[(?P<datetime>[^\]]+)\] "(?P<method>\S+) (?P<resource>\S+) \S+" (?P<status>\d{3}) (?P<size>\S+) ".*?" ".*?"'
)

def parse_log_line(line):
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    else:
        return None

def human_readable_percent(part, total):
    return f"{(part / total) * 100:.2f}%" if total else "0.00%"

def main(log_file):
    total_requests = 0
    total_data = 0
    resource_counter = Counter()
    host_counter = Counter()
    status_counter = Counter()

    with open(log_file, 'r') as f:
        for line in f:
            data = parse_log_line(line)
            if not data:
                continue

            total_requests += 1
            size = int(data['size']) if data['size'] != '-' else 0
            total_data += size

            resource_counter[data['resource']] += 1
            host_counter[data['host']] += 1
            status_counter[data['status']] += 1

    if total_requests == 0:
        print("No valid log lines found.")
        return

    most_requested_resource, resource_count = resource_counter.most_common(1)[0]
    most_active_host, host_count = host_counter.most_common(1)[0]

    print(f"Total number of requests: {total_requests}")
    print(f"Total data transmitted: {total_data} bytes")
    print()
    print(f"Most requested resource: {most_requested_resource}")
    print(f"  Total requests for this resource: {resource_count}")
    print(f"  Percentage of requests: {human_readable_percent(resource_count, total_requests)}")
    print()
    print(f"Remote host with most requests: {most_active_host}")
    print(f"  Total requests from this host: {host_count}")
    print(f"  Percentage of requests: {human_readable_percent(host_count, total_requests)}")
    print()
    print("HTTP Status Code Percentages:")
    classes = {'1xx': 0, '2xx': 0, '3xx': 0, '4xx': 0, '5xx': 0}
    for status, count in status_counter.items():
        if status.startswith('1'):
            classes['1xx'] += count
        elif status.startswith('2'):
            classes['2xx'] += count
        elif status.startswith('3'):
            classes['3xx'] += count
        elif status.startswith('4'):
            classes['4xx'] += count
        elif status.startswith('5'):
            classes['5xx'] += count

    for cls, count in classes.items():
        print(f"  {cls}: {human_readable_percent(count, total_requests)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <log_file>")
        sys.exit(1)
    main(sys.argv[1])

