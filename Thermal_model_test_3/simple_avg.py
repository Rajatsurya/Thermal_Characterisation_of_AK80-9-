import pandas as pd

# Read the CSV file
print("Reading CSV file...")
df = pd.read_csv('test3_3amps_data.csv')

# Display initial information
print(f"Original shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# Remove rows with any missing values
df = df.replace('', pd.NA)
df_cleaned = df.dropna()

print(f"Cleaned shape: {df_cleaned.shape}")
print(f"Rows removed: {df.shape[0] - df_cleaned.shape[0]}")

# Calculate average of columns 2-6 (index 1-5)
cols_to_average = df_cleaned.columns[1:6]  # Columns 2-6
print(f"Calculating average of columns: {list(cols_to_average)}")

# Convert to numeric and calculate average
for col in cols_to_average:
    df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')

df_cleaned['avg_cols_2_6'] = df_cleaned[cols_to_average].mean(axis=1)

# Save the result
df_cleaned.to_csv('test3_3amps_data_with_avg.csv', index=False)
print("Data saved to 'test3_3amps_data_with_avg.csv'")

# Show sample
print("\nFirst few rows:")
print(df_cleaned.head()) 