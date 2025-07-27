import pandas as pd
import matplotlib.pyplot as plt

csv_file = "interpolated_300Hz_test_2.csv"

df = pd.read_csv(csv_file)

time = df["Time"].values

temp_c = df["Temp_C"].values

temp_f = df["Temp_F"].values

plt.figure(figsize=(12, 7))
plt.plot(time, temp_c, label='Temperature (°C)', color='red')
plt.plot(time, temp_f, label='Temperature (°F)', color='blue', linestyle='--')
plt.xlabel('Time (s)')
plt.ylabel('Temperature')
plt.title('Temperature vs Time (Interpolated 300Hz)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show() 