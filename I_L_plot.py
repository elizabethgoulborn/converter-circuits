# Function to plot waveform

def I_L_plot(t, mode, T, t_on, I_L, I_L_ave, t_off):

# t = Time to plot over (s)
# t_on = On period (s)
# t_off = Off period (s)
# t_zero = Period of zero inductor conductance (s) (used for DCM only)
# I_L = Inductor current (A)
# I_L_ave = Average inductor current (A)

	import math
	I_L_plot = [0] * len(t)

	# CCM Mode
	if mode == "CCM":
	
		# Populate CCM Plot
		for i in range(len(t)):
			
			# Regulate time period
			t_reg = t[i] % T
			
			# On period
			if t_reg < t_on:
				I_L_plot[i] = (I_L_ave - I_L/2) + (I_L/t_on) * t_reg
			
			# Off period
			else:
				I_L_plot[i] = (I_L_ave + I_L/2) - (I_L/(T - t_on)) * (t_reg - t_on)

	# DCM Mode	do this 
	elif mode == "DCM":
	
		# Populate DCM Plot
		for i in range(len(t)):
			
			# Regulate time period
			t_reg = t[i] % T
			
		
			# On period
			if t_reg < t_on:
				I_L_plot[i] = (I_L/t_on) * t_reg
			
			# Off period
			elif t_reg < t_on + t_off:
				I_L_plot[i] = I_L - (I_L/(t_off)) * (t_reg - t_on)
			
			# Zero period
			else:
				I_L_plot[i] = 0
	
	# Invalid Mode
	else:
		print("\nInvalid mode. Check inputs and try again.")
	
	
	return I_L_plot
