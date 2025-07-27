import pandas as pd
import matplotlib.pyplot as plt
csv_file = "current_log_1hr_300Hz_1min0mA_10min1500mA.csv"

df = pd.read_csv(csv_file)

current = df["current (mA)"].values
time_s = df["time (s)"].values

plt.figure(figsize=(12, 7))
plt.plot(time_s, current, label='Current Profile', color='red')
plt.xlabel('Time (s)')
plt.ylabel('Current (mA)')
plt.title('Current vs Time')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

