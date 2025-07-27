import pandas as pd

# Load CSV
csv_file = "motor_thermal_test_2.csv"
time_column = "OSL:timestamp"
df = pd.read_csv(csv_file)

# Subtract the initial timestamp from all values
df[time_column] = df[time_column] - df[time_column].iloc[0]

# Save to a new CSV file
updated_csv_file = "test2_thermal_data.csv"
df.to_csv(updated_csv_file, index=False)

print(f"Updated file saved as {updated_csv_file}")
df2 = pd.read_csv("test2_thermal_data.csv")
print(len(df2))