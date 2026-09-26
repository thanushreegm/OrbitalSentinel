# OrbitalSentinel 🌊🛰️

**Satellite-Based Oil Spill Detection and AIS Vessel Analysis**

[🚀 Live Demo](https://orbitalsent-hwkuh4kuhiyvhec7wpa3ny.streamlit.app/) · [💻 GitHub Repository](https://github.com/thanushreegm/OrbitalSentinel)

## Overview

OrbitalSentinel is a prototype dashboard for exploring oil-spill detection from satellite imagery and correlating detected events with Automatic Identification System (AIS) vessel data. It brings image analysis and vessel movement information together to support preliminary maritime investigation.

## Features

* **Satellite Image Analysis:** Analyze demo satellite imagery to identify potential oil-spill regions.
* **Spill Visualization:** Display detected regions and related visual outputs in the dashboard.
* **AIS Data Analysis:** Explore vessel position and movement records from AIS CSV data.
* **Spatial and Temporal Correlation:** Compare vessel locations and timestamps with a detected spill event.
* **Investigation Dashboard:** View the analysis and preliminary candidate results in one interface.

## Tech Stack

* Python
* Streamlit
* Pandas and NumPy
* OpenCV
* Folium

## Demo

The project includes synthetic satellite imagery and sample AIS data to demonstrate the workflow. Results are intended for prototyping and learning—not as proof that a vessel caused a spill.

## Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/thanushreegm/OrbitalSentinel.git
   cd OrbitalSentinel
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the dashboard:

   ```bash
   streamlit run dashboard.py
   ```

## Limitations

This is a prototype. The demo uses synthetic imagery and sample AIS records, and vessel matching is preliminary heuristic analysis. Real-world use would require validated satellite data, reliable georeferencing, robust detection validation, and further investigation.

## Author

**Thanushree G M**
B.E. Computer Science and Engineering (AI & ML) Student

[GitHub](https://github.com/thanushreegm)
