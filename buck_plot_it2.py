# buck_plot: a function to give characteristic graphs for a buck converter
# with given inputs.
 
# Improves upon an initial plotting program that used standard derivations
# rather than numerical integration (this model does not assume 100%
# component efficiency)

# Introduces calculations for capacitor voltage ripple to begin a more
# comprehensive converter simulation.

# Elizabeth Goulborn
# 08.26

def buck_plot(V_in, f_switch, L, C, D, R):
	
	# Define inputs
	
	# Input voltage, V_in (V)
	# MOSFET switching frequency (Hz)
	# Inductance, L (H)   
	# Capacitance, C (F)
	# Duty Cycle, D
	# Load resistance, R (Ohms)
	
	# Relevant imports
	
	import math
	import numpy as np
	import matplotlib.pyplot as plt
	

	# Confirm valid inputs to function call

	validity = False
	while validity == False:

		parameters = (V_in, f_switch, L, C, D, R)
		if all(p >= 0 for p in parameters) and D <= 1:
			validity = True
		else:
			print("\n\nOne or more values invalid. Please try again:\n")
			return

	# Calculations
	w = 2*math.pi*f_switch                                                    # Angular frequency (rads^-1)
	T = 1/f_switch										                      # Time Period (s)
	t_on = D*T                                                                # On period (s)

	# Output characteristic graphs
	t_points = 100000	                                                      # Time points to plot over
	t = np.linspace(0, 100*T, t_points)                                       # Time plotting list
	I_L = [0] * len(t)                                                        # Initialise inductor current
	V_C = [0] * len(t)                                                        # Initialise capacitor voltage
	I_R = [0] * len(t)                                                        # Initialise load current
	
	# Numerical integration with Kirchoff's Voltage Law
	# Stops V_in value from disappearing
	V_on = V_in        
	# Set h
	h = t[1]-t[0]               
	
	for k in range (0, len(t) - 1):
		
		# Puts t_reg in correct range
		t_reg = t[k] % T
		
		# Determines if MOSFET is ON or OFF
		if 0 <= t_reg < t_on:
			V_on = V_in 
			switch_mode = "ON"
			
		else:
			# Indicates DCM mode
			V_on = 0 
			switch_mode = "OFF"
			
		# Euler's forward approximation (inductor current)
		div_I_L = (1/L)*(V_on - V_C[k])		
		I_L[k+1] = I_L[k] + div_I_L * h		
		
		# Load current calculation for capacitor voltage
		I_R[k] = V_C[k]/R
		
		# Euler's forward approximation (capacitor voltage)
		div_V_C = (1/C)*(I_L[k] - I_R[k])
		V_C[k+1] = V_C[k] + div_V_C * h
		
		
		# Account for DCM if needed
		if I_L[k+1] < 0 and switch_mode == "OFF":
			I_L[k+1] = 0

	# Plotting the output graphs as separate plots on one figure 
	fig = plt.figure()
	fig1 = fig.add_subplot(121)
	fig2 = fig.add_subplot(122)
	fig1.plot(t, I_L, '-', label = 'Inductor Current Variation (A)')
	fig2.plot(t, V_C, '-', label = 'Capacitor Voltage Ripple (V)')

	# Plot clarity 
	# Axes
	fig1.set_xlabel("Time (s)")
	fig2.set_xlabel("Time (s)")
	fig1.set_ylabel("Inductor Current (A)")
	fig2.set_ylabel("Capacitor Voltage (V)")
	
	# Titles
	fig1.set_title("Buck Converter Inductor Current")
	fig2.set_title("Buck Converter Capacitor Voltage")
	
	# Legends
	fig1.legend(loc = 'upper left')
	fig2.legend(loc = 'upper left')
	
	# Final plots 
	plt.show()



buck_plot(24, 100000, 15e-6, 47e-6, 0.4, 50)
