import pandas as pd
import folium
from geopy.distance import geodesic


# ============================================================
# ORBITALSENTINEL - TASK 10
# Satellite Spill + AIS Vessel Correlation
# ============================================================


# ------------------------------------------------------------
# 1. READ DETECTED OIL SPILL
# ------------------------------------------------------------

spill_data = pd.read_csv("spill_detection.csv")

spill_latitude = float(spill_data.loc[0, "spill_latitude"])
spill_longitude = float(spill_data.loc[0, "spill_longitude"])
spill_time = str(spill_data.loc[0, "spill_time"])

print("\n========================================")
print("DETECTED OIL SPILL")
print("========================================")

print(f"Latitude  : {spill_latitude}")
print(f"Longitude : {spill_longitude}")
print(f"Time      : {spill_time}")


# ------------------------------------------------------------
# 2. READ AIS DATA
# ------------------------------------------------------------

ais_data = pd.read_csv("ais_data.csv")

print("\nVessels detected:")
print(ais_data["VesselID"].unique())


# ------------------------------------------------------------
# 3. CALCULATE DISTANCE FROM SPILL
# ------------------------------------------------------------

spill_location = (
    spill_latitude,
    spill_longitude
)

distances = []

for _, row in ais_data.iterrows():

    vessel_location = (
        row["Latitude"],
        row["Longitude"]
    )

    distance = geodesic(
        spill_location,
        vessel_location
    ).kilometers

    distances.append(distance)


ais_data["Distance_km"] = distances


# ------------------------------------------------------------
# 4. CALCULATE TIME DIFFERENCE
# ------------------------------------------------------------

ais_data["AIS_Time"] = pd.to_datetime(
    ais_data["Time"],
    format="%H:%M"
)

detected_time = pd.to_datetime(
    spill_time,
    format="%H:%M"
)

ais_data["Time_Difference_min"] = (
    ais_data["AIS_Time"] - detected_time
).dt.total_seconds().abs() / 60


# ------------------------------------------------------------
# 5. SUMMARIZE EACH VESSEL
# ------------------------------------------------------------

vessel_summary = (
    ais_data
    .groupby("VesselID")
    .agg(
        Minimum_Distance_km=("Distance_km", "min"),
        Minimum_Time_Difference_min=("Time_Difference_min", "min")
    )
    .reset_index()
)


# ------------------------------------------------------------
# 6. DISTANCE SCORE
# ------------------------------------------------------------

max_distance = vessel_summary["Minimum_Distance_km"].max()

if max_distance == 0:

    vessel_summary["Distance_Score"] = 100

else:

    vessel_summary["Distance_Score"] = (
        100
        * (
            1
            - vessel_summary["Minimum_Distance_km"]
            / max_distance
        )
    )


# ------------------------------------------------------------
# 7. TIME SCORE
# ------------------------------------------------------------

max_time = vessel_summary[
    "Minimum_Time_Difference_min"
].max()

if max_time == 0:

    vessel_summary["Time_Score"] = 100

else:

    vessel_summary["Time_Score"] = (
        100
        * (
            1
            - vessel_summary["Minimum_Time_Difference_min"]
            / max_time
        )
    )


# ------------------------------------------------------------
# 8. TRAJECTORY SCORE
# ------------------------------------------------------------

trajectory_scores = []

for vessel in vessel_summary["VesselID"]:

    vessel_points = ais_data[
        ais_data["VesselID"] == vessel
    ].sort_values("AIS_Time")

    first_distance = vessel_points.iloc[0]["Distance_km"]
    last_distance = vessel_points.iloc[-1]["Distance_km"]

    if last_distance < first_distance:

        trajectory_score = 100

    else:

        trajectory_score = 30

    trajectory_scores.append(
        trajectory_score
    )


vessel_summary["Trajectory_Score"] = trajectory_scores


# ------------------------------------------------------------
# 9. FINAL RESPONSIBILITY SCORE
# ------------------------------------------------------------

