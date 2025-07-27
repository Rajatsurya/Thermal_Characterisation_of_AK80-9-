import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Load the CSV file
csv_file = "test3_3amps_data_with_avg.csv"  # Use your actual filename
df = pd.read_csv(csv_file)

# Extract time column (assuming it's the first column)
df["Time"] = df.iloc[:, 0].astype(float)

# Create new time vector at 300 Hz
start_time = df["Time"].iloc[0]
end_time = df["Time"].iloc[-1]
new_time = np.arange(start_time, end_time + 1/300, 1/300)  # Include endpoint

# Interpolate all numerical columns to 300 Hz
interp_data = {"Time": new_time}
for col in df.columns:
    if col != "Time":
        try:
            interp_data[col] = np.interp(new_time, df["Time"], df[col])
        except Exception as e:
            print(f"Skipping column {col}: {e}")

# Create interpolated DataFrame
interp_df = pd.DataFrame(interp_data)

# Filter data to only include time <= 2200 seconds
mask = interp_df["Time"] <= 2100
filtered_df = interp_df[mask]

# Save to CSV
filtered_df.to_csv("interpolated_300Hz_test_3.csv", index=False)
print("Interpolation complete. Saved to 'interpolated_300Hz_test_3.csv' with data from 0 to 2200s.")


# Plot filtered data: column 2 (already in °C) vs Time
plt.figure(figsize=(10, 4))
plt.plot(filtered_df["Time"], filtered_df.iloc[:, 1], '-', label=filtered_df.columns[1], linewidth=1)
plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.title(f"{filtered_df.columns[1]} (°C) vs Time (0 to 2200s)")
plt.legend()
plt.tight_layout()
plt.show()


 