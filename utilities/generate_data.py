#!/usr/bin/env python3
import argparse
import numpy as np
from datetime import datetime, timedelta
import random

# 32-bit counter maximum value
U32_MAX = 2**32

def generate_square_wave_data(t_start, t_end, frequency, rate_high, rate_low, duty_cycle, device_name="TEST01"):
    """
    Generate synthetic microsecond counter data following a square wave pattern.
    
    Args:
        t_start: Start timestamp string (YYYY-MM-DD HH:MM:SS)
        t_end: End timestamp string (YYYY-MM-DD HH:MM:SS) 
        frequency: Square wave frequency in Hz
        rate_high: High rate in Hz (events per second)
        rate_low: Low rate in Hz (events per second)
        duty_cycle: Duty cycle (0.0 to 1.0, fraction of time at high rate)
        device_name: Device identifier
    
    Returns:
        List of lines for the output file
    """
    
    # Parse timestamps
    start_dt = datetime.strptime(t_start, '%Y-%m-%d %H:%M:%S')
    end_dt = datetime.strptime(t_end, '%Y-%m-%d %H:%M:%S')
    total_duration = (end_dt - start_dt).total_seconds()
    
    if total_duration <= 0:
        raise ValueError("End time must be after start time")
    
    # Calculate square wave period
    period = 1.0 / frequency  # seconds
    high_time = period * duty_cycle
    low_time = period * (1 - duty_cycle)
    
    # Generate events
    events = []
    current_time = 0.0
    microsecond_counter = random.randint(0, 1000000)  # Random starting counter
    
    while current_time < total_duration:
        # Determine current phase of square wave
        phase_time = current_time % period
        
        if phase_time < high_time:
            # High phase
            target_rate = rate_high
        else:
            # Low phase  
            target_rate = rate_low
        
        # Add some normal distribution around the target rate
        # Standard deviation is 10% of the rate to keep it realistic
        actual_rate = max(0.1, np.random.normal(target_rate, target_rate * 0.1))
        
        # Calculate time to next event (exponential distribution for Poisson process)
        if actual_rate > 0:
            inter_event_time = np.random.exponential(1.0 / actual_rate)
        else:
            inter_event_time = 1.0  # Fallback
        
        current_time += inter_event_time
        
        if current_time < total_duration:
            # Convert to microseconds and add to counter
            microseconds_elapsed = int(inter_event_time * 1e6)
            microsecond_counter += microseconds_elapsed
            
            # Handle 32-bit counter rollover
            microsecond_counter = microsecond_counter % U32_MAX
            
            events.append(microsecond_counter)
    
    # Format output
    lines = []
    lines.append(f"{t_start} - Port: {device_name}")
    
    for counter in events:
        lines.append(str(counter))
    
    return lines

def main():
    parser = argparse.ArgumentParser(description='Generate synthetic timeseries data with square wave pattern')
    parser.add_argument('t_start', help='Start time (YYYY-MM-DD HH:MM:SS)')
    parser.add_argument('t_end', help='End time (YYYY-MM-DD HH:MM:SS)')
    parser.add_argument('frequency', type=float, help='Square wave frequency in Hz')
    parser.add_argument('rate_high', type=float, help='High rate in Hz (events/sec)')
    parser.add_argument('rate_low', type=float, help='Low rate in Hz (events/sec)')
    parser.add_argument('duty_cycle', type=float, help='Duty cycle (0.0 to 1.0)')
    parser.add_argument('--output', '-o', help='Output filename (default: generated_data.txt)')
    parser.add_argument('--device', default='TEST01', help='Device name (default: TEST01)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not (0.0 < args.duty_cycle < 1.0):
        print("Error: Duty cycle must be between 0.0 and 1.0")
        return 1
    
    if args.rate_high <= 0 or args.rate_low <= 0:
        print("Error: Rates must be positive")
        return 1
    
    if args.frequency <= 0:
        print("Error: Frequency must be positive")
        return 1
    
    try:
        lines = generate_square_wave_data(
            args.t_start, args.t_end, args.frequency,
            args.rate_high, args.rate_low, args.duty_cycle,
            args.device
        )
        
        output_file = args.output or 'generated_data.txt'
        
        with open(output_file, 'w') as f:
            for line in lines:
                f.write(line + '\n')
        
        print(f"Generated {len(lines)-1} data points")
        print(f"Output written to: {output_file}")
        print(f"Square wave: {args.frequency} Hz, {args.duty_cycle*100:.1f}% duty cycle")
        print(f"Rates: {args.rate_high} Hz (high) / {args.rate_low} Hz (low)")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    main()