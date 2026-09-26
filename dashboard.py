import os
from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import cv2
import folium
from PIL import Image
from geopy.distance import geodesic
from streamlit.components.v1 import html

# ============================================================
# ORBITALSENTINEL — MARITIME INVESTIGATION WORKSPACE
# ============================================================

st.set_page_config(
    page_title="OrbitalSentinel | Maritime Investigation",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PROFESSIONAL UI THEME
# ============================================================

st.markdown(
    """
<style>
/* ---------- APP ---------- */
.block-container {
    padding-top: 1.25rem;
    padding-bottom: 2.5rem;
    max-width: 1500px;
}

[data-testid="stAppViewContainer"] {
    background: #06131c;
}

[data-testid="stHeader"] {
    background: rgba(6,19,28,0.92);
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background: #071923;
    border-right: 1px solid rgba(71, 190, 232, 0.16);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.1rem;
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 2.35rem;
    text-align: left;
    border-radius: 9px;
    border: 1px solid transparent;
    background: transparent;
    color: #b9cbd5;
    font-weight: 600;
    margin: 0.08rem 0;
    padding-left: 0.75rem;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(51, 177, 221, 0.10);
    border-color: rgba(51, 177, 221, 0.20);
    color: #ffffff;
}

section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(90deg, rgba(20,126,181,0.85), rgba(18,89,139,0.65));
    border-color: rgba(61, 196, 241, 0.45);
    color: #ffffff;
    box-shadow: 0 5px 18px rgba(0, 120, 180, 0.18);
}

/* ---------- TEXT ---------- */
h1, h2, h3 {
    color: #eef8fc !important;
    font-weight: 750;
    letter-spacing: -0.025em;
}

p, label, .stMarkdown, .stCaption {
    color: #b8cbd5;
}

/* ---------- CARDS ---------- */
.os-card {
    background: linear-gradient(145deg, rgba(12,31,43,0.98), rgba(7,22,31,0.98));
    border: 1px solid rgba(92, 185, 219, 0.16);
    border-radius: 13px;
    padding: 1rem 1.05rem;
    min-height: 105px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.16);
}

.os-card-title {
    color: #83a2b0;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}

.os-card-value {
    color: #f1fbff;
    font-size: 1.45rem;
    font-weight: 750;
}

.os-card-sub {
    color: #78929f;
    font-size: 0.78rem;
    margin-top: 0.25rem;
}

.case-banner {
    background: linear-gradient(120deg, #0b2532, #09202c 55%, #0c2938);
    border: 1px solid rgba(65, 190, 235, 0.23);
    border-radius: 15px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}

.case-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: #f2fbff;
}

.case-subtitle {
    color: #8faab5;
    font-size: 0.83rem;
    margin-top: 0.15rem;
}

.section-kicker {
    color: #4fc7ee;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.13em;
    text-transform: uppercase;
}

.section-title {
    color: #edfaff;
    font-size: 1.35rem;
    font-weight: 800;
    margin-top: 0.15rem;
}

.status-pill {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    border-radius: 999px;
    background: rgba(35, 196, 130, 0.12);
    border: 1px solid rgba(35, 196, 130, 0.35);
    color: #65e0ad;
    font-size: 0.72rem;
    font-weight: 800;
}

.info-panel {
    background: rgba(10, 28, 39, 0.9);
    border: 1px solid rgba(85, 176, 211, 0.14);
    border-radius: 12px;
    padding: 0.95rem 1rem;
}

.workflow-step {
    background: #0b202c;
    border: 1px solid rgba(79, 178, 216, 0.14);
    border-radius: 11px;
    padding: 0.85rem;
    min-height: 92px;
}

.workflow-num {
    color: #49c7ef;
    font-size: 0.72rem;
    font-weight: 800;
}

.workflow-name {
    color: #e9f7fb;
    font-weight: 750;
    margin-top: 0.25rem;
}

.workflow-desc {
    color: #8199a5;
    font-size: 0.75rem;
    margin-top: 0.2rem;
}

.score-bar {
    height: 9px;
    border-radius: 999px;
    background: #102a37;
    overflow: hidden;
}

.score-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #149bd0, #45d4f4);
}

.alert-panel {
    background: linear-gradient(120deg, rgba(101,20,30,0.38), rgba(46,17,25,0.55));
    border: 1px solid rgba(255, 91, 103, 0.30);
    border-radius: 13px;
    padding: 1rem;
}

.disclaimer {
    background: rgba(128, 128, 128, 0.05);
    border: 1px solid rgba(128, 128, 128, 0.16);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    color: #879da8;
    font-size: 0.78rem;
}

hr {
    border-color: rgba(91, 176, 209, 0.12) !important;
}

[data-testid="stMetric"] {
    background: rgba(10, 29, 40, 0.85);
    border: 1px solid rgba(84, 181, 219, 0.14);
    border-radius: 12px;
    padding: 0.75rem;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(84, 181, 219, 0.14);
    border-radius: 10px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# HELPERS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


def local_file(name):
    return BASE_DIR / name


def fmt(value, digits=2):
    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return str(value)


def card(title, value, subtitle=""):
    st.markdown(
        f"""
        <div class="os-card">
            <div class="os-card-title">{title}</div>
            <div class="os-card-value">{value}</div>
            <div class="os-card-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(kicker, title, description=""):
    st.markdown(f'<div class="section-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if description:
        st.caption(description)


# ============================================================
# OIL-SPILL DETECTOR — EXISTING PROTOTYPE LOGIC
# ============================================================


def detect_uploaded_oil_spill(image_rgb):
    """
    Prototype computer-vision detector.
    It searches for a relatively dark connected region that can
    represent a possible oil spill.
    """
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    image_height, image_width = gray.shape
    total_pixels = image_height * image_width

    minimum_area = max(100, int(total_pixels * 0.001))
    maximum_area = int(total_pixels * 0.40)

    threshold_value = int(np.percentile(blurred, 20))
    threshold_value = max(15, min(threshold_value + 5, 110))

    mask = cv2.inRange(blurred, 0, threshold_value)

    kernel_open = np.ones((5, 5), np.uint8)
    kernel_close = np.ones((9, 9), np.uint8)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    valid_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < minimum_area or area > maximum_area:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        if w > image_width * 0.95 and h > image_height * 0.95:
            continue
        valid_contours.append(contour)

    if not valid_contours:
        adaptive_mask = cv2.adaptiveThreshold(
            blurred,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            31,
            5,
        )
        adaptive_mask = cv2.morphologyEx(adaptive_mask, cv2.MORPH_OPEN, kernel_open)
        adaptive_mask = cv2.morphologyEx(adaptive_mask, cv2.MORPH_CLOSE, kernel_close)

        contours, _ = cv2.findContours(
            adaptive_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        valid_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < minimum_area or area > maximum_area:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            if w > image_width * 0.95 and h > image_height * 0.95:
                continue
            valid_contours.append(contour)
        mask = adaptive_mask

    if not valid_contours:
        return None

    oil_spill_contour = max(valid_contours, key=cv2.contourArea)
    spill_area_pixels = float(cv2.contourArea(oil_spill_contour))
    x, y, width, height = cv2.boundingRect(oil_spill_contour)

    moments = cv2.moments(oil_spill_contour)
    if moments["m00"] != 0:
        centroid_x = int(moments["m10"] / moments["m00"])
        centroid_y = int(moments["m01"] / moments["m00"])
    else:
        centroid_x = int(x + width / 2)
        centroid_y = int(y + height / 2)

    final_mask = np.zeros_like(gray)
    cv2.drawContours(final_mask, [oil_spill_contour], -1, 255, -1)

    overlay = image_bgr.copy()
    cv2.drawContours(overlay, [oil_spill_contour], -1, (0, 0, 255), 3)
    cv2.circle(overlay, (centroid_x, centroid_y), 7, (0, 0, 255), -1)
    cv2.putText(
        overlay,
        "Detected Oil Spill",
        (x, max(25, y - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2,
    )

    overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)

    return {
        "area": spill_area_pixels,
        "width": int(width),
        "height": int(height),
        "centroid_x": centroid_x,
        "centroid_y": centroid_y,
        "mask": final_mask,
        "overlay": overlay_rgb,
        "image": image_rgb,
    }


# ============================================================
# SESSION STATE / NAVIGATION
# ============================================================

MODULES = [
    ("🏠", "Mission Dashboard"),
    ("📂", "Data Input"),
    ("🛰️", "Satellite Analysis"),
    ("🛢️", "Spill Characterization"),
    ("🚢", "AIS Analysis"),
    ("🎯", "Vessel Attribution"),
    ("🗺️", "Investigation Map"),
    ("📄", "Investigation Report"),
    ("⚠️", "Final Assessment"),
]

if "module" not in st.session_state:
    st.session_state.module = "Mission Dashboard"

if "data_mode" not in st.session_state:
    st.session_state.data_mode = "Demo Investigation"

if "case_name" not in st.session_state:
    st.session_state.case_name = "Arabian Sea Demonstration"

if "region" not in st.session_state:
    st.session_state.region = "Arabian Sea"


def navigate(module):
    st.session_state.module = module


# ============================================================
# SIDEBAR — PRODUCT NAVIGATION
# ============================================================

# Always initialize upload/input variables before the sidebar.
# Streamlit reruns the script from top to bottom, so this prevents
# NameError issues when switching between Demo and New Investigation.
uploaded_ais = None
uploaded_satellite = None
uploaded_time = "10:20"

with st.sidebar:
    st.markdown(
        """
        <div style="padding:0.15rem 0 0.7rem 0;">
            <div style="font-size:1.35rem;font-weight:850;color:#effbff;">🛰️ OrbitalSentinel</div>
            <div style="font-size:0.72rem;color:#7795a2;margin-top:0.18rem;letter-spacing:0.05em;">
                MARITIME INTELLIGENCE &amp; OIL-SPILL ATTRIBUTION
            </div>
        </div>
        <div class="status-pill">● PROTOTYPE ACTIVE</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption("CASE SETUP")


    data_mode = st.radio(
        "Investigation mode",
        ["Demo Investigation", "New Investigation"],
        index=0 if st.session_state.data_mode == "Demo Investigation" else 1,
        key="data_mode_selector",
        help="Use Demo Investigation for the built-in presentation case, or New Investigation for your own compatible data.",
    )

    if data_mode != st.session_state.data_mode:
        st.session_state.data_mode = data_mode
        if data_mode == "Demo Investigation":
            st.session_state.case_name = "Arabian Sea Demonstration"
            st.session_state.region = "Arabian Sea"
        else:
            st.session_state.case_name = ""
            st.session_state.region = ""
        st.rerun()

    if st.session_state.data_mode == "Demo Investigation":
        st.markdown(
            '<div class="info-panel" style="padding:.7rem .8rem;margin-bottom:.4rem;">'
            '<div style="color:#65e0ad;font-size:.72rem;font-weight:800;letter-spacing:.08em;">● DEMO DATA LOADED</div>'
            '<div style="color:#91a9b4;font-size:.76rem;margin-top:.25rem;">No upload required. Built-in AIS + satellite-like demo data are used.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        case_name_input = st.text_input(
            "Case Name",
            value=st.session_state.case_name,
            placeholder="e.g. Coastal Spill Investigation 01",
            key="new_case_name",
        )
        region_input = st.text_input(
            "Region / Sea",
            value=st.session_state.region,
            placeholder="e.g. Bay of Bengal",
            key="new_region",
        )
        st.session_state.case_name = case_name_input.strip()
        st.session_state.region = region_input.strip()

        uploaded_ais = st.file_uploader(
            "AIS CSV",
            type=["csv"],
            key="ais_upload",
            help="Required columns: VesselID, Time, Latitude, Longitude, SOG, COG",
        )

        uploaded_satellite = st.file_uploader(
            "Satellite / Sea Image",
            type=["png", "jpg", "jpeg", "tif", "tiff"],
            key="satellite_upload",
            help="Current prototype expects an image containing a relatively dark connected candidate spill region.",
        )

        st.caption("Upload an AIS CSV and a satellite/sea image. The current prototype analyzes the image directly; geographic spill coordinates are not assumed from the upload.")

        uploaded_time = st.text_input(
            "Detection Time (HH:MM)",
            value="10:20",
            key="detection_time",
        )

        st.caption("Compatible prototype input: image + AIS CSV. Real Sentinel-1/SAR products require additional preprocessing and georeferencing.")

    if st.session_state.data_mode == "Demo Investigation":
        uploaded_ais = None
        uploaded_satellite = None
        uploaded_time = "10:20"

    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption("DATA STATUS")
    if st.session_state.data_mode == "Demo Investigation":
        st.caption("✓ AIS dataset · ✓ satellite-like image · ✓ georeferenced demo case")
    else:
        st.caption("✓ User-provided case inputs. Bundled synthetic demo image has known demo bounds; other uploads need georeferencing for map-based attribution.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption("INVESTIGATION WORKSPACE")

    for icon, name in MODULES:
        if st.button(
            f"{icon}  {name}",
            key=f"nav_{name}",
            type="primary" if st.session_state.module == name else "secondary",
            use_container_width=True,
        ):
            navigate(name)
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption("WORKSPACE STATUS")
    if st.session_state.data_mode == "Demo Investigation":
        st.caption("✓ Demo case ready · No upload required")
    else:
        st.caption("✓ New case setup · User data mode")

# ============================================================
# LOAD / DETECT SPILL
# ============================================================

uploaded_detection_mask = None
uploaded_detection_overlay = None
uploaded_detection_image = None

# Always initialize spill georeferencing state before any investigation branch.
# Demo mode will replace these with the known demo coordinates below; a new
# uploaded image remains pixel-space unless reliable georeferencing is available.
spill_coordinates_available = False
spill_latitude = None
spill_longitude = None

if st.session_state.data_mode == "New Investigation" and uploaded_satellite is not None:
    try:
        uploaded_image = Image.open(uploaded_satellite).convert("RGB")
        satellite_image = np.array(uploaded_image)
    except Exception as exc:
        st.error(f"Unable to read uploaded satellite image: {exc}")
        st.stop()

    detection = detect_uploaded_oil_spill(satellite_image)

    if detection is None:
        st.error("No plausible oil-spill region was detected in the uploaded image.")
        st.info("Try an image where the possible spill appears as a relatively dark connected region over the sea.")
        st.stop()

    image_height, image_width = satellite_image.shape[:2]

    centroid_x = detection["centroid_x"]
    centroid_y = detection["centroid_y"]

    # Only apply the known geographic bounds to the bundled synthetic demo
    # image. Arbitrary user images are not georeferenced by this prototype.
    # This enables full attribution for the exact demo image without asking
    # the user to enter bounds, while avoiding invented coordinates otherwise.
    uploaded_image_name = Path(uploaded_satellite.name).name.lower()
    is_bundled_demo_image = uploaded_image_name == "synthetic_satellite.png"

    if is_bundled_demo_image:
        north, south, west, east = 13.20, 12.60, 74.50, 75.10
        spill_longitude = west + (centroid_x / max(1, image_width - 1)) * (east - west)
        spill_latitude = north - (centroid_y / max(1, image_height - 1)) * (north - south)
        spill_coordinates_available = True
    else:
        spill_latitude = None
        spill_longitude = None
        spill_coordinates_available = False

    spill_area_pixels = detection["area"]
    spill_width_pixels = detection["width"]
    spill_height_pixels = detection["height"]
    spill_coverage_percent = (spill_area_pixels / (image_width * image_height)) * 100

    if spill_area_pixels < 3000:
        severity = "SMALL"
    elif spill_area_pixels < 8000:
        severity = "MEDIUM"
    else:
        severity = "LARGE"

    spill_time = uploaded_time
    try:
        pd.to_datetime(spill_time, format="%H:%M")
    except Exception:
        st.error("Detection time must use HH:MM format, for example 10:20.")
        st.stop()

    uploaded_detection_mask = detection["mask"]
    uploaded_detection_overlay = detection["overlay"]
    uploaded_detection_image = detection["image"]

elif st.session_state.data_mode == "Demo Investigation":
    spill_path = local_file("spill_detection.csv")
    if not spill_path.exists():
        st.error("spill_detection.csv was not found. Please run task9.py first.")
        st.stop()

    spill_data = pd.read_csv(spill_path)
    if spill_data.empty:
        st.error("spill_detection.csv does not contain a spill record.")
        st.stop()

    required_spill_columns = [
        "spill_latitude",
        "spill_longitude",
        "spill_time",
        "spill_area_pixels",
        "spill_width_pixels",
        "spill_height_pixels",
        "spill_coverage_percent",
        "severity",
    ]
    missing_columns = [c for c in required_spill_columns if c not in spill_data.columns]
    if missing_columns:
        st.error("spill_detection.csv is missing: " + ", ".join(missing_columns))
        st.stop()

    spill_latitude = float(spill_data.loc[0, "spill_latitude"])
    spill_longitude = float(spill_data.loc[0, "spill_longitude"])
    spill_coordinates_available = True
    spill_time = str(spill_data.loc[0, "spill_time"])
    spill_area_pixels = float(spill_data.loc[0, "spill_area_pixels"])
    spill_width_pixels = int(spill_data.loc[0, "spill_width_pixels"])
    spill_height_pixels = int(spill_data.loc[0, "spill_height_pixels"])
    spill_coverage_percent = float(spill_data.loc[0, "spill_coverage_percent"])
    severity = str(spill_data.loc[0, "severity"])

else:
    st.markdown(
        '<div class="case-banner">'
        '<div class="case-subtitle">NEW INVESTIGATION</div>'
        '<div class="case-title">Waiting for case inputs</div>'
        '<div class="case-subtitle">Upload a satellite/sea image and an AIS CSV to begin analysis.</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.stop()

# ============================================================
# LOAD / VALIDATE AIS
# ============================================================

if st.session_state.data_mode == "New Investigation":
    if uploaded_ais is None:
        st.warning("Upload an AIS CSV in Case Setup to continue the new investigation.")
        st.stop()
    try:
        ais_data = pd.read_csv(uploaded_ais)
    except Exception as exc:
        st.error(f"Unable to read uploaded AIS CSV: {exc}")
        st.stop()
else:
    ais_path = local_file("ais_data.csv")
    if not ais_path.exists():
        st.error("ais_data.csv was not found. Restore the demo AIS file or switch to New Investigation.")
        st.stop()
    ais_data = pd.read_csv(ais_path)

required_ais_columns = ["VesselID", "Time", "Latitude", "Longitude", "SOG", "COG"]
missing_ais_columns = [c for c in required_ais_columns if c not in ais_data.columns]
if missing_ais_columns:
    st.error("AIS data is missing required columns: " + ", ".join(missing_ais_columns))
    st.stop()

ais_data = ais_data.copy().dropna(how="all").reset_index(drop=True)

for column in ["Latitude", "Longitude", "SOG", "COG"]:
    ais_data[column] = pd.to_numeric(ais_data[column], errors="coerce")

ais_data["Time"] = ais_data["Time"].astype(str)

missing_values = ais_data[required_ais_columns].isnull().sum().sum()
if missing_values > 0:
    ais_data = ais_data.dropna(subset=required_ais_columns).reset_index(drop=True)

invalid_coordinates = (
    (ais_data["Latitude"] < -90)
    | (ais_data["Latitude"] > 90)
    | (ais_data["Longitude"] < -180)
    | (ais_data["Longitude"] > 180)
)

if invalid_coordinates.any():
    ais_data = ais_data[~invalid_coordinates].reset_index(drop=True)

if ais_data.empty:
    st.error("No valid AIS records are available for analysis.")
    st.stop()

# ============================================================
# AIS CORRELATION / SCORING
# ============================================================

temporal_tie = False

try:
    ais_data["AIS_Time"] = pd.to_datetime(ais_data["Time"], format="%H:%M")
    detected_time = pd.to_datetime(spill_time, format="%H:%M")
except Exception:
    st.error("Invalid time format in AIS or spill data. Expected HH:MM.")
    st.stop()

ais_data["Time_Difference_min"] = (
    ais_data["AIS_Time"] - detected_time
).dt.total_seconds().abs() / 60

if spill_coordinates_available:
    spill_location = (spill_latitude, spill_longitude)
    ais_data["Distance_km"] = [
        geodesic(spill_location, (row["Latitude"], row["Longitude"])).kilometers
        for _, row in ais_data.iterrows()
    ]

    vessel_summary = (
        ais_data.groupby("VesselID")
        .agg(
            Minimum_Distance_km=("Distance_km", "min"),
            Minimum_Time_Difference_min=("Time_Difference_min", "min"),
        )
        .reset_index()
    )

    max_distance = vessel_summary["Minimum_Distance_km"].max()
    if max_distance == 0:
        vessel_summary["Distance_Score"] = 100.0
    else:
        vessel_summary["Distance_Score"] = 100 * (
            1 - vessel_summary["Minimum_Distance_km"] / max_distance
        )

    max_time = vessel_summary["Minimum_Time_Difference_min"].max()
    if max_time == 0:
        vessel_summary["Time_Score"] = 100.0
    else:
        vessel_summary["Time_Score"] = 100 * (
            1 - vessel_summary["Minimum_Time_Difference_min"] / max_time
        )

    trajectory_scores = []
    for vessel in vessel_summary["VesselID"]:
        vessel_points = ais_data[ais_data["VesselID"] == vessel].sort_values("AIS_Time")
        first_distance = float(vessel_points.iloc[0]["Distance_km"])
        last_distance = float(vessel_points.iloc[-1]["Distance_km"])
        minimum_distance = float(vessel_points["Distance_km"].min())
        endpoint_reference = max(first_distance, last_distance)

        if endpoint_reference <= 0:
            trajectory_score = 100.0
        else:
            approach_strength = 1 - (minimum_distance / endpoint_reference)
            trajectory_score = float(np.clip(approach_strength * 100, 0, 100))

        trajectory_scores.append(trajectory_score)

    vessel_summary["Trajectory_Score"] = trajectory_scores
    vessel_summary["Final_Score"] = (
        vessel_summary["Distance_Score"] * 0.50
        + vessel_summary["Time_Score"] * 0.30
        + vessel_summary["Trajectory_Score"] * 0.20
    )
    scoring_mode = "Full spatial + temporal + trajectory model"
else:
    # User-uploaded images are not assumed to have Arabian Sea bounds.
    # Without a geographic spill coordinate, distance and approach scores
    # cannot be calculated honestly. We therefore provide a clearly-labelled
    # preliminary temporal ranking instead of fabricating a location.
    ais_data["Distance_km"] = np.nan
    vessel_summary = (
        ais_data.groupby("VesselID")
        .agg(Minimum_Time_Difference_min=("Time_Difference_min", "min"))
        .reset_index()
    )

    time_values = vessel_summary["Minimum_Time_Difference_min"].astype(float)
    # Do not assign 100/100 to every vessel when all vessels are equally close
    # in time. Without a georeferenced spill, there is no valid evidence to
    # break that tie.
    if time_values.nunique(dropna=True) <= 1:
        vessel_summary["Time_Score"] = np.nan
        temporal_tie = True
    else:
        min_time = float(time_values.min())
        max_time = float(time_values.max())
        time_range = max_time - min_time
        vessel_summary["Time_Score"] = 100 * (
            1 - (time_values - min_time) / time_range
        )

    vessel_summary["Minimum_Distance_km"] = np.nan
    vessel_summary["Distance_Score"] = np.nan
    vessel_summary["Trajectory_Score"] = np.nan
    vessel_summary["Final_Score"] = vessel_summary["Time_Score"]
    scoring_mode = (
        "Preliminary temporal analysis — no geographic spill coordinates"
        if not temporal_tie
        else "Temporal tie — geographic spill coordinates required for attribution"
    )

vessel_summary["Final_Score"] = vessel_summary["Final_Score"].clip(0, 100)
if not spill_coordinates_available and temporal_tie:
    vessel_summary = vessel_summary.sort_values("VesselID").reset_index(drop=True)
    vessel_summary["Rank"] = "TIE"
else:
    vessel_summary = (
        vessel_summary.sort_values("Final_Score", ascending=False, na_position="last")
        .reset_index(drop=True)
    )
    vessel_summary["Rank"] = vessel_summary.index + 1

top_vessel = vessel_summary.iloc[0]

# Safe display values for cases where no unique attribution score exists.
top_score_display = "TIED" if pd.isna(top_vessel["Final_Score"]) else f"{top_vessel['Final_Score']:.2f}"
top_candidate_display = "No unique candidate" if (not spill_coordinates_available and temporal_tie) else str(top_vessel["VesselID"])

spill_lat_display = f"{spill_latitude:.5f}" if spill_coordinates_available else "Not available"
spill_lon_display = f"{spill_longitude:.5f}" if spill_coordinates_available else "Not available"
spill_location_display = (
    f"{spill_latitude:.5f}, {spill_longitude:.5f}"
    if spill_coordinates_available
    else "Not georeferenced"
)

# Prototype heuristic indicator — deliberately not a probability.
detection_confidence = int(np.clip(70 + min(spill_coverage_percent * 4, 25), 0, 95))

# ============================================================
# TOP APPLICATION HEADER
# ============================================================

st.markdown(
    f"""
    <div class="case-banner">
        <div style="display:flex;justify-content:space-between;gap:1rem;align-items:flex-start;">
            <div>
                <div class="case-subtitle">ACTIVE MARITIME INVESTIGATION · ORBITALSENTINEL</div>
                <div class="case-title">{st.session_state.case_name or "Untitled Investigation"}</div>
                <div class="case-subtitle">{st.session_state.region or "Region not specified"} · Satellite analysis + AIS trajectory correlation + explainable vessel ranking</div>
            </div>
            <div style="text-align:right;min-width:150px;">
                <div class="status-pill">● ACTIVE CASE</div>
                <div style="font-size:0.72rem;color:#6f8a97;margin-top:0.5rem;">{"DEMO DATA" if st.session_state.data_mode == "Demo Investigation" else "USER DATA"}</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# MODULE: MISSION DASHBOARD
# ============================================================

if st.session_state.module == "Mission Dashboard":
    section_header(
        "CASE OVERVIEW",
        "Mission Dashboard",
        "A compact operational view of the current spill investigation.",
    )

    cols = st.columns(6)
    values = [
        ("SPILL STATUS", "DETECTED", "Oil-spill region identified"),
        ("SEVERITY", severity, "Prototype classification"),
        ("SPILL AREA", f"{spill_area_pixels:.0f}", "pixels"),
        ("VESSELS", str(len(vessel_summary)), "candidates analyzed"),
        ("TOP CANDIDATE", top_candidate_display, "highest-ranked" if not temporal_tie else "no unique leader"),
        ("RELATIVE SCORE", top_score_display, "out of 100" if not temporal_tie else "not established"),
    ]
    for col, (title, value, sub) in zip(cols, values):
        with col:
            card(title, value, sub)

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.45, 1])
    with left:
        st.markdown("### Investigation Workflow")
        workflow = [
            ("01", "Satellite Analysis", "Detect a possible spill region"),
            ("02", "Spill Characterization", "Measure extent and severity"),
            ("03", "AIS Analysis", "Correlate vessel movement"),
            ("04", "Vessel Attribution", "Rank candidate vessels"),
        ]
        wcols = st.columns(4)
        for c, (num, name, desc) in zip(wcols, workflow):
            with c:
                st.markdown(
                    f'<div class="workflow-step"><div class="workflow-num">{num}</div>'
                    f'<div class="workflow-name">{name}</div><div class="workflow-desc">{desc}</div></div>',
                    unsafe_allow_html=True,
                )

        st.markdown("### Current Evidence Snapshot")
        e1, e2, e3 = st.columns(3)
        with e1:
            card("LOCATION", spill_lat_display, spill_lon_display)
        with e2:
            card("DETECTION TIME", spill_time, "AIS comparison reference")
        with e3:
            card("TOP VESSEL", str(top_vessel["VesselID"]), "relative ranking")

    with right:
        st.markdown("### Highest-Ranked Candidate")
        if spill_coordinates_available:
            candidate_label = "Relative Attribution Score"
            candidate_note = "Distance 50% · Time 30% · Trajectory 20%"
        else:
            candidate_label = "Preliminary Time Score"
            candidate_note = "Time proximity only · spatial evidence unavailable"

        st.markdown(
            f"""
            <div class="info-panel">
                <div style="color:#78a0ae;font-size:.72rem;letter-spacing:.09em;font-weight:800;">CANDIDATE #1</div>
                <div style="font-size:1.7rem;font-weight:850;color:#f0fbff;margin:.35rem 0;">{top_candidate_display}</div>
                <div style="font-size:.82rem;color:#8da5af;">{candidate_label}</div>
                <div style="font-size:2.3rem;font-weight:850;color:#4ed0f2;">{top_score_display}<span style="font-size:1rem;color:#7894a0;">{(" / 100" if not temporal_tie else "")}</span></div>
                <div style="font-size:.72rem;color:#78939e;margin-top:.35rem;">{candidate_note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("#### Evidence contribution")
        if spill_coordinates_available:
            evidence_rows = [
                ("Distance", top_vessel["Distance_Score"], "50%"),
                ("Time", top_vessel["Time_Score"], "30%"),
                ("Trajectory", top_vessel["Trajectory_Score"], "20%"),
            ]
        else:
            evidence_rows = [("Time", top_vessel["Time_Score"], "100%")]

        for label, score, weight in evidence_rows:
            st.write(f"**{label}** · {score:.1f}/100 · weight {weight}")
            st.markdown(
                f'<div class="score-bar"><div class="score-fill" style="width:{float(np.clip(score,0,100))}%;"></div></div>',
                unsafe_allow_html=True,
            )

        if not spill_coordinates_available:
            st.caption("Spatial and trajectory evidence will be enabled automatically when the uploaded image provides usable georeferencing.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="disclaimer">Prototype decision-support system. The relative score ranks candidates using the current heuristic model; it is not a probability and does not establish legal or factual responsibility.</div>',
        unsafe_allow_html=True,
    )

# ============================================================
# MODULE: DATA INPUT
# ============================================================

elif st.session_state.module == "Data Input":
    section_header(
        "CASE INPUTS",
        "Data Input",
        "Manage the AIS dataset and satellite image used by the investigation.",
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        card("AIS RECORDS", len(ais_data), "validated records")
    with c2:
        card("VESSELS", ais_data["VesselID"].nunique(), "unique vessel IDs")
    with c3:
        card("AIS FIELDS", len(ais_data.columns), "loaded columns")
    with c4:
        card("SATELLITE INPUT", "UPLOADED" if st.session_state.data_mode == "New Investigation" else "DEMO", "current image source")

    st.markdown("### AIS Dataset")
    st.dataframe(ais_data[required_ais_columns], use_container_width=True, hide_index=True)

    st.markdown("### Input Validation")
    v1, v2 = st.columns(2)
    with v1:
        st.success("AIS schema validated")
        if missing_values > 0:
            st.warning(f"Removed {missing_values} missing AIS values during cleaning.")
        else:
            st.info("No missing values detected in required AIS fields.")
    with v2:
        if invalid_coordinates.any():
            st.warning("Invalid coordinate rows were removed during validation.")
        else:
            st.success("AIS latitude/longitude ranges are valid.")

    st.markdown("### Spill Input")
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        card("LATITUDE", spill_lat_display, "estimated spill centroid" if spill_coordinates_available else "geographic position unavailable")
    with s2:
        card("LONGITUDE", spill_lon_display, "estimated spill centroid" if spill_coordinates_available else "geographic position unavailable")
    with s3:
        card("TIME", spill_time, "detection reference")
    with s4:
        card("SOURCE", "USER IMAGE" if st.session_state.data_mode == "New Investigation" else "DEMO CSV", "spill result source")

# ============================================================
# MODULE: SATELLITE ANALYSIS
# ============================================================

elif st.session_state.module == "Satellite Analysis":
    section_header(
        "EARTH OBSERVATION",
        "Satellite Analysis",
        "Prototype computer-vision processing for identifying a possible oil-spill region.",
    )

    st.info(
        "Prototype Mode: the demonstration can use satellite-like/synthetic imagery. "
        "Real deployment would use validated satellite datasets and a trained detection model."
    )

    if uploaded_detection_image is not None:
        img1, img2 = st.columns(2)
        with img1:
            st.markdown("### Input Image")
            st.image(uploaded_detection_image, use_container_width=True)
        with img2:
            st.markdown("### Detected Region")
            st.image(uploaded_detection_overlay, use_container_width=True)
    else:
        img1, img2 = st.columns(2)
        synthetic_path = local_file("synthetic_satellite.png")
        detection_path = local_file("oil_spill_detection.png")
        with img1:
            st.markdown("### Demonstration Satellite Image")
            if synthetic_path.exists():
                st.image(str(synthetic_path), use_container_width=True)
            else:
                st.warning("synthetic_satellite.png not found.")
        with img2:
            st.markdown("### Detection Output")
            if detection_path.exists():
                st.image(str(detection_path), use_container_width=True)
            else:
                st.warning("oil_spill_detection.png not found.")

    st.markdown("### Detection Output")
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        card("CENTROID LAT", spill_lat_display, "estimated coordinate" if spill_coordinates_available else "pixel-space result")
    with d2:
        card("CENTROID LON", spill_lon_display, "estimated coordinate" if spill_coordinates_available else "pixel-space result")
    with d3:
        card("AREA", f"{spill_area_pixels:.0f}", "detected pixels")
    with d4:
        card("COVERAGE", f"{spill_coverage_percent:.2f}%", "of input image")

    st.markdown("### Detection Mask")
    if uploaded_detection_mask is not None:
        st.image(uploaded_detection_mask, clamp=True, use_container_width=True)
    else:
        mask_path = local_file("oil_spill_mask.png")
        if mask_path.exists():
            st.image(str(mask_path), use_container_width=True)
        else:
            st.warning("oil_spill_mask.png not found.")

# ============================================================
# MODULE: SPILL CHARACTERIZATION
# ============================================================

elif st.session_state.module == "Spill Characterization":
    section_header(
        "SPILL PROFILE",
        "Spill Characterization",
        "Quantify the detected region before correlating it with vessel movement.",
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        card("AREA", f"{spill_area_pixels:.2f}", "pixels")
    with c2:
        card("WIDTH", spill_width_pixels, "pixels")
    with c3:
        card("HEIGHT", spill_height_pixels, "pixels")
    with c4:
        card("COVERAGE", f"{spill_coverage_percent:.2f}%", "image coverage")

    st.markdown("### Classification")
    if severity == "LARGE":
        st.error("🚨 LARGE spill classification")
    elif severity == "MEDIUM":
        st.warning("⚠️ MEDIUM spill classification")
    else:
        st.info("ℹ️ SMALL spill classification")

    p1, p2 = st.columns(2)
    with p1:
        st.markdown("#### Estimated Location")
        st.metric("Latitude", spill_lat_display)
        st.metric("Longitude", spill_lon_display)
    with p2:
        st.markdown("#### Detection Reference")
        st.metric("Time", spill_time)
        st.metric("Prototype Detection Indicator", f"{detection_confidence}%")
        st.caption("Heuristic indicator only; not a trained ML probability.")

# ============================================================
# MODULE: AIS ANALYSIS
# ============================================================

elif st.session_state.module == "AIS Analysis":
    section_header(
        "VESSEL TRAFFIC",
        "AIS Analysis",
        "Inspect vessel positions and their spatial/temporal relationship to the detected spill.",
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        card("VESSELS", ais_data["VesselID"].nunique(), "unique tracks")
    with c2:
        card("AIS EVENTS", len(ais_data), "records")
    with c3:
        card("CLOSEST DISTANCE", f"{ais_data['Distance_km'].min():.2f}" if spill_coordinates_available else "N/A", "km" if spill_coordinates_available else "spill not georeferenced")
    with c4:
        card("CLOSEST TIME", f"{ais_data['Time_Difference_min'].min():.0f}", "minutes")

    st.markdown("### Vessel Overview")
    display = vessel_summary[
        [
            "Rank",
            "VesselID",
            "Minimum_Distance_km",
            "Minimum_Time_Difference_min",
            "Distance_Score",
            "Time_Score",
            "Trajectory_Score",
            "Final_Score",
        ]
    ].copy()
    display.columns = [
        "Rank",
        "Vessel",
        "Min Distance (km)",
        "Min Time Difference (min)",
        "Distance Score",
        "Time Score",
        "Trajectory Score",
        "Relative Score",
    ]
    st.dataframe(display.round(2), use_container_width=True, hide_index=True)

    st.markdown("### AIS Event Timeline")
    # Sort BEFORE selecting display columns because AIS_Time is an
    # internal datetime column and is not included in the displayed table.
    timeline = ais_data.sort_values(
        ["AIS_Time", "VesselID"]
    )[
        ["VesselID", "Time", "Latitude", "Longitude", "SOG", "COG", "Distance_km", "Time_Difference_min"]
    ].copy()
    st.dataframe(
        timeline.rename(
            columns={
                "VesselID": "Vessel",
                "Time": "AIS Time",
                "Distance_km": "Distance to Spill (km)",
                "Time_Difference_min": "Time Difference (min)",
            }
        ).round(2),
        use_container_width=True,
        hide_index=True,
    )

# ============================================================
# MODULE: VESSEL ATTRIBUTION
# ============================================================

elif st.session_state.module == "Vessel Attribution":
    section_header(
        "EVIDENCE FUSION",
        "Vessel Attribution",
        "Rank candidate vessels using explainable evidence available for the current case.",
    )

    if spill_coordinates_available:
        attr_label = "Relative Attribution Score"
        attr_note = "Full spatial + temporal + trajectory model"
    else:
        attr_label = "Preliminary Time Score"
        attr_note = "Time proximity only — not full attribution"

    st.markdown(
        f"""
        <div class="info-panel">
            <div style="color:#7796a2;font-size:.72rem;font-weight:800;letter-spacing:.09em;">HIGHEST-RANKED CANDIDATE</div>
            <div style="font-size:2rem;font-weight:850;color:#f2fbff;margin:.3rem 0;">{top_candidate_display}</div>
            <div style="color:#8ca6b1;font-size:.8rem;">{attr_label}</div>
            <div style="font-size:2.8rem;font-weight:850;color:#4fd1f2;">{top_score_display}<span style="font-size:1rem;color:#78939e;">{(" / 100" if not temporal_tie else "")}</span></div>
            <div style="color:#78939e;font-size:.72rem;margin-top:.35rem;">{attr_note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Candidate Ranking")
    rank_cols = st.columns([0.55, 1.4, 1, 1, 1, 1])
    score_header = "RELATIVE SCORE" if spill_coordinates_available else "PRELIMINARY SCORE"
    for c, title in zip(rank_cols, ["#", "VESSEL", "DISTANCE", "TIME", "TRAJECTORY", score_header]):
        c.markdown(f"**{title}**")

    for _, row in vessel_summary.iterrows():
        cols = st.columns([0.55, 1.4, 1, 1, 1, 1])
        cols[0].write(f"**{row['Rank']}**")
        cols[1].write(f"**{row['VesselID']}**")
        cols[2].write(f"{row['Distance_Score']:.1f}" if pd.notna(row['Distance_Score']) else "N/A")
        cols[3].write(f"{row['Time_Score']:.1f}" if pd.notna(row['Time_Score']) else "TIE")
        cols[4].write(f"{row['Trajectory_Score']:.1f}" if pd.notna(row['Trajectory_Score']) else "N/A")
        cols[5].write(f"**{row['Final_Score']:.2f}**" if pd.notna(row['Final_Score']) else "**TIE**")

    st.markdown("### Why was the top candidate ranked highest?")
    reasons = []
    if spill_coordinates_available:
        if top_vessel["Minimum_Distance_km"] <= vessel_summary["Minimum_Distance_km"].median():
            reasons.append("Strong spatial relationship with the detected spill region.")
        if top_vessel["Trajectory_Score"] >= 50:
            reasons.append("The vessel track shows meaningful approach consistency.")
    if top_vessel["Minimum_Time_Difference_min"] <= vessel_summary["Minimum_Time_Difference_min"].median():
        reasons.append("Strong temporal proximity to the spill detection time.")
    if not spill_coordinates_available:
        if vessel_summary["Time_Score"].nunique(dropna=True) <= 1:
            reasons.append("All available vessels have the same temporal proximity to the detection time; no unique time-based leader can be established.")
        reasons.append("Geographic spill coordinates are unavailable, so this is a preliminary time-based ranking only.")
    elif not reasons:
        reasons.append("The combined weighted evidence produced the highest relative score.")

    for reason in reasons:
        st.write("✓ " + reason)

    st.markdown("### Scoring Model")
    if spill_coordinates_available:
        st.code(
            "Relative Attribution Score = "
            "(Distance Score × 50%) + "
            "(Time Score × 30%) + "
            "(Trajectory Score × 20%)"
        )
    else:
        st.code("Preliminary Candidate Score = Time Proximity Score × 100%")

    st.caption(
        "The score is a relative decision-support ranking. It is not a probability and does not establish legal or factual responsibility."
    )

# ============================================================
# MODULE: INVESTIGATION MAP
# ============================================================

elif st.session_state.module == "Investigation Map":
    section_header(
        "GEOSPATIAL INVESTIGATION",
        "Investigation Map",
        "Visualize the detected spill and all available AIS vessel trajectories in one workspace.",
    )

    if spill_coordinates_available:
        map_center = [spill_latitude, spill_longitude]
    else:
        map_center = [ais_data["Latitude"].mean(), ais_data["Longitude"].mean()]

    m = folium.Map(location=map_center, zoom_start=9, control_scale=True)

    if spill_coordinates_available:
        folium.Marker(
            [spill_latitude, spill_longitude],
            popup=(
                f"<b>Detected Oil Spill</b><br>"
                f"Latitude: {spill_latitude:.5f}<br>"
                f"Longitude: {spill_longitude:.5f}<br>"
                f"Time: {spill_time}<br>"
                f"Severity: {severity}"
            ),
            tooltip="Detected Oil Spill",
            icon=folium.Icon(color="red", icon="warning-sign"),
        ).add_to(m)

        folium.Circle(
            [spill_latitude, spill_longitude],
            radius=2000,
            popup="Prototype 2 km investigation radius",
            color="red",
            fill=True,
            fill_opacity=0.16,
        ).add_to(m)
    else:
        folium.Marker(
            map_center,
            popup="AIS map center — spill image is not georeferenced",
            tooltip="AIS Map Center",
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(m)
        st.info("The uploaded image is not georeferenced in this prototype, so the spill cannot be placed at a real-world map coordinate. AIS tracks are shown independently without inventing a spill location.")

    for vessel in ais_data["VesselID"].unique():
        vessel_data = ais_data[ais_data["VesselID"] == vessel].sort_values("AIS_Time")
        route = [[row["Latitude"], row["Longitude"]] for _, row in vessel_data.iterrows()]

        is_top = vessel == top_vessel["VesselID"]
        folium.PolyLine(
            route,
            weight=6 if is_top else 3,
            opacity=0.88 if is_top else 0.58,
            tooltip=(
                f"🏆 {vessel} — Highest-Ranked Candidate"
                if is_top
                else f"{vessel} route"
            ),
        ).add_to(m)

        for _, row in vessel_data.iterrows():
            folium.CircleMarker(
                [row["Latitude"], row["Longitude"]],
                radius=5 if is_top else 4,
                popup=(
                    f"<b>{vessel}</b><br>"
                    f"Time: {row['Time']}<br>"
                    f"Distance to spill: {row['Distance_km']:.2f} km" if spill_coordinates_available else "Distance to spill: unavailable"
                ),
            ).add_to(m)

    html(m._repr_html_(), height=650)

    st.markdown("### Map Evidence")
    a, b, c = st.columns(3)
    with a:
        card("SPILL", spill_location_display, "detected centroid" if spill_coordinates_available else "image not georeferenced")
    with b:
        card("VESSEL TRACKS", ais_data["VesselID"].nunique(), "displayed")
    with c:
        card("HIGHLIGHTED", str(top_vessel["VesselID"]), "top candidate")

# ============================================================
# MODULE: INVESTIGATION REPORT
# ============================================================

elif st.session_state.module == "Investigation Report":
    section_header(
        "CASE REPORT",
        "Investigation Report",
        "A concise evidence summary generated from the current prototype analysis.",
    )

    st.markdown(
        f"""
        <div class="info-panel">
            <div style="font-size:.72rem;color:#73909c;font-weight:800;letter-spacing:.1em;">ORBITALSENTINEL CASE SUMMARY</div>
            <div style="font-size:1.45rem;color:#f1fbff;font-weight:800;margin:.35rem 0;">{st.session_state.case_name or "Untitled Investigation"}</div>
            <div style="color:#8ba5b0;font-size:.82rem;">Region: {st.session_state.region or "Not specified"} · Source: {"built-in demo data" if st.session_state.data_mode == "Demo Investigation" else "user-provided inputs"}.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Incident Summary")
    summary = pd.DataFrame(
        {
            "Field": [
                "Spill location",
                "Detection time",
                "Severity",
                "Estimated area",
                "Spill coverage",
                "Vessels analyzed",
                "Highest-ranked candidate",
                "Relative attribution score",
            ],
            "Result": [
                spill_location_display,
                spill_time,
                severity,
                f"{spill_area_pixels:.2f} pixels",
                f"{spill_coverage_percent:.2f}%",
                str(len(vessel_summary)),
                top_candidate_display,
                (f"{top_vessel['Final_Score']:.2f}/100"
                 if pd.notna(top_vessel["Final_Score"]) else "Tie — insufficient evidence"),
            ],
        }
    )
    st.table(summary)

    st.markdown("### Evidence Used")
    e1, e2 = st.columns(2)
    with e1:
        st.write("🛰️ Satellite-like image / spill region")
        st.write("📍 Estimated spill coordinates" if spill_coordinates_available else "📍 Spill coordinates not available from image")
        st.write("📐 Spill area, dimensions and coverage")
        st.write("⚠️ Prototype severity classification")
    with e2:
        st.write("🚢 AIS vessel positions")
        st.write("📏 Vessel-to-spill distance" if spill_coordinates_available else "📏 Vessel-to-spill distance not calculated")
        st.write("⏱️ Time correlation")
        st.write("🛳️ Trajectory consistency" if spill_coordinates_available else "🛳️ Trajectory consistency not calculated")

    st.markdown("### Attribution Formula")
    if spill_coordinates_available:
        st.code(
            "Relative Attribution Score = "
            "(Distance × 0.50) + (Time × 0.30) + (Trajectory × 0.20)"
        )
    else:
        st.code("Preliminary Candidate Score = Time Proximity Score × 100%")

    st.markdown(
        '<div class="disclaimer">This report is generated by a prototype decision-support model. Candidate ranking requires validation with real satellite imagery, complete AIS records and additional evidence before operational use.</div>',
        unsafe_allow_html=True,
    )

# ============================================================
# MODULE: FINAL ASSESSMENT
# ============================================================

elif st.session_state.module == "Final Assessment":
    section_header(
        "OPERATIONAL ASSESSMENT",
        "Final Assessment",
        "Present the current evidence without overstating what the prototype can prove.",
    )

    if severity == "LARGE":
        st.markdown(
            f'<div class="alert-panel"><div style="color:#ff7580;font-size:.72rem;font-weight:800;letter-spacing:.1em;">HIGH ALERT</div>'
            f'<div style="color:#fff2f3;font-size:1.35rem;font-weight:800;margin-top:.25rem;">Large oil-spill region detected</div>'
            f'<div style="color:#b89499;font-size:.8rem;margin-top:.25rem;">Immediate investigation recommended within the prototype workflow.</div></div>',
            unsafe_allow_html=True,
        )
    elif severity == "MEDIUM":
        st.warning("Medium oil-spill region detected. Investigation recommended.")
    else:
        st.info("Small oil-spill region detected. Continue evidence review.")

    st.markdown("### Highest-Ranked Candidate Vessel")
    c1, c2, c3 = st.columns(3)
    with c1:
        card("CANDIDATE", top_candidate_display, "rank #1" if not temporal_tie else "no unique leader")
    with c2:
        card(
            "RELATIVE SCORE" if spill_coordinates_available else "PRELIMINARY TIME SCORE",
            top_score_display,
            "full attribution model" if spill_coordinates_available else ("time proximity only" if not temporal_tie else "no unique time-based leader"),
        )
    with c3:
        card("MIN DISTANCE", f"{top_vessel['Minimum_Distance_km']:.2f} km" if spill_coordinates_available else "N/A", "closest AIS position" if spill_coordinates_available else "spill not georeferenced")

    st.markdown("### Evidence Assessment")
    if spill_coordinates_available:
        assessment = pd.DataFrame(
            {
                "Evidence": ["Distance", "Time", "Trajectory"],
                "Score": [
                    top_vessel["Distance_Score"],
                    top_vessel["Time_Score"],
                    top_vessel["Trajectory_Score"],
                ],
                "Weight": ["50%", "30%", "20%"],
            }
        )
    else:
        assessment = pd.DataFrame(
            {
                "Evidence": ["Time"],
                "Score": [top_vessel["Time_Score"]],
                "Weight": ["100%"],
            }
        )
    st.dataframe(assessment.round(2), use_container_width=True, hide_index=True)

    st.markdown("### Assessment Statement")
    if spill_coordinates_available:
        st.info(
            f"{top_vessel['VesselID']} is the highest-ranked candidate vessel based on the available "
            "spatial, temporal and trajectory evidence in this prototype."
        )
    elif temporal_tie:
        st.info(
            "No unique candidate can be established from the current time-only evidence. "
            "Use a georeferenced spill image and AIS records with meaningful time coverage."
        )
    else:
        st.info(
            f"{top_vessel['VesselID']} is the preliminary top candidate based on temporal proximity only. "
            "A georeferenced spill location is required for the full spatial + temporal + trajectory model."
        )

    st.markdown(
        '<div class="disclaimer"><b>Important:</b> This is a decision-support ranking, not proof of responsibility. The current prototype uses synthetic/demo data and heuristic scoring. Real-world attribution should be verified using validated satellite products, complete AIS history and independent evidence.</div>',
        unsafe_allow_html=True,
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="border-top:1px solid rgba(80,170,205,.12);padding-top:.75rem;display:flex;justify-content:space-between;color:#607b87;font-size:.72rem;">
        <span>🛰️ OrbitalSentinel · Maritime Investigation Prototype</span>
        <span>Satellite Analysis · AIS Correlation · Explainable Attribution</span>
    </div>
    """,
    unsafe_allow_html=True,
)
