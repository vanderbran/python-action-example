import re
from collections import defaultdict
import sys

def parse_log_line(line):
    """
    Uses Regex to parse through an error pulling out: ip, time, method, path, protocol, and status. 

    Args: 
        line (string): The error line. 

    Returns:
        Dictionary containing IP, Status, and Path
    """

    # Regex Pattern to match this string: 
    # ::ffff:10.122.144.51 - - [07/Oct/2025 12:02:27] "GET / HTTP/1.1" 200 -
    # NOTE: I did remove the last (\d+) which stores size 
    pattern = r'(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) (\S+)"'
    match = re.match(pattern, line)

    # If we match, create a dictionary based off of results 
    if match:
        ip, timestamp, method, path, protocol, status = match.groups()
        if int(status) >= 400:
            return {'ip': ip, 'status': status, 'path': path}
    return None

def analyze_logs(file_path):
    """
    Counts number of errors from IPs, or number of errors by status

    Args: 
        file_path: path to log file containing errors 

    Returns:
        Dictionary containing counts of errors
    """

    # Dictionary to count how many errors we have 
    errors_by_ip = defaultdict(int)
    errors_by_status = defaultdict(int)
    with open(file_path, 'r') as f:
        for line in f:
            error = parse_log_line(line.strip())
            if error:
                errors_by_ip[error['ip']] += 1
                errors_by_status[error['status']] += 1
    return {'errors_by_ip': dict(errors_by_ip), 'errors_by_status': dict(errors_by_status)}

def main():
    # yell at user if they're dumb 
    if len(sys.argv) != 2:
        print("Usage: python analyzer.py <log_file>")
        sys.exit(1)
    # else, report.
    report = analyze_logs(sys.argv[1])
    print("Error Summary:", report)

if __name__ == '__main__':
    main()
