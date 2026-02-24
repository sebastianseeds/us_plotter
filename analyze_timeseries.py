#!/usr/bin/env python3
import argparse
import re
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

# 32-bit counter maximum value
U32_MAX = 2**32

def parse_data_file(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    # Parse first line for timestamp and device
    first_line = lines[0]
    timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', first_line)
    device_match = re.search(r'Port:\s*(\S+)', first_line)
    
    if not timestamp_match:
        raise ValueError("Could not parse timestamp from first line")
    
    start_timestamp = datetime.strptime(timestamp_match.group(1), '%Y-%m-%d %H:%M:%S')
    device_name = device_match.group(1) if device_match else "Unknown"
    
    # Parse microsecond counters
    counters = []
    for line in lines[1:]:
        try:
            counter = int(line)
            counters.append(counter)
        except ValueError:
            continue
    
    return start_timestamp, device_name, counters

def create_timeseries_histogram(start_timestamp, counters, bin_width=1.0):
    if len(counters) < 2:
        return None, None
    
    # Calculate time deltas in seconds
    # Each increment in counter represents 1 microsecond
    time_deltas = []
    prev_counter = counters[0]
    
    for counter in counters[1:]:
        # Handle rollover (32-bit counter)
        if counter < prev_counter:
            # Counter rolled over
            delta = (U32_MAX - prev_counter) + counter
        else:
            delta = counter - prev_counter
        
        # Convert microseconds to seconds
        time_deltas.append(delta / 1e6)
        prev_counter = counter
    
    # Create histogram bins
    max_time = sum(time_deltas)
    num_bins = int(np.ceil(max_time / bin_width))
    bins = np.linspace(0, num_bins * bin_width, num_bins + 1)
    
    # Calculate cumulative time for each event
    cumulative_times = np.cumsum(time_deltas)
    
    # Create histogram
    hist, bin_edges = np.histogram(cumulative_times, bins=bins)
    
    # Convert bin edges to actual timestamps
    timestamps = [start_timestamp + timedelta(seconds=t) for t in bin_edges[:-1]]
    
    return timestamps, hist

def main():
    parser = argparse.ArgumentParser(description='Analyze timeseries data from microsecond counter file')
    parser.add_argument('data_file', help='Path to the data file')
    parser.add_argument('--bin-width', type=float, default=1.0, help='Histogram bin width in seconds (default: 1.0)')
    parser.add_argument('--output', help='Output filename for plot (optional)')
    
    args = parser.parse_args()
    
    try:
        start_timestamp, device_name, counters = parse_data_file(args.data_file)
        print(f"Device: {device_name}")
        print(f"Start time: {start_timestamp}")
        print(f"Number of data points: {len(counters)}")
        
        timestamps, hist = create_timeseries_histogram(start_timestamp, counters, args.bin_width)
        
        if timestamps is None:
            print("Not enough data points to create histogram")
            return
        
        # Create plot
        plt.figure(figsize=(12, 6))
        plt.bar([t for t in timestamps], hist, width=timedelta(seconds=args.bin_width*0.8))
        plt.xlabel('Time')
        plt.ylabel('Event Count')
        plt.title(f'Timeseries Histogram - {device_name} (Bin width: {args.bin_width}s)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if args.output:
            plt.savefig(args.output)
            print(f"Plot saved to {args.output}")
        else:
            plt.show()
            
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    main()