import numpy as np
import pandas as pd

# Constants
sampling_frequency_hz = 300
total_duration_sec = 33 * 60  # 33 minutes

# Cycle parameters
off_duration_sec = 60         # 1 minute at 0 amps
on_duration_sec = 10 * 60     # 10 minutes at 3 amps
num_cycles = 3

# Calculate samples per cycle
off_samples = off_duration_sec * sampling_frequency_hz
on_samples = on_duration_sec * sampling_frequency_hz
cycle_samples = off_samples + on_samples

# Create one cycle: 1 min 0 amps + 10 min 3 amps
one_cycle_current = np.concatenate([
    np.zeros(off_samples),      # 0 amps for 1 min
    np.full(on_samples, 4)      # 3 amps for 10 min
])

# Repeat the cycle 3 times
total_samples = cycle_samples * num_cycles
full_current = np.tile(one_cycle_current, num_cycles)

# Create time array
time_array = np.linspace(0, total_duration_sec, total_samples, endpoint=False)

# Create DataFrame
df = pd.DataFrame({
    'Time (s)': time_array,
    'current (mA)': full_current * 1000  # Convert A to mA
})

# Save to CSV
csv_path = "current_profile_33min_300Hz_4amps.csv"
df.to_csv(csv_path, index=False)

print(f"Current profile generated successfully!")
print(f"Total duration: {total_duration_sec/60:.1f} minutes")
print(f"Sampling frequency: {sampling_frequency_hz} Hz")
print(f"Number of cycles: {num_cycles}")
print(f"Each cycle: {off_duration_sec/60:.1f} min at 0A + {on_duration_sec/60:.1f} min at 3A")
print(f"Total samples: {len(df)}")
print(f"Saved to: {csv_path}")

# Optional: Display first few rows
print("\nFirst 10 rows:")
print(df.head(10)) 

