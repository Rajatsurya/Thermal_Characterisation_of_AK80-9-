import pandas as pd

# Read the CSV file
print("Reading CSV file...")
df = pd.read_csv('test4_4amps.csv')

# Display initial information
print(f"Original shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# Remove rows with any missing values
df = df.replace('', pd.NA)
df_cleaned = df.dropna()

print(f"Cleaned shape: {df_cleaned.shape}")
print(f"Rows removed: {df.shape[0] - df_cleaned.shape[0]}")

# Save the cleaned data
df_cleaned.to_csv('test4_4amps_data_cleaned.csv', index=False)
print("Cleaned data saved to 'test3_3amps_data_cleaned.csv'")

# Show sample
print("\nFirst few rows of cleaned data:")
print(df_cleaned.head()) 