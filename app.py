"""Institutional Astronomy, Moon Phases, Solar Ephemeris & Planetary Intelligence Platform."""

import datetime
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from src.astronomy_engine import AstronomyEngine, PLANETS_ORBITAL_DATA
from src.celestial_events_data import CelestialEventsManager
from src.iss_tracker_client import ISSTrackerClient
from src.visualizer import (
    create_3d_solar_system_orrery,
    create_night_sky_polar_chart,
    create_moon_illumination_gauge,
    create_planetary_distance_bar,
    create_iss_world_map
)

# Page Setup
st.set_page_config(
    page_title="Celestial Ephemeris & Astronomy Intelligence Platform",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Deep Space Glassmorphism Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 0.8rem;
    }
    .live-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        color: #34d399;
        font-weight: 600;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.75);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0.3rem 0;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #38bdf8;
    }
    .moon-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Clients
@st.cache_resource
def get_iss_client() -> ISSTrackerClient:
    return ISSTrackerClient()

iss_client = get_iss_client()

# Preset Observer Cities
OBSERVER_CITIES = {
    "Casablanca, Morocco 🇲🇦": {"city": "Casablanca", "lat": 33.5731, "lon": -7.5898, "tz_offset": 1.0},
    "Marrakech, Morocco 🇲🇦": {"city": "Marrakech", "lat": 31.6295, "lon": -7.9811, "tz_offset": 1.0},
    "Riyadh, Saudi Arabia 🇸🇦": {"city": "Riyadh", "lat": 24.7136, "lon": 46.6753, "tz_offset": 3.0},
    "Dubai, UAE 🇦🇪": {"city": "Dubai", "lat": 25.2048, "lon": 55.2708, "tz_offset": 4.0},
    "Cairo, Egypt 🇪🇬": {"city": "Cairo", "lat": 30.0444, "lon": 31.2357, "tz_offset": 2.0},
    "Paris, France 🇫🇷": {"city": "Paris", "lat": 48.8566, "lon": 2.3522, "tz_offset": 2.0},
    "London, UK 🇬🇧": {"city": "London", "lat": 51.5074, "lon": -0.1278, "tz_offset": 1.0},
    "Tokyo, Japan 🇯🇵": {"city": "Tokyo", "lat": 35.6762, "lon": 139.6503, "tz_offset": 9.0},
    "New York, USA 🇺🇸": {"city": "New York", "lat": 40.7128, "lon": -74.0060, "tz_offset": -4.0},
    "Sydney, Australia 🇦🇺": {"city": "Sydney", "lat": -33.8688, "lon": 151.2093, "tz_offset": 10.0}
}

# Sidebar Controls
st.sidebar.markdown("## 🔭 Observer Coordinates & Date")
chosen_location_key = st.sidebar.selectbox("Select Observer City / Observatory:", list(OBSERVER_CITIES.keys()), index=0)
loc_info = OBSERVER_CITIES[chosen_location_key]

simulate_custom_time = st.sidebar.checkbox("Simulate Custom Astronomical Date/Time", value=False)
if simulate_custom_time:
    sim_date = st.sidebar.date_input("Target Date:", value=datetime.date.today())
    sim_time = st.sidebar.time_input("Target Time (UTC):", value=datetime.datetime.utcnow().time())
    current_dt = datetime.datetime.combine(sim_date, sim_time)
else:
    current_dt = datetime.datetime.utcnow()

# Live Auto-Refresh (10 Seconds)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 Live Telemetry & Auto-Refresh")
auto_refresh_enabled = st.sidebar.toggle("10s Auto-Refresh (Live Sync)", value=True)
refresh_counter = 0
if auto_refresh_enabled and not simulate_custom_time:
    refresh_counter = st_autorefresh(interval=10000, limit=None, key="celestial_auto_refresh_10s")

