# log_analyzer.py

import re

def read_log_file(file_path):
    """
    Reads the log file and returns its lines as a list.
    """
    with open(file_path, 'r') as file:
        return file.readlines()

def parse_log_line(log_line):
    """
    Parses a single log line and extracts structured data.
    Returns a dictionary containing the extracted information.
    """
    parsed_data = {}

    # Extract the timestamp
    timestamp_match = re.search(r"\[(.*?)\]", log_line)
    parsed_data["timestamp"] = timestamp_match.group(1) if timestamp_match else None

    # Extract the event type
    event_match = re.search(r"EVENT:\s(\w+)", log_line)
    parsed_data["event"] = event_match.group(1) if event_match else None

    # Extract latency (remove 'ms' and convert to integer)
    latency_match = re.search(r"LATENCY:\s(\d+)ms", log_line)
    parsed_data["latency"] = int(latency_match.group(1)) if latency_match else None

    # Extract the status
    status_match = re.search(r"STATUS:\s(\w+|\d+%)", log_line)
    parsed_data["status"] = status_match.group(1) if status_match else None

    # Extract error details (if present)
    error_match = re.search(r"ERROR:\s(.+)$", log_line)
    parsed_data["error"] = error_match.group(1) if error_match else None

    return parsed_data

def analyze_logs(log_lines):
    """
    Analyzes a list of log lines and categorizes events.
    Returns a dictionary summarizing the analysis.
    """
    analysis = {
        "total_logs": 0,
        "events": {},
        "errors": []
    }

    for line in log_lines:
        log_data = parse_log_line(line)
        analysis["total_logs"] += 1

        # Count occurrences of each event
        event = log_data.get("event")
        if event:
            if event not in analysis["events"]:
                analysis["events"][event] = 0
            analysis["events"][event] += 1

        # Collect error details
        if log_data.get("error"):
            analysis["errors"].append(log_data)

    return analysis

def display_analysis(analysis):
    """
    Displays the log analysis results in a readable format.
    """
    print("\nLog Analysis Results:")
    print(f"Total Logs: {analysis['total_logs']}")

    print("\nEvent Counts:")
    for event, count in analysis["events"].items():
        print(f"  {event}: {count}")

    print("\nErrors:")
    if analysis["errors"]:
        for error in analysis["errors"]:
            print(f"  Timestamp: {error['timestamp']}, Event: {error['event']}, Error: {error['error']}")
    else:
        print("  No errors found.")

def main():
    """
    Main function to coordinate log file reading, analysis, and displaying results.
    """
    log_file_path = "networks_logs.txt"  # Path to the log file

    # Step 1: Read the log file
    log_lines = read_log_file(log_file_path)

    # Step 2: Analyze the logs
    analysis = analyze_logs(log_lines)

    # Step 3: Display the analysis results
    display_analysis(analysis)

if __name__ == "__main__":
    main()
