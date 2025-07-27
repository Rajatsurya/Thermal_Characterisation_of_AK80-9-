import pandas as pd
import numpy as np

# Load the CSV file
csv_file = "case avg temp test 2.csv"
df = pd.read_csv(csv_file)

# Rename the temperature column for ease of use
f_col = "plastic metal intersection*.Max. (F)"
df = df.rename(columns={f_col: "Temp_F"})

# Convert Fahrenheit to Celsius and add as new column
df["Temp_C"] = (df["Temp_F"] - 32) * 5 / 9

# Extract time column (assuming it's the first unnamed column)
df["Time"] = df.iloc[:, 0].astype(float)

# Create new time vector at 300 Hz
start_time = df["Time"].iloc[0]
end_time = df["Time"].iloc[-1]
new_time = np.arange(start_time, end_time, 1/300)  # 300 Hz sampling

# Interpolate all numerical columns to 300 Hz
interp_data = {"Time": new_time}
for col in df.columns:
    if col not in ["Time"]:  # Skip re-interpolating time
        interp_data[col] = np.interp(new_time, df["Time"], df[col])

# Create interpolated DataFrame
interp_df = pd.DataFrame(interp_data)

# Save to CSV
interp_df.to_csv("interpolated_300Hz_test_2", index=False)

print("Interpolation complete. Saved to 'interpolated_300Hz.csv'.")