user_lat = loc_info["lat"]
user_lon = loc_info["lon"]
user_tz_offset = loc_info["tz_offset"]
user_city = loc_info["city"]

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
### 📍 Observatory Details:
- **Location:** {chosen_location_key}
- **Latitude:** `{user_lat:.4f}°` | **Longitude:** `{user_lon:.4f}°`
- **Timezone Offset:** `UTC+{user_tz_offset:+.0f}h`
- **Calculation Epoch:** `{current_dt.strftime('%Y-%m-%d %H:%M:%S UTC')}`
""")

# Main Header
st.markdown('<div class="main-title">🌌 Celestial Ephemeris, Moon Phases & Planetary Intelligence</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Real-Time Lunar Phases | Solar Ephemeris & Twilights | 3D Solar System Orrery | Live ISS Space Station Tracking — <b>{chosen_location_key}</b></div>', unsafe_allow_html=True)

# Live Status Badge
if auto_refresh_enabled and not simulate_custom_time:
    st.markdown(f'<div class="live-badge">🟢 LIVE TELEMETRY ACTIVE &bull; Auto-Refreshing every 10s &bull; Last Synced: {current_dt.strftime("%H:%M:%S UTC")} &bull; Cycle #{refresh_counter}</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="live-badge" style="background:rgba(148,163,184,0.1); border-color:rgba(148,163,184,0.3); color:#94a3b8;">⏸️ LIVE SYNC PAUSED (Manual / Custom Simulation Mode) &bull; Epoch: {current_dt.strftime("%Y-%m-%d %H:%M:%S UTC")}</div>', unsafe_allow_html=True)

# Calculate Astronomical Data
moon_res = AstronomyEngine.calculate_moon_phase(current_dt)
sun_res = AstronomyEngine.calculate_sun_and_twilight(user_lat, user_lon, current_dt.date(), tz_offset_hours=user_tz_offset)
planets_res = AstronomyEngine.calculate_planetary_ephemeris(current_dt, user_lat, user_lon)
iss_res = iss_client.fetch_live_iss_position(user_lat, user_lon)

visible_planets_count = sum(1 for p in planets_res if p["is_above_horizon"] and "Visible" in p["visibility_badge"])

# Top KPI Metric Cards
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Current Moon Phase</div>
        <div class="metric-value">{moon_res['icon']} {moon_res['phase_simple']}</div>
        <div class="metric-sub">Age: {moon_res['moon_age_days']} days</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Lunar Illumination</div>
        <div class="metric-value">🌕 {moon_res['illumination_pct']}%</div>
        <div class="metric-sub">Next Full Moon: {moon_res['days_to_full_moon']}d</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Earth-Moon Distance</div>
        <div class="metric-value">📏 {int(moon_res['distance_km']):,} <span style="font-size:1rem;">km</span></div>
        <div class="metric-sub">{moon_res['distance_status'][:20]}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Naked-Eye Planets</div>
        <div class="metric-value">🪐 {visible_planets_count} / 5</div>
        <div class="metric-sub">Visible in Local Night Sky</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Daylight Length</div>
        <div class="metric-value">☀️ {sun_res['day_length_formatted']}</div>
        <div class="metric-sub">Solar Noon: {sun_res['solar_noon']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Navigation Tabs (6 Modules)
tabs = st.tabs([
    "🌙 Moon Phases & Lunar Intelligence",
    "🪐 Planets & Solar System Ephemeris",
    "☀️ Sun, Twilight & Golden Hours",
    "🌌 3D Solar System & Stargazing Sky Chart",
    "☄️ Meteor Showers & Eclipses Calendar",
    "🛰️ Live ISS & Space Station Tracker"
])

# ----------------- TAB 1: Moon Phases -----------------
with tabs[0]:
    st.markdown("### 🌙 Real-Time Lunar Ephemeris, Phases & Orbital Dynamics")
    
    m_col1, m_col2 = st.columns([1, 1.2])
    with m_col1:
        st.markdown(f"""
        <div class="moon-card">
            <h3>{moon_res['phase_name']}</h3>
            <h1 style="color:#fef08a; font-size:3rem; margin:0.5rem 0;">{moon_res['icon']} {moon_res['illumination_pct']}%</h1>
            <p><b>🌓 Description:</b> {moon_res['visibility_desc']}</p>
            <hr style="border-color: rgba(245, 158, 11, 0.2);">
            <p><b>📅 Lunar Synodic Age:</b> <code>{moon_res['moon_age_days']} / 29.53 days</code></p>
            <p><b>📏 Distance to Earth:</b> <code>{int(moon_res['distance_km']):,} km</code> ({moon_res['distance_status']})</p>
            <p><b>⏱️ Lunar Light Travel Time:</b> <code>{moon_res['light_travel_time_sec']} seconds</code></p>
            <p><b>🌕 Next Full Moon:</b> <b>{moon_res['next_full_moon_date']}</b> (in {moon_res['days_to_full_moon']} days)</p>
            <p><b>🌑 Next New Moon:</b> <b>{moon_res['next_new_moon_date']}</b> (in {moon_res['days_to_new_moon']} days)</p>
        </div>
        """, unsafe_allow_html=True)

    with m_col2:
        fig_moon_gauge = create_moon_illumination_gauge(moon_res["illumination_pct"], moon_res["phase_simple"])
        st.plotly_chart(fig_moon_gauge, use_container_width=True)

        with st.expander("📚 Lunar Synodic Cycle Guide"):
            st.markdown("""
            | Lunar Phase | Typical Age | Illumination | Stargazing Impact |
            | :--- | :--- | :--- | :--- |
            | **New Moon 🌑** | 0.0 - 1.8 days | 0% | **Best time for Deep-Sky Astrophotography** (Milky Way & galaxies). |
            | **Waxing Crescent 🌒** | 1.8 - 5.5 days | 1% - 35% | Beautiful crescent in western evening twilight. |
            | **First Quarter 🌓** | 5.5 - 9.2 days | 50% | High contrast along lunar terminator for telescope crater viewing. |
            | **Full Moon 🌕** | 12.9 - 16.6 days | 100% | Brightest night sky; washes out faint nebulae. |
            | **Third Quarter 🌗** | 20.3 - 24.0 days | 50% | Visible during dawn and morning hours. |
            """)

# ----------------- TAB 2: Planetary Ephemeris -----------------
with tabs[1]:
    st.markdown("### 🪐 Planetary Coordinates, Magnitudes & Visibility")
    st.markdown("Real-time positions, apparent magnitudes, and observing recommendations for all 7 Solar System planets.")

    df_planets = pd.DataFrame(planets_res)
    st.dataframe(
        df_planets[["display_label", "type", "constellation", "distance_million_km", "distance_au", "apparent_magnitude", "altitude_deg", "visibility_badge"]].rename(columns={
            "display_label": "Planet",
            "type": "Classification",
            "constellation": "Constellation",
            "distance_million_km": "Distance (M km)",
            "distance_au": "Distance (AU)",
            "apparent_magnitude": "Magnitude (m)",
            "altitude_deg": "Altitude (°)",
            "visibility_badge": "Observing Status"
        }),
        use_container_width=True,
        hide_index=True
    )

    fig_dist = create_planetary_distance_bar(planets_res)
    st.plotly_chart(fig_dist, use_container_width=True)

# ----------------- TAB 3: Sun & Twilight Hours -----------------
with tabs[2]:
    st.markdown("### ☀️ Solar Ephemeris, Twilight Boundaries & Golden Hours")
    st.markdown(f"Photographic lighting windows and solar angles calculated for **{chosen_location_key}**.")

    s_c1, s_c2, s_c3 = st.columns(3)
    with s_c1:
        st.markdown(f"""
        #### 🌅 Sunrise & Sunset
        - **Dawn (Sunrise):** `{sun_res['sunrise']}`
        - **Solar Noon:** `{sun_res['solar_noon']}`
        - **Dusk (Sunset):** `{sun_res['sunset']}`
        - **Total Daylight:** `{sun_res['day_length_formatted']}`
        - **Solar Declination:** `{sun_res['solar_declination_deg']}°`
        """)

    with s_c2:
        st.markdown(f"""
        #### 🌌 Twilight Boundaries
        - **Civil Twilight:** `{sun_res['civil_dawn']} - {sun_res['sunrise']}` & `{sun_res['sunset']} - {sun_res['civil_dusk']}`
        - **Nautical Twilight:** `{sun_res['nautical_dawn']} - {sun_res['nautical_dusk']}`
        - **Astronomical Dark Sky:** `{sun_res['astronomical_dusk']} - {sun_res['astronomical_dawn']}` *(Optimal Stargazing)*
        """)

    with s_c3:
        st.markdown(f"""
        #### 📸 Photography Lighting Hours
        - **Evening Golden Hour:** `{sun_res['golden_hour_evening']}` *(Warm soft sunlight)*
        - **Evening Blue Hour:** `{sun_res['blue_hour_evening']}` *(Vibrant deep blue sky gradient)*
        """)

# ----------------- TAB 4: 3D Orrery & Sky Chart -----------------
with tabs[3]:
    st.markdown("### 🌌 3D Interactive Solar System Orrery & Night Sky Chart")
    
    st.plotly_chart(create_3d_solar_system_orrery(planets_res), use_container_width=True)

    st.markdown("#### 🔭 2D Night Sky Polar Radar")
    st.plotly_chart(create_night_sky_polar_chart(planets_res, moon_res), use_container_width=True)

# ----------------- TAB 5: Meteor Showers & Eclipses -----------------
with tabs[4]:
    st.markdown("### ☄️ Meteor Showers Calendar & Solar/Lunar Eclipses")
    
    e_tab1, e_tab2 = st.tabs(["☄️ Annual Major Meteor Showers", "🌑 Solar & Lunar Eclipses (2026 - 2030)"])
    
    with e_tab1:
        st.markdown("#### ☄️ Major Annual Meteor Showers")
        df_meteors = CelestialEventsManager.get_meteor_showers_df()
        st.dataframe(df_meteors.rename(columns={
            "name": "Shower Name",
            "peak_date": "Peak Date",
            "activity_period": "Activity Window",
            "zhr_hourly_rate": "Zenithal Hourly Rate (ZHR)",
            "radiant_constellation": "Radiant",
            "parent_body": "Parent Comet / Asteroid",
            "viewing_conditions": "Observing Profile"
        }), use_container_width=True, hide_index=True)

    with e_tab2:
        st.markdown("#### 🌑 Solar & Lunar Eclipses Calendar")
        df_eclipses = CelestialEventsManager.get_eclipses_df()
        st.dataframe(df_eclipses.rename(columns={
            "date": "Date",
            "type": "Eclipse Type",
            "duration_totality": "Max Totality",
            "path_regions": "Geographic Path & Visibility",
            "significance": "Astronomical Significance"
        }), use_container_width=True, hide_index=True)

# ----------------- TAB 6: Live ISS Tracker -----------------
with tabs[5]:
    st.markdown("### 🛰️ Live International Space Station (ISS) Orbital Tracking")
    
    ic1, ic2, ic3, ic4 = st.columns(4)
    ic1.metric("Orbital Altitude", f"{iss_res['altitude_km']} km", "Low Earth Orbit (LEO)")
    ic2.metric("Orbital Velocity", f"{iss_res['velocity_kmh']:,} km/h", f"{iss_res['velocity_kms']} km/s")
    ic3.metric(f"Distance to {user_city}", f"{iss_res['distance_to_user_km']:,} km", "Overhead" if iss_res['is_overhead'] else "Beyond Horizon")
    ic4.metric("Orbital Period", f"{iss_res['orbital_period_min']} min", "16 Sunrises / Day")

    fig_iss = create_iss_world_map(iss_res, user_lat, user_lon, user_city)
    st.plotly_chart(fig_iss, use_container_width=True)
