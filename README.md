# US Plotter - Timeseries Data Analysis

A Python toolkit for generating and analyzing microsecond counter timeseries data.

## Setup

Create and activate the virtual environment:

```bash
./setup_env.sh
source .venv/bin/activate
```

## Data Generator

Generate synthetic data with square wave patterns using `utilities/generate_data.py`.

### Usage
```bash
python3 utilities/generate_data.py <t_start> <t_end> <frequency> <rate_high> <rate_low> <duty_cycle> [options]
```

### Parameters
- `t_start`: Start timestamp (YYYY-MM-DD HH:MM:SS)
- `t_end`: End timestamp (YYYY-MM-DD HH:MM:SS)
- `frequency`: Square wave frequency in Hz
- `rate_high`: High rate in Hz (events/second)
- `rate_low`: Low rate in Hz (events/second)
- `duty_cycle`: Duty cycle (0.0 to 1.0, fraction of time at high rate)

### Examples

**Basic square wave (0.1 Hz, 30% duty cycle):**
```bash
python3 utilities/generate_data.py "2025-12-19 10:00:00" "2025-12-19 10:01:00" 0.1 100 10 0.3
```

**Fast switching (1 Hz, 50% duty cycle):**
```bash
python3 utilities/generate_data.py "2025-12-19 10:00:00" "2025-12-19 10:00:10" 1.0 200 20 0.5 --output fast_data.txt
```

**Low duty cycle (0.05 Hz, 20% duty cycle):**
```bash
python3 utilities/generate_data.py "2025-12-19 09:00:00" "2025-12-19 09:05:00" 0.05 150 5 0.2 --device ALT42 --output low_duty.txt
```

## Data Analyzer

Analyze timeseries data and create histograms using `analyze_timeseries.py`.

### Usage
```bash
python3 analyze_timeseries.py <data_file> [options]
```

### Examples

**Basic analysis (1-second bins):**
```bash
python3 analyze_timeseries.py example_data.txt
```

**High resolution (0.1-second bins):**
```bash
python3 analyze_timeseries.py generated_data.txt --bin-width 0.1
```

**Save plot to file:**
```bash
python3 analyze_timeseries.py generated_data.txt --bin-width 0.5 --output histogram.png
```

## Complete Workflow Example

Generate data and analyze it:

```bash
# Generate 2 minutes of data with 0.2 Hz square wave
python3 utilities/generate_data.py "2025-12-19 14:00:00" "2025-12-19 14:02:00" 0.2 80 15 0.4 --output test_data.txt

# Analyze with 0.5-second bins
python3 analyze_timeseries.py test_data.txt --bin-width 0.5 --output analysis.png
```

This creates a bimodal distribution with peaks around 15 Hz and 80 Hz, switching every 5 seconds (0.2 Hz) with 40% high time.

## Data Format

The data files follow this format:
```
2025-12-19 10:44:20 - Port: DEVICE_NAME
11543665558
11554575648
...
```

- Line 1: Start timestamp and device name
- Subsequent lines: Microsecond counter values (32-bit, handles rollover)