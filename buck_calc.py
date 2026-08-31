# buck_calc is a function used to calculate the inductor current and 
# capacitor voltage transient and steady-state behaviour of a buck converter.

# Uses numerical integration rather than standard derivations.

# Elizabeth Goulborn
# 08.2026	
	
def buck_calc(V_in, t, T, D, L, C, R, I_L_i, V_C_i):
		
	# Define inputs
	
	# Input voltage, V_in (V)
	# Plotting time range, t (s) 
	# Time period, T (s)
	# Duty cycle, D
	# Inductance, L (H)
	# Capacitance, C (F)
	# Load resistance, R (Ohms)
	# Initial inductor current, I_L_i (A)
	# Initial capacitor voltage, V_C_i (V)
	
	# Library import
	import numpy as np

	# Confirm valid inputs to function call
	scalar_parameters = (V_in, T, D, L, C, R)
	if all(p >= 0 for p in scalar_parameters) and np.all(t >= 0) and D <= 1:
		pass
	else:
		raise ValueError("\n\nOne or more values invalid. Please try again:\n")

	# Calculations
	t_on = D*T                                                                # On period (s)
	
	# Initialise outputs
	I_L = [0] * len(t)                                                        # Initialise inductor current
	I_L[0] = I_L_i                                                            # Correct I_L initial point
	V_C = [0] * len(t)                                                        # Initialise capacitor voltage
	V_C[0] = V_C_i                                                            # Correct V_C initial point
	I_R = [0] * len(t)                                                        # Initialise load current
	
	# Stops V_in value from disappearing
	V_on = V_in        
	
	# Set h
	h = t[1]-t[0]               
	
	for k in range (0, len(t) - 1):
		
		# Puts t_reg in correct range
		t_reg = t[k] % T
		
		# MOSFET ON
		if 0 <= t_reg < t_on:
			V_on = V_in 
			switch_mode = "ON"
		
		# MOSFET OFF	
		else:
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
		
	# Return outputs	
	return(V_C, I_L, t)
			
		
