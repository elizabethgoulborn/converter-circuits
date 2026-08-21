# Iteration 1: Basic buck converter calculator, outputs a plot of converter current
# Objective: Given some input parameters, output circuit characteristics using known derivations.
# Eliza Goulborn
# 08.2026


# Importing 

import math
import numpy as np
import matplotlib.pyplot as plt
from I_L_plot import I_L_plot

# Input parameters, confirming non negative values

validity = False
while validity == False:

	V_in = float(input("\nInput voltage (V): "))                              # V_in (V)
	f_switch = float(input("\nSwitching frequency (Hz): "))                   # MOSFET switching frequency (Hz)
	L = float(input("\nInductor inductance (H): "))                           # Inductance, L (H)   
	C = float(input("\nCapacitor capacitance (F): "))                         # Capacitance, C (F)
	D = float(input("\nDuty Cycle: "))                                        # Duty Cycle, D
	R = float(input("\nLoad resistance (Ohms): "))                            # Load resistance, R (Ohms)
	
	parameters = (V_in, f_switch, L, C, D, R)
	if all(p >= 0 for p in parameters) and D <= 1:
		validity = True
	else:
		print("\n\nOne or more values invalid. Please try again:\n")

# Calculations
w = 2*math.pi*f_switch                                                    # Angular frequency (rads^-1)
T = 1/f_switch										                      # Time Period (s)
t_on = D*T                                                                # On period (s)

# Determine conduction mode via boundary load and boundary duty cycle
R_b = 2*f_switch*L*(1/(1-D))                                              # Boundary Load (Ohms)
D_b = 1 - 2*f_switch*L*(1/R)                                              # Boundary Duty Cycle

# CCM only if both boundary conditions are met
if R<= R_b and D >= D_b:	
	
	# Inductor is continuously conducting (at no point is I_L = 0)
	mode = "CCM"
	t_off = (1-D)*T                                                       # Inductor current fall time (s)
	V_out = D*V_in                                                        # Output Voltage (V)
	I_L = (V_in - V_out)*t_on*(1/L)                                       # Change in pk-pk current (A)

else:
	
	# Inductor is not continuously conducting (at some point I_L = 0)
	mode = "DCM"
	V_out = (2*V_in)*(1/(1 + math.sqrt(1 + (8*f_switch*L)/(D**2 * R))))   # Output voltage (V)
	I_L = (V_in - V_out)*t_on*(1/L)                                       # pk current (A)
	t_off = (t_on/V_out)*(V_in - V_out)                                   # Inductor current fall time (s) (calculated with inductor volt-seconds balance)

# Output characteristic graphs

I_L_ave = V_out/R                                                         # Average output current (A)
t_points = 1000		                                                      # Time points to plot over
t = np.linspace(0, T*3, t_points)                                         # Time plotting list
graph = I_L_plot(t, mode, T, t_on, I_L, I_L_ave, t_off)

# Plotting the output graph for Inductor Current (A) vs Time (s)
plt.plot(t, graph, '-', label = 'Inductor Current Variation (A)')

# Plot average inductor current as reference
ave_line = [I_L_ave] * len(t)
plt.plot(t, ave_line, '--', label = 'Average Inductor Current (A)')

# Plot clarity 
plt.xlabel("Time (s)")
plt.ylabel("Inductor Current (A)")
plt.title("Buck Converter Inductor Current, Mode = " + mode)
plt.legend(loc = 'upper left')
plt.grid()
plt.show()


