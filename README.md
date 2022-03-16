# Tactile-Visualization

Master's Research & Thesis on Haptic Design and Data Visualization.  
Explores the concept of using new "mediums" of Data Interpretation and Visualization in the form of Tactile Response.

<p align=center>
    <img src="showcase-example/User-Example.jpg" width=360px>
</p>

Showcase Demo
<p align=center>
    <img src="showcase-example/Demo-Example.gif">
</p>
<br>
<br>

---

# How it works
Large dataset is obtained online and stored into the sqlite .db for quick reading and analyzing. 
Data can then be sent and display in 2 modes:
1. Data Visualization via `matplotlib`
2. Haptic/Tactile Data Visualization (via Full Body Tactile Suit)


## User Interface (with Tactile Suit Visualizer for Debugging)
<p align=center>
    <img src="showcase-example/Tactile-Visualization_Overview.png" width=720px>
</p>
    
## Components of how it works
<p align=center>
    <img src="showcase-example/UML-Overview.png" width=720px>
</p>

Haptic Suit and software used in this demo:
- B-Haptic Tactoc Suit
- Haptic Player & Communication Code with Tactile Suit (forked from https://github.com/bhaptics/tact-python)
---


# Other Functionality (and Preliminary Testing)
Other Data display using Tactile Response is also being explored, such as "column-mode" and "dot-point" mode.

Under this format, data is being displayed similar to "audio" file in temporal pattern from right to left, with "intensity" of tactile vibration correlating to the % of the data.

## Column Mode Data representation using Tactile Suit:
<img src="showcase-example\Column-Mode.gif">

## Dot-Point Mode (Inital Testing) of parsing data and output with Intensity based on Highest % of data value within the set

<img src="showcase-example\Dot-Point-Mode.gif">

---

<!-- 
---
# Video - Full Run Demo (normal speed)
(Due to recording program running, this doesn't reflect the actual runtime speed of the data). -->