vessel_summary["Final_Score"] = (

    vessel_summary["Distance_Score"] * 0.50

    + vessel_summary["Time_Score"] * 0.30

    + vessel_summary["Trajectory_Score"] * 0.20
)


# ------------------------------------------------------------
# 10. RANK VESSELS
# ------------------------------------------------------------

vessel_summary = vessel_summary.sort_values(
    "Final_Score",
    ascending=False
).reset_index(drop=True)

vessel_summary["Rank"] = (
    vessel_summary.index + 1
)


# ------------------------------------------------------------
# 11. PRINT RESULTS
# ------------------------------------------------------------

print("\n========================================")
print("VESSEL RESPONSIBILITY RANKING")
print("========================================")

print(
    vessel_summary[
        [
            "Rank",
            "VesselID",
            "Minimum_Distance_km",
            "Minimum_Time_Difference_min",
            "Distance_Score",
            "Time_Score",
            "Trajectory_Score",
            "Final_Score"
        ]
    ].round(2)
)


# ------------------------------------------------------------
# 12. MOST LIKELY VESSEL
# ------------------------------------------------------------

top_vessel = vessel_summary.iloc[0]

print("\n========================================")
print("MOST LIKELY RESPONSIBLE VESSEL")
print("========================================")

print(
    f"Vessel ID       : {top_vessel['VesselID']}"
)

print(
    f"Final Score     : {top_vessel['Final_Score']:.2f}"
)

print(
    f"Minimum Distance: "
    f"{top_vessel['Minimum_Distance_km']:.2f} km"
)

print(
    f"Time Difference : "
    f"{top_vessel['Minimum_Time_Difference_min']:.2f} minutes"
)


# ------------------------------------------------------------
# 13. CREATE MAP
# ------------------------------------------------------------

m = folium.Map(
    location=[
        spill_latitude,
        spill_longitude
    ],
    zoom_start=9
)


# Oil spill marker

folium.Marker(
    [
        spill_latitude,
        spill_longitude
    ],
    popup=(
        "<b>DETECTED OIL SPILL</b><br>"
        f"Latitude: {spill_latitude}<br>"
        f"Longitude: {spill_longitude}<br>"
        f"Detection Time: {spill_time}"
    ),
    icon=folium.Icon(
        color="red",
        icon="warning-sign"
    )
).add_to(m)


# Approximate spill area

folium.Circle(
    [
        spill_latitude,
        spill_longitude
    ],
    radius=2000,
    color="red",
    fill=True,
    fill_opacity=0.2
).add_to(m)


# ------------------------------------------------------------
# 14. DRAW ALL VESSEL ROUTES
# ------------------------------------------------------------

for vessel in ais_data["VesselID"].unique():

    vessel_data = ais_data[
        ais_data["VesselID"] == vessel
    ].sort_values("AIS_Time")

    route = [
        [
            row["Latitude"],
            row["Longitude"]
        ]
        for _, row in vessel_data.iterrows()
    ]


    # Highlight top-ranked vessel

    if vessel == top_vessel["VesselID"]:

        weight = 6
        opacity = 1.0

    else:

        weight = 3
        opacity = 0.6


    folium.PolyLine(
        route,
        weight=weight,
        opacity=opacity,
        tooltip=f"{vessel} route"
    ).add_to(m)


    # AIS points

    for _, row in vessel_data.iterrows():

        folium.CircleMarker(
            [
                row["Latitude"],
                row["Longitude"]
            ],
            radius=4,
            popup=(
                f"<b>{vessel}</b><br>"
                f"Time: {row['Time']}<br>"
                f"Distance from spill: "
                f"{row['Distance_km']:.2f} km"
            )
        ).add_to(m)


# ------------------------------------------------------------
# 15. SAVE FINAL MAP
# ------------------------------------------------------------

m.save("orbital_sentinel_final_map.html")


print("\n========================================")
print("TASK 10 COMPLETED SUCCESSFULLY!")
print("========================================")

print(
    "\nFinal map: orbital_sentinel_final_map.html"
)