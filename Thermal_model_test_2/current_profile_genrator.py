import numpy as np
import pandas as pd

# Constants
duration_sec = 1800  # 1/2 hour
frequency_hz = 3000  # 3000 Hz
total_samples = duration_sec * frequency_hz

# Durations in seconds
initial_off_sec = 60         # First 1 minute of 0 mA
on_duration_sec = 10 * 60    # 10 minutes at 10000 mA
off_duration_sec = 0         # No off period after ramp (only initial 1 min off per cycle)

# Samples
initial_off_samples = initial_off_sec * frequency_hz
on_samples = on_duration_sec * frequency_hz

# Create one cycle: 1 min 0 mA + 10 min 10000 mA = 11 min = 198000 samples
one_cycle_current = np.concatenate([
    np.zeros(initial_off_samples),      # 0 mA for 1 min
    np.full(on_samples, 10000)           # 10000 mA for 10 min
])

cycle_samples = len(one_cycle_current)
num_cycles = int(np.ceil(total_samples / cycle_samples))

# Repeat the cycle and truncate to exactly 1 hour
full_current = np.tile(one_cycle_current, num_cycles)[:total_samples]
time_array = np.linspace(0, duration_sec, total_samples, endpoint=False)

# Create DataFrame
df = pd.DataFrame({
    'time (s)': time_array,
    'current (mA)': full_current
})

# Save to CSV
csv_path = "current_log_1hr_300Hz_10000mA.csv"
df.to_csv(csv_path, index=False)

csv_path
