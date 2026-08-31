# converter_plot_it3: a function that uses numerical integration to
# simulate the transient and steady-state behaviour of a buck converter. 

# This design improves on a previous iteration to include more losses for a realistic 
# model and comments on characteristics of the circuit (e.g. voltage ripple ratio)

# Elizabeth Goulborn
# 08.26

def converter_plot_it3(circuit, V_in, f_switch, L, C, D, R, s_lim, I_L_i, V_C_i):
	
	# Define inputs
	
	# Converter type, circuit
	# Input voltage, V_in (V)
	# MOSFET switching frequency (Hz)
	# Inductance, L (H)   
	# Capacitance, C (F)
	# Duty Cycle, D
	# Load resistance, R (Ohms)
	# Sampling limit for simulation, s_lim
	# Initial inductor current, I_L_i (A)
	# Initial capacitor voltage, V_C_i (V)
	
	# Relevant imports
	
	import math
	import numpy as np
	import matplotlib.pyplot as plt
	from circuit_calc import circuit_calc

	# Confirm valid inputs to function call
	parameters = (V_in, f_switch, L, C, D, R)
	if all(p >= 0 for p in parameters) and D <= 1:
		pass
	else:
		raise ValueError("\n\nOne or more values invalid. Please try again:\n")
			
	if circuit not in ("Buck", "Boost", "Buck-boost"):
		raise ValueError("\nCircuit type not recognised. Recognised strings: Buck, Boost, Buck-boost")
	
	# a) SETTLING TIME: Time for response to decrease and remain within some range of its peak value
	
	# Initialise loop
	# Means
	mean_V_C = []
	mean_t = []
	
	# Starting points
	I_L_start = 0
	V_C_start = 0
	T_passed = 0
	
	# Return arrays
	all_I_L = []
	all_V_C = []
	all_t = []
	
	# Calculations                        
	T = 1/f_switch										                 # Time Period (s)
	t_on = D*T                                                           # On period (s)
	T_sampling = 100 * T                                                 # Sampling period
	T_sampling_max = 10000 * T                                           # Max sampling time
	t_points = 1000000                                                   # Time points to plot over
	t = np.linspace(T_passed, T_passed + T_sampling, t_points)           # Time plotting list
	h = t[1] - t[0]  

	# While loop
	transient = True
	while transient == True:
		
		# Define V_C and I_L start points
		V_C_i = V_C_start
		I_L_i = I_L_start

		# Grab some chunk of the time and voltage arrays
		section_V_C, section_I_L, section_t = circuit_calc(circuit, V_in, t, T, D, L, C, R, I_L_i, V_C_i)
		
		# Add calculated sections to all 
		all_V_C.append(section_V_C)
		all_I_L.append(section_I_L)
		all_t.append(section_t)
				
		# Save V_C and I_L position to begin next loop if needed
		V_C_start = section_V_C[-1]
		I_L_start = section_I_L[-1]		
					
		# Find the mean of this chunk and add to a new array
		mean_V_C.append(np.mean(section_V_C))
		mean_t.append(np.mean(section_t))
		
		# Increase time counter
		T_passed += T_sampling
		t = np.linspace(T_passed, T_passed + T_sampling, t_points)
		
		# Are values within tolerance?
		if len(mean_V_C) >= 2:
			lim_calc = abs(mean_V_C[-1] - mean_V_C[-2])/mean_V_C[-2]
		
			# If within tolerance return values
			if lim_calc <= s_lim:
				V_out = mean_V_C[-1]
				t_ss = mean_t[-1]
				transient = False
				break
		
		# Exit if sampling exceeds given maximum
		if T_passed >= T_sampling_max:
				
			# Indicate issue to user
			print("\nWarning: steady-state could not be reached. V_out and t_ss are taken as best estimates.")
			
			# Exit loop
			transient = False
			break
	
	# Concatenate arrays in the all_X lists to one array
	V_C = np.concatenate(all_V_C)
	I_L = np.concatenate(all_I_L)
	t = np.concatenate(all_t)
		 
	# b) RISE TIME: Time for response to increase from 10% to 90% of peak value
	
	# Determine peak value
	V_C_max = np.max(V_C)
	
	# Use min() method to locate the 10% and 90% to peak value marks
	V_C_10 = min(range(len(V_C)), key = lambda i:abs(V_C[i] - (V_C_max * 0.1)))
	V_C_90 = min(range(len(V_C)), key = lambda i:abs(V_C[i] - (V_C_max * 0.9)))
	
	# t_rise formula
	t_rise = t[V_C_90] - t[V_C_10]
	
	# c) MAXIMUM OVERSHOOT: (Max value - Steady-state value) / (Steady-state value) x 100 (%)
	max_overshoot = (V_C_max - V_out) / (V_out) * 100
	
	# d) STEADY-STATE VOLTAGE RIPPLE
	
	# Find steady-state min and max voltages
	sec_min = np.min(section_V_C)
	sec_max = np.max(section_V_C)
	
	# Voltage ripple calculation
	vrr = (sec_max-sec_min)/V_out * 100

	# e) EFFICIENCY: output power / input power x 100 (%)
	
	# Output power (V_out and R are known)
	P_out = V_out**2 / R

	# Input current (steady-state)
	
	if circuit in ("Buck", "Buck-boost"):
		# Buck: source only connected during t_on
		t_rel = (section_t % T) < t_on
		I_L_in_ave = D * np.mean(section_I_L[t_rel])
		
	else:
		# Boost and buck-boost: source connected continuously
		I_L_in_ave = np.mean(section_I_L)
	
	# Input power 
	P_in = V_in * I_L_in_ave
	
	# Efficiency calculation
	eff = P_out / P_in * 100
	
	# f) PLOTTING

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
	fig1.set_title(circuit + " Converter Inductor Current")
	fig2.set_title(circuit +  " Converter Capacitor Voltage")
	
	# Legends
	fig1.legend(loc = 'upper left')
	fig2.legend(loc = 'upper left')
	
	# Final plots 
	plt.show()
	print("Voltage Output: " + str(V_out) + "V")
	print("Rise time: " + str(t_rise) + "s")
	print("Time to steady-state: " + str(t_ss) + "s")
	print("Voltage Ripple Ratio: " + str(vrr) + "%")
	print("Max. overshoot: " + str(max_overshoot) + "%")
	print("Efficiency: " + str(eff) + "%")

