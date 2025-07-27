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
    csv_file_path = 'motor_thermal_test_4.csv'  # CSV with time and current
    csv_file_path2 = 'interpolated_300Hz_test_4.csv'
    current_column_name = 'knee[DephyActpack]:motor_current'
    df = pd.read_csv(csv_file_path)
    df2 = pd.read_csv(csv_file_path2)
    winding_temp_ItoT_col = 'knee[DephyActpack]:winding_temperature'  
    case_temp_ItoT_col= 'knee[DephyActpack]:case_temperature'
    time_col= 'OSL:timestamp'
    thermal_cam_degree_c_col = 'avg_cols_2_6'
    # thermal_cam_degree_c_col2 = 'Case temp.Max. degree c'
    winding_temp_ItoT = df[winding_temp_ItoT_col].values
    case_temp_ItoT = df[case_temp_ItoT_col].values
    time_t = df[time_col].values
    thermal_cam_degree_c= df2[thermal_cam_degree_c_col]
    # thermal_cam_degree_max= df2[thermal_cam_degree_c_col2]
    sampling_frequency_hz = 300
    ambient_temperature = 29.5

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

    # Plot results
    plt.figure(figsize=(12, 7))
    
    # Trim to match lengths for plotting
    min_len = min(len(time_t), len(thermal_cam_degree_c))
    
    plt.plot(time_t[:min_len], cases[:min_len], label='Housing temperature predicted by the thermal model', color='blue')
    plt.plot(time_t[:min_len], thermal_cam_degree_c[:min_len], label='Housing temperature as measured from the thermal camera', color='red')
    # plt.plot(time_t[:min_len], thermal_cam_degree_max[:min_len], label='Max Housing temperature as measured from the thermal camera', color='green')
    
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (°C)')
    plt.title('Motor Housing Thermal Plots')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 7))
    # plt.plot(times, windings, label='Winding Temperature', color='red')
    plt.plot(time_t, windings, label='Winding temperature predicted by the thermal model', color='red')
    plt.plot(time_t,winding_temp_ItoT, label = 'Winding temperature predicted by the defaut ItoT model', color='green')
    # plt.plot(time_t,)
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (°C)')
    plt.title('Motor Winding Thermal plots')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    print(f"\nFinal Case Temperature: {cases[-1]:.2f} °C")
    print (f" the max temp of the winding is {max(windings)}")
    print(f" the max temp of the winding from Ito2 model is {max(winding_temp_ItoT):.2f} °C")
    

