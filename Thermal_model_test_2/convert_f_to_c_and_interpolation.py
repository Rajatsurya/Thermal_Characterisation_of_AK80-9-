import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Load the CSV file
csv_file = "test_2_case_temp.csv"  # Use your actual filename
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

# Save to CSV
interp_df.to_csv("interpolated_300Hz_test_2.csv", index=False)
print("Interpolation complete. Saved to 'interpolated_300Hz_test_2.csv'.")


# Plot interpolated data: column 2 (already in °C) vs Time, limited to Time <= 3890
mask = interp_df["Time"] <= 3890
plt.figure(figsize=(10, 4))
plt.plot(interp_df["Time"][mask], interp_df.iloc[:, 1][mask], '-', label=interp_df.columns[1], linewidth=1)
plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.title(f"{interp_df.columns[1]} (°C) vs Time (up to 3890s)")
plt.legend()
plt.tight_layout()
plt.show()


