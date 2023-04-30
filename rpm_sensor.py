# We're using the RPi.GPIO library to set up GPIO pins for an RPM sensor connected to a Raspberry
# Pi. We're setting up GPIO pin 18 as an input. The script sets up a data collection loop that runs indefinitely.
# Each iteration of the loop collects RPM data for 5 seconds using the sensor, and then calculates the RPM from the
# count of sensor pulses and prints the result.To run this script, you would need to save it as a Python file (e.g.
# "rpm_sensor.py") on the Raspberry Pi and then run it from the command line using the command python3 rpm_sensor.py.
import time
import RPi.GPIO 
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Set up GPIO pins for RPM sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)

# Set up data collection loop
while True:
    rpm_count = 0
    start_time = time.time()

    # Collect RPM data for 5 seconds
    while time.time() - start_time < 5:
        if GPIO.input(18) == GPIO.HIGH:
            rpm_count += 1

    # Calculate RPM from count and print result
    rpm = rpm_count / 5 * 60
    print(f"RPM: {rpm}")

# DATA COLLECTION
# Start data collection loop
#The data collection loop within the try block and handling the KeyboardInterrupt exception
#The user has the ability to press Ctrl+C at any point during the data collection to stop it
start_time = time.time()
try:
    while time.time() - start_time < duration:
        start_pulse = time.time()
        pulse_count = 0

        # Measure RPM for a fixed period of time
        while time.time() - start_pulse < 1 / sample_rate:
            if GPIO.input(18) == GPIO.HIGH:
                pulse_count += 1

        # Calculate RPM and store data
        rpm = pulse_count * sample_rate * 60 / 2
        rpm_data.append(rpm)
        time_data.append(time.time() - start_time)

except KeyboardInterrupt:
    print("Data collection interrupted by the user.")

finally:
    # Write RPM data to a CSV file
    with open('rpm_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'rpm'])
        for i in range(len(rpm_data)):
            writer.writerow([time_data[i], rpm_data[i]])

    # Clean up GPIO pins
    GPIO.cleanup()

    # Provide a summary report
    print("Data collection stopped. Summary report:")
    print(f"Total data points collected: {len(rpm_data)}")
    print(f"Duration of data collection: {time.time() - start_time} seconds")
    print(f"Average RPM: {sum(rpm_data) / len(rpm_data)}")

# DATA ANALYSIS
# Read in RPM data from database
df = pd.read_csv('rpm_data.csv')

# Calculate mean RPM for each driving mode
mean_rpm = df.groupby('mode')['rpm'].mean()

# Generate a bar chart of mean RPM by driving mode
plt.bar(mean_rpm.index, mean_rpm.values)
plt.title('Mean RPM by Driving Mode')
plt.xlabel('Driving Mode')
plt.ylabel('Mean RPM')
plt.show()

# Calculate fuel efficiency for each driving mode
fuel_efficiency = (df.groupby('mode')['speed'].mean() / mean_rpm) * 60

# Generate a bar chart of fuel efficiency by driving mode
plt.bar(fuel_efficiency.index, fuel_efficiency.values)
plt.title('Fuel Efficiency by Driving Mode')
plt.xlabel('Driving Mode')
plt.ylabel('Fuel Efficiency (MPG)')
plt.show()

# Identify instances where RPM is higher than necessary during highway driving
highway_rpm = df[df['speed'] >= 60]['rpm']
mean_highway_rpm = np.mean(highway_rpm)

if mean_highway_rpm > 3000:
    print('The engine is operating at a higher RPM than necessary during highway driving.')
else:
    print('The engine is operating efficiently during highway driving.')


# Make optimizations to the engine design to improve fuel efficiency
# For example, adjusting the fuel injection system, adjusting gear ratios, or improving aerodynamics

# OPTIMIZATION
# This function takes in an array of RPM data and an array of fuel consumption data, along with the type of change to
# be made (fuel injection rate, gear ratios, or aerodynamics) and the magnitude of the change to be made (as a
# percentage increase or decrease). The function then applies the specified changes to the data, simulating the
# effects of the changes on engine performance and fuel efficiency. Finally, the function returns the simulated RPM
# and fuel consumption data after the changes have been made. You could then call this function from within your main
# program, allowing the user to input the type and magnitude of the changes to be made, and displaying the simulated
# results.


# Define a function to simulate the effects of changes to the engine design
def simulate_engine_changes(rpm_data, fuel_data, change_type, change_amount):
    """
    Simulate changes to the engine design and evaluate their effects on performance and fuel efficiency.

    Parameters:
    rpm_data (np.ndarray): Array of RPM values.
    fuel_data (np.ndarray): Array of fuel consumption values.
    change_type (str): Type of change to be made ('fuel_injection', 'gear_ratios', or 'aerodynamics').
    change_amount (float): Magnitude of the change to be made (percentage increase or decrease).

    Returns:
    tuple: A tuple containing the simulated RPM and fuel consumption data after the engine changes have been made.
    """
    if change_type == 'fuel_injection':
        # Increase or decrease fuel injection rate by specified percentage
        new_fuel_data = fuel_data * (1 + change_amount / 100)
    elif change_type == 'gear_ratios':
        # Increase or decrease gear ratios by specified percentage
        new_rpm_data = rpm_data * (1 + change_amount / 100)
        new_fuel_data = fuel_data * (1 - change_amount / 100)
    elif change_type == 'aerodynamics':
        # Increase or decrease aerodynamic drag by specified percentage
        new_fuel_data = fuel_data * (1 - change_amount / 100)
    else:
        print("Invalid change type. Please enter 'fuel_injection', 'gear_ratios', or 'aerodynamics'.")
        return None

    # Return simulated RPM and fuel consumption data after changes have been made
    return (new_rpm_data, new_fuel_data)


# REPORTING
def generate_report(rpm_data, optimizations):
    # Create a PDF canvas
    report_name = "Engine Performance Report.pdf"
    c = canvas.Canvas(report_name, pagesize=letter)

    # Add a title to the report
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "Engine Performance Report")

    # Add a section for RPM data
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 700, "RPM Data")

    # Create a line chart of the RPM data using Matplotlib
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(rpm_data, linewidth=2)
    ax.set_xlabel("Time")
    ax.set_ylabel("RPM")
    ax.set_title("Engine RPM During Test Drive")

    # Save the chart as a PNG file
    chart_name = "RPM Chart.png"
    plt.savefig(chart_name, dpi=150)

    # Add the chart to the PDF report
    c.drawImage(chart_name, 50, 500, width=500, height=300)

    # Add a section for optimizations
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 450, "Optimizations")

    # Add a written analysis of the optimizations made
    c.setFont("Helvetica", 12)
    c.drawString(50, 400, "The following optimizations were made:")
    for i, optimization in enumerate(optimizations):
        c.drawString(70, 380 - (i * 20), f"{i + 1}. {optimization}")

    # Add a recommendation for further improvements
    c.setFont("Helvetica", 12)
    c.drawString(50, 250, "Based on the results of the analysis, we recommend the following further improvements:")
    c.drawString(70, 230, "- Upgrade the fuel injection system to reduce RPM during highway driving.")
    c.drawString(70, 210, "- Adjust the gear ratios to optimize fuel efficiency.")

    # Save the PDF report
    c.showPage()
    c.save()

    print(f"Report generated: {report_name}")
