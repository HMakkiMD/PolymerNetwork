#!/usr/bin/env python
# coding: utf-8

# In[57]:


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from scipy.interpolate import LSQUnivariateSpline


# Function to calculate R-squared (goodness of fit)
def r_squared(y, y_fit):
    residuals = y - y_fit
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    return 1 - (ss_res / ss_tot)

ignored_files = []  # To keep track of files that have incorrect data
fitted_data = []    # To store fitted data for plotting

# Create a figure and axis for the plot
plt.figure(figsize=(10, 6))

for i in range(1, 2):
    #filename = f"W01_P{i:03d}"  # Pads numbers with leading zeros to make them 3 digits
    filename='results'
    try:
        # Open the file and read lines (assuming .txt as file extension, adjust if needed)
        #with open(f"all_txt_files/{filename}.txt", 'r') as f:
        with open(f"{filename}.txt", 'r') as f:
            msd = []
            temperature = []
            lines = f.readlines()
            
            for line in lines:
                try:
                    msd.append(float(line.split()[0]))  # Try to convert the first item to float
                except (ValueError, IndexError):
                    # If there's an error, ignore the entire file and break out of the loop
                    print(f"Ignoring {filename} due to bad data.")
                    ignored_files.append(filename)
                    break

            if len(msd) == len(lines):  # Only plot if all lines were successfully processed
                highest_temp = 620
                for j in range(len(msd)):
                    temperature.append(highest_temp - j * 20)

                # Reverse both temperature and msd to ensure they're in ascending order
                temperature = temperature[::-1]
                msd = msd[::-1]

                # Select the fitting range (example: between 140 and 500 degrees)
                msd_min, msd_max = 0, 2
                msd_filtered = np.array([t for t in msd if msd_min <= t <= msd_max])
                temp_filtered = np.array([temperature[k] for k in range(len(temperature)) if msd_min <= msd[k] <= msd_max])

                if len(temp_filtered) > 0:
                    # Refine initial guess based on data range
                    a_guess = np.min(msd_filtered)  # Smallest value in msd_filtered
                    b_guess = 0.5  # Example guess for the exponent

                    # Perform the power law fit with increased maxfev and initial guesses
                    try:
                        '''
                        popt, pcov = curve_fit(
                            power_law, temp_filtered, msd_filtered, 
                            p0=(a_guess, b_guess), 
                            maxfev=2000
                        )
                        '''
                        # Define knot positions (you can adjust the number and locations)
                        knots = np.linspace(temp_filtered.min(), temp_filtered.max(), 5)[1:-1]  # Choosing 3 internal knots

                        # Fit a cubic spline to the data
                        spline = LSQUnivariateSpline(temp_filtered, msd_filtered, t=knots, k=3)  # k=3 for cubic spline

                        # Generate more points to get a smooth curve
                        temp_smooth = np.linspace(temp_filtered.min(), temp_filtered.max(), 500)
                        msd_smooth = spline(temp_smooth)

                        # Calculate goodness of fit (R-squared)
                        #msd_predicted = exponential_fit(temp_filtered, *popt)
                        #r2 = r_squared(msd_filtered, msd_predicted)
                        msd_pred = spline(temp_filtered)
                        ss_res = np.sum((msd_filtered - msd_pred)**2)  # Residual sum of squares
                        ss_tot = np.sum((msd_filtered - np.mean(msd_filtered))**2)  # Total sum of squares
                        r2 = 1 - (ss_res / ss_tot)

                        # Plot original data
                        plt.plot(temp_filtered, msd_filtered,'o', label=filename)
                        
                        # Plot the fitted curve
                        plt.plot(temp_smooth, msd_smooth, '--', label=f'Fitted {filename}, R2 = {round(r2,4)}')

                        # Store fitted data
                        fitted_data.append((filename, temp_smooth, msd_smooth, r2))
                    
                    except RuntimeError as e:
                        print(f"Power law fit failed for {filename}: {e}")
                        ignored_files.append(filename)
                
    except FileNotFoundError:
        print(f"File {filename} not found.")
        ignored_files.append(filename)

# Position the legend outside the plot
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Files")

# Add axis labels
plt.xlabel('Temperature')
plt.ylabel('MSD')

# Adjust the layout to make space for the legend
plt.tight_layout(rect=[0, 0, 0.75, 1])  # Adjusts the plot size to leave space for the legend

#plt.show()

# Report ignored files and goodness of fit
if ignored_files:
    print(f"\nFiles ignored due to missing or incorrect data: {ignored_files}")
else:
    print("\nAll files processed successfully.")

'''
print("\nFitted data and goodness of fit (R-squared values):")
for data in fitted_data:
    print(f"{data[0]}: R² = {data[3]:.2f}")
'''
# You can save the fitted_data to a file if needed for further analysis

from scipy import interpolate

# Define the target MSD value
target_msd = 0.00884667469381180

# Open a file to write the results
with open('msd_temperature_results.txt', 'w') as file:
    # Loop over all fitted_data entries
    for data in fitted_data:
        polymer_name = data[0]  # Extract the polymer name
        temperatures = data[1]  # Extract the temperature array
        msd_values = data[2]    # Extract the MSD array
        
        # Create an interpolation function to find temperature at the target MSD
        interpolation_func = interpolate.interp1d(msd_values, temperatures, fill_value="extrapolate")
        
        # Find the temperature corresponding to the target MSD
        temperature = interpolation_func(target_msd)-273.15
        
        # Write the result to the file using the polymer name
        file.write(f"Tg for {polymer_name}: {temperature:.2f} °C\n")

print("Results have been written to 'msd_temperature_results.txt'")

print(temperature)
# In[49]:


r2


# In[44]:


temp_smooth


# In[ ]:




