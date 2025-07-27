import numpy as np
from thermal import ThermalModel
import matplotlib.pyplot as plt
import pandas as pd


def run_thermal_simulation(csv_path, current_col, freq_hz, ambient_temp):
    dt = 1 / freq_hz

    df = pd.read_csv(csv_path)
    
    motor_currents_mA = df[current_col].values
    print(f"Successfully loaded {len(motor_currents_mA)} current data points.")

    # Initialize the Thermal Model
    thermal_model = ThermalModel(ambient=ambient_temp)
    print(f"Thermal model initialized with ambient temperature: {ambient_temp}°C")

    # Lists to store the simulated temperatures over time
    time_points = []
    winding_temperatures = []
    case_temperatures = []

    current_time = 0.0

    # Simulate the thermal model
    print("Starting thermal model simulation...")
    for i, current_mA in enumerate(motor_currents_mA):
        thermal_model.update(dt=dt, motor_current=current_mA)

        # Store current state
        time_points.append(current_time)
        winding_temperatures.append(thermal_model.T_w)
        case_temperatures.append(thermal_model.T_c)

        current_time += dt

        # Optional progress update every 10 seconds
        if (i + 1) % (freq_hz * 10) == 0:
            print(f"Simulating... {current_time:.1f}s processed. Current Case Temp: {thermal_model.T_c:.2f}°C")

    print("Simulation complete!")
    print(f"Final Winding Temperature: {thermal_model.T_w:.2f} °C")
    print(f"Final Case Temperature: {thermal_model.T_c:.2f} °C")

    return time_points, motor_currents_mA, winding_temperatures, case_temperatures


if __name__ == "__main__":
    csv_file_path = 'current_log_1hr_300Hz_1min0mA_10min1500mA.csv'  # CSV with time and current
    current_column_name = 'current (mA)'  
    sampling_frequency_hz = 300
    ambient_temperature = 21.0

    times, currents, windings, cases = run_thermal_simulation(
        csv_path=csv_file_path,
        current_col=current_column_name,
        freq_hz=sampling_frequency_hz,
        ambient_temp=ambient_temperature
    )

    # Save to CSV
    results_df = pd.DataFrame({
        'Time_s': times,
        'Motor_Current_mA': currents,
        'Winding_Temperature_C': windings,
        'Case_Temperature_C': cases
    })

    results_csv_path = 'thermal_model_simulation_results.csv'
    results_df.to_csv(results_csv_path, index=False)
    print(f"\nSimulation results saved to: {results_csv_path}")

    # Plot results
    plt.figure(figsize=(12, 7))
    plt.plot(times, windings, label='Winding Temperature', color='red')
    plt.plot(times, cases, label='Case Temperature', color='blue', linestyle='--')
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (°C)')
    plt.title('Motor Thermal Simulation: Winding and Case Temperatures')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    print(f"\nFinal Case Temperature: {cases[-1]:.2f} °C")
    print (f" the max temp of the winding is {max(windings)}")
    

