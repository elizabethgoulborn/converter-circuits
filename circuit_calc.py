# Given the type of converter circuit, run its corresponding calculation
# function.

# Elizabeth Goulborn
# 08.2026

# Imports
import numpy as np
from buck_calc import buck_calc
from boost_calc import boost_calc
from buck_boost_calc import buck_boost_calc

def circuit_calc(circuit, V_in, t, T, D, L, C, R, I_L_i, V_C_i):
	
	# Define inputs
	
	# Converter type, circuit
	# Input voltage, V_in (V)
	# Plotting time range, t (s) 
	# Duty Cycle, D
	# Inductance, L (H)   
	# Capacitance, C (F)
	# Load resistance, R (Ohms)
	# Initial inductor current, I_L_i (A)
	# Initial capacitor voltage, V_C_i (V)

	# Reject invalid input
	if circuit not in ("Buck", "Boost", "Buck-boost"):
		raise ValueError("\nCircuit type not recognised. Recognised converter names: Buck, Boost, Buck-boost.")
	
	# Buck 
	elif circuit == "Buck":
		V_C, I_L, t = buck_calc(V_in, t, T, D, L, C, R, I_L_i, V_C_i)
		
	# Boost
	elif circuit == "Boost":
		V_C, I_L, t = boost_calc(V_in, t, T, D, L, C, R, I_L_i, V_C_i)
		
	# Buck-boost
	else:
		V_C, I_L, t = buck_boost_calc(V_in, t, T, D, L, C, R, I_L_i, V_C_i)
		
	# Ensure V_C and I_L are np arrays to be compatible with later arrays
	V_C = np.array(V_C)
	I_L = np.array(I_L)	
	t = np.array(t)
	
	# Return outputs
	return V_C, I_L, t
