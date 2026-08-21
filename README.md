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





