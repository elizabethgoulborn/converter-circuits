# converter-circuits
**Experimenting on Python to develop a simulator for converter circuits.**

## **Iteration 1: Buck converter inductor current calculator and plotter**

  **Objective:** Use standard derivations to plot the inductor current variation of a buck converter<br/>
  **Language used:** Python<br/>
  **Libraries used:** math, numpy, matplotlib<br/>
  **Main achievements:** plots match expected values, validated user input, used functions to make code cleaner<br/>
  **Aims for next iteration:** explore a better user input validator, manually integrate for volt-seconds and amp-seconds balance,
  use data to comment on system behaviour, utilise more functions, potentially integrate voltage ripple
  <br/><br/>
  I wanted to use my current knowledge of power electronic theory to make something practical while developing
  my coding skills.
  <br/><br/>

  Given user inputs for component values, the code plots inductor current against time after determining
  if the circuit is in CCM *(Continuous Conduction Mode)* or DCM *(Discontinuous Conduction Mode)*.<br/><br/>

  I tested this code with some values that corresponded to a CCM system and DCM system, seen below:<br/><br/>

### CCM:
<img align="left" width="400" height="300" src="https://github.com/user-attachments/assets/c6bac744-7ba1-47c0-a93c-5d52eef25662">
<img align="right" width="500" height="300" src="https://github.com/user-attachments/assets/71598053-4592-4216-b351-69f3c2f75f25">
<br clear="both"/><br/><br/>

### DCM: 
<img align="left" width="400" height="300" src="https://github.com/user-attachments/assets/26ad8b86-b15b-461b-88c4-0f4b20bc4d03">
<img align="right" width="500" height="300" src="https://github.com/user-attachments/assets/336d543a-6fe1-48f3-8ee8-c6d945c1e16c">
<br clear="both"/><br/><br/>

## **Iteration 2: Buck converter simulator: inductor current and capacitor voltage**

  **Objective:** Use techniques to create a more streamlined simulator, rather than a simple calculator<br/>
  **Language used:** Python<br/>
  **Libraries used:** math, numpy, matplotlib<br/>
  **Main achievements:** Introduced voltage ripple, switched standard derivations for numerical integration, moved to a switch-state reference over conduction mode, turned the simulator into a function itself<br/>
  **Aims for next iteration:** Integrate resistive and other losses, make the model reactive/ gear it for circuit design rather than commentary, apply concept to other types of converter.
  <br/><br/>

  **Key points on code design:** <br/>
- I modified the code (specifically the integrator for loop) to work off the MOSFET on/off state rather than the conduction mode to remove unnecessary code
- Euler's forward approximation was used for the numerical integration as, although step time must be chosen carefully, it has a good computational complexity and was simple to implement

  I tested this code with the same CCM and DCM systems from Iteration 1, seen below: <br/><br/>

<img align="left" width="450" height="300" src="https://github.com/user-attachments/assets/53477095-5a12-435f-91f6-3f5e5803e3f0">
<img align="right" width="450" height="300" src="https://github.com/user-attachments/assets/fb5faf39-d996-47e3-9579-a5efe367f29b">
<br clear="both"/><br/><br/>

**Observations from analysis:** See below for a scaled up view of the DCM system, where we can observe the capacitor charging and discharging, and the inductor current varying as it does with the Iteration 1 system. This code has possible applications in circuit design, and would be more widely applicable if it ran for boost and buck-boost converters in addition to the simple buck. This change will be a part of my implementation for the next iteration of this simulator to increase the versatility of the code.

<img width="2502" height="934" alt="Screenshot 2026-08-24 231054" src="https://github.com/user-attachments/assets/de2e32b4-b7a6-41c7-9a85-5b451569e1f7" />




