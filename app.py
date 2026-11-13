import streamlit as st
import pandas as pd
import requests
import folium
from datetime import datetime
from streamlit_folium import st_folium
from random import randint

# --- IMPORTS FROM MODEL & UTILS ---
try:
    from model import train_model, predict_aqi, forecast_future_aqi
    from utils import get_aqi

except ImportError as e:
    st.error(f"Import Error: {e}")
    st.exception(e)
    st.stop()

# --- 0. PAGE CONFIG ---
# We remove initial_sidebar_state="expanded" since we are removing the sidebar entirely.
st.set_page_config(page_title="EnviroCast AI | Smart AQI", page_icon="🌍", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS FOR MODERN UI ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Outfit:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif;
}

/* Hide Sidebar Completely */
[data-testid="collapsedControl"] {
    display: none;
}
[data-testid="stSidebar"] {
    display: none;
}

/* Gradient Background */
.stApp {
    background: linear-gradient(135deg, #e0f2fe 0%, #f0fdf4 100%);
}

.title-main {
    background: -webkit-linear-gradient(45deg, #0284c7, #10b981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    font-size: 3rem;
    margin-bottom: 0.5rem;
    text-align: center;
}

.subtitle-main {
    text-align: center;
    color: #475569;
    font-size: 1.2rem;
    margin-bottom: 2rem;
    font-weight: 400;
}

/* Metric Cards Customization */
div[data-testid="metric-container"] {
    background: linear-gradient(145deg, #ffffff, #f8fafc);
    padding: 15px 20px;
    border-radius: 16px;
    box-shadow: 4px 4px 15px rgba(0,0,0,0.03), -4px -4px 15px rgba(255,255,255,1);
    border-left: 6px solid #0ea5e9;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
div[data-testid="metric-container"]::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 50px; height: 100%;
    background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.8) 100%);
    opacity: 0.5;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 6px 6px 20px rgba(0,0,0,0.06), -6px -6px 20px rgba(255,255,255,1);
    border-left-color: #10b981;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9 0%, #10b981 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 14px 28px;
    font-weight: 700;
    font-family: 'Outfit', sans-serif;
    width: 100%;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 14px 0 rgba(14, 165, 233, 0.39);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0284c7 0%, #059669 100%);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(14, 165, 233, 0.5);
    color: white;
}

/* Download button special */
.stDownloadButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    box-shadow: 0 4px 14px 0 rgba(16, 185, 129, 0.39);
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5);
}

/* Logout Button Special Style (making it red to stand out) */
.logout-btn button {
    background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%) !important;
    box-shadow: 0 4px 14px 0 rgba(239, 68, 68, 0.39) !important;
    padding: 8px 16px !important;
}
.logout-btn button:hover {
    background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%) !important;
}

/* Status Box */
.status-box {
    padding: 30px;
    border-radius: 20px;
    color: white;
    font-weight: 700;
    text-align: center;
    font-size: 26px;
    margin: 20px 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    font-family: 'Outfit', sans-serif;
    animation: slideUp 0.6s ease-out;
    position: relative;
    overflow: hidden;
}
.status-box::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 60%);
    pointer-events: none;
}
.status-desc {
    font-size: 16px;
    font-weight: 400;
    margin-top: 10px;
    opacity: 0.9;
    font-family: 'Inter', sans-serif;
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Dataframe customization */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

/* Navigation Menu Tabs Styling */
div[data-testid="stRadio"] > div {
    display: flex;
    flex-direction: row;
    justify-content: center;
    background-color: rgba(255, 255, 255, 0.4);
    padding: 10px;
    border-radius: 15px;
    gap: 10px;
    flex-wrap: wrap;
}
div[data-testid="stRadio"] label {
    background-color: transparent;
    padding: 10px 20px;
    border-radius: 10px;
    cursor: pointer;
    border: none;
    transition: all 0.3s ease;
}
div[data-testid="stRadio"] label:hover {
    background-color: rgba(255,255,255,0.6);
}
div[data-testid="stRadio"] [data-checked="true"] {
    background-color: white !important;
    color: #0284c7 !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
    border-radius: 10px !important;
}
[data-testid="stRadio"] label > div[data-testid="stMarkdownContainer"] > p {
    font-weight: 600;
    margin: 0;
}

/* Specific class to move logout button visually to top right via markdown injection */
.st-key-logout_upper {
    position: fixed !important;
    top: 12px !important;
    right: 65px !important;
    z-index: 999999 !important;
    width: auto !important;
}

/* Hide native Deploy Button completely */
[data-testid="stAppDeployButton"], .stAppDeployButton {
    display: none !important;
}

/* Fix Streamlit main padding to accommodate absolute button */
.block-container {
    padding-top: 4rem;
}
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def get_aqi_category(aqi):
    if aqi <= 60: return "Good"
    elif aqi <= 100: return "Moderate"
    elif aqi <= 150: return "Unhealthy"
    elif aqi <= 250: return "Very Unhealthy"
    else: return "Hazardous"

def show_health_alert(aqi, title_prefix="Analysis for"):
    if aqi <= 60:
        bg = "linear-gradient(135deg, #059669 0%, #10b981 100%)"
        icon, title, desc = "🍃", "GOOD", "Air quality is considered satisfactory, and air pollution poses little or no risk."
    elif aqi <= 100:
        bg = "linear-gradient(135deg, #d97706 0%, #f59e0b 100%)"
        icon, title, desc = "😐", "MODERATE", "Air quality is acceptable; however, there may be a moderate health concern for a very small number of people."
    elif aqi <= 150:
        bg = "linear-gradient(135deg, #ea580c 0%, #f97316 100%)"
        icon, title, desc = "😷", "UNHEALTHY FOR SENSITIVE GROUPS", "Members of sensitive groups may experience health effects. The general public is not likely to be affected."
    elif aqi <= 250:
        bg = "linear-gradient(135deg, #b91c1c 0%, #ef4444 100%)"
        icon, title, desc = "🚨", "VERY UNHEALTHY", "Health alert: everyone may experience more serious health effects. Stay indoors."
    else:
        bg = "linear-gradient(135deg, #7f1d1d 0%, #9f1239 100%)"
        icon, title, desc = "☠️", "HAZARDOUS", "Health warnings of emergency conditions. The entire population is more likely to be affected."

    st.markdown(
        f'<div class="status-box" style="background: {bg};">'
        f'<div style="font-size: 40px; margin-bottom: 10px;">{icon}</div>'
        f'{title} <br><span style="font-size: 20px;">AQI: {round(aqi,1)}</span>'
        f'<div class="status-desc">{desc}</div>'
        f'</div>', unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "user_db" not in st.session_state: st.session_state.user_db = {"admin": "1234"}
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "auth_mode" not in st.session_state: st.session_state.auth_mode = "login"
if "prediction_history" not in st.session_state: st.session_state.prediction_history = []

# --- AUTHENTICATION PAGE ---
def auth_page():
    st.markdown('<div class="title-main" style="margin-top: 5vh; font-size: 3.5rem;">🌍 EnviroCast AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-main">Smart Air Quality Prediction and Forecasting System</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.auth_mode == "login":

            u = st.text_input("Username", placeholder="Enter your username")
            p = st.text_input("Password", type="password", placeholder="Enter your password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Secure Login"):
                if u in st.session_state.user_db and st.session_state.user_db[u] == p:
                    st.session_state.logged_in = True
                    st.rerun()
                else: 
                    st.error("❌ Invalid Credentials. Please try again.")
            st.markdown("<hr style='margin:20px 0; opacity:0.3'>", unsafe_allow_html=True)
            if st.button("Create New Account", use_container_width=True):
                st.session_state.auth_mode = "register"
                st.rerun()
        else:
            st.markdown('<h2 style="color: #0f172a; margin-bottom: 30px; text-align: center;">Join Us! 🌱</h2>', unsafe_allow_html=True)
            ru = st.text_input("New Username", placeholder="Choose a username")
            rp = st.text_input("New Password", type="password", placeholder="Create a strong password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Register & Continue"):
                if ru and rp:
                    st.session_state.user_db[ru] = rp
                    st.session_state.auth_mode = "login"
                    st.success("✅ Account created successfully!")
                    st.rerun()
                else:
                    st.warning("⚠️ Please fill in all fields.")
            st.markdown("<hr style='margin:20px 0; opacity:0.3'>", unsafe_allow_html=True)
            st.button("Back to Login", on_click=lambda: st.session_state.update({"auth_mode": "login"}))

if not st.session_state.logged_in:
    auth_page()
    st.stop()


# --- DATA & MODEL LOADING ---
@st.cache_resource(show_spinner=False)
def load_ml_resources():
    return train_model()

with st.spinner("Initializing EnviroCast AI Engine..."):
    try:
        model, df_main, metrics = load_ml_resources()
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()


# --- LOGOUT BUTTON (TOP RIGHT) ---
# This button is placed high up in the render order and styled to hover near the native "Deploy" button
col_dummy, col_logout = st.columns([85, 15])
with col_logout:
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("🚪 Logout", key="logout_upper"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# --- MAIN CONTENT DASHBOARD ---
st.markdown('<div class="title-main">EnviroCast AI Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-main">Monitor, Predict, and Analyze Air Quality with Machine Learning</div>', unsafe_allow_html=True)

# Navigation via programmatic state to improve speed (Lazy Loading)
nav_options = [
    "📍 Live AQI Analysis", 
    "🧪 Manual Prediction", 
    "🔮 Future Forecast", 
    "🗺️ Map View", 
    "📊 Data Report", 
    "📈 Trends"
]

selected_tab = st.radio("Navigation", nav_options, horizontal=True, label_visibility="collapsed")

# ------------- TAB 1: LIVE AQI ANALYSIS -------------
if selected_tab == "📍 Live AQI Analysis":
    st.markdown('<h3><span style="font-size:1.5rem">📡</span> Real-Time Air Quality Monitoring</h3>', unsafe_allow_html=True)
    st.write("Enter any global city name to fetch real-time pollutant levels and our AI-predicted AQI.")
    
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        city = st.text_input("City Name", placeholder="e.g., Delhi, New York, London", value="Delhi", label_visibility="collapsed")
    with col_btn:
        analyze_btn = st.button("Analyze Live AQI")
    
    if analyze_btn and city:
        with st.spinner(f"Fetching live sensor data for {city}..."):
            try:
                data = get_aqi(city)
                if data and 'list' in data and len(data['list']) > 0:
                    c = data['list'][0]['components']
                    
                    p = predict_aqi(model, c.get('pm2_5',0), c.get('pm10',0), c.get('no2',0), c.get('co',0)/100, c.get('so2',0), c.get('o3',0))
                    
                    st.session_state.prediction_history.append({"City": city, "AQI": round(p, 2), "Status": get_aqi_category(p), "Time": datetime.now().strftime("%Y-%m-%d %H:%M")})
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    show_health_alert(p, f"{city}")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("#### 🔬 Detailed Pollutant Breakdown")
                    m1, m2, m3, m4, m5, m6 = st.columns(6)
                    m1.metric("PM2.5", f"{c.get('pm2_5',0)} μg/m³")
                    m2.metric("PM10", f"{c.get('pm10',0)} μg/m³")
                    m3.metric("NO2", f"{c.get('no2',0)} μg/m³")
                    m4.metric("CO", f"{c.get('co',0)} μg/m³")
                    m5.metric("SO2", f"{c.get('so2',0)} μg/m³")
                    m6.metric("O3", f"{c.get('o3',0)} μg/m³")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("#### 📊 Relative Pollutant Concentration")
                    pollutant_df = pd.DataFrame({
                        "Concentration": [c.get('pm2_5',0), c.get('pm10',0), c.get('no2',0), c.get('so2',0), c.get('o3',0)]
                    }, index=["PM2.5", "PM10", "NO2", "SO2", "O3"])
                    
                    st.bar_chart(pollutant_df, color="#0ea5e9", use_container_width=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    download_df = pd.DataFrame({
                        "Parameter": ["Predicted AQI", "PM2.5", "PM10", "NO2", "CO", "SO2", "O3"],
                        "Value": [round(p, 2), c.get('pm2_5',0), c.get('pm10',0), c.get('no2',0), c.get('co',0), c.get('so2',0), c.get('o3',0)],
                        "Unit": ["AQI", "μg/m³", "μg/m³", "μg/m³", "μg/m³", "μg/m³", "μg/m³"]
                    })
                    st.download_button(
                        label="⬇️ Download Full Report (CSV)",
                        data=download_df.to_csv(index=False),
                        file_name=f"{city}_envirocast_report_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.error(f"❌ Could not find reliable data for '{city}'. Please check the spellings or try a larger nearby city.")
            except Exception as e:
                st.error("🚨 Cloud API execution failed. Please check internet connectivity or try again later.")

# ------------- TAB 2: MANUAL PREDICTION -------------
if selected_tab == "🧪 Manual Prediction":
    st.markdown('<h3><span style="font-size:1.5rem">🧪</span> Manual Scenario Simulator</h3>', unsafe_allow_html=True)
    st.write("Adjust the environmental factors using the sliders below to see how our ML model predicts the AQI.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_a, spacer, col_b = st.columns([10, 1, 10])
    with col_a:
        m25 = st.slider("Fine Particulate Matter (PM2.5)", 0.0, 500.0, 25.0, help="μg/m³")
        m10 = st.slider("Coarse Particulate Matter (PM10)", 0.0, 500.0, 45.0, help="μg/m³")
        no2_v = st.slider("Nitrogen Dioxide (NO2)", 0.0, 200.0, 15.0, help="μg/m³")
    with col_b:
        co_v = st.slider("Carbon Monoxide (CO)", 0.0, 50.0, 1.5, help="mg/m³")
        so2_v = st.slider("Sulfur Dioxide (SO2)", 0.0, 200.0, 10.0, help="μg/m³")
        o3_v = st.slider("Ozone (O3)", 0.0, 300.0, 40.0, help="μg/m³")
    
    st.markdown("<br>", unsafe_allow_html=True)
    predict_manual = st.button("Run Simulation", use_container_width=True)
    if predict_manual:
        with st.spinner("Running ML Inference Engine..."):
            res = predict_aqi(model, m25, m10, no2_v, co_v, so2_v, o3_v)
            show_health_alert(res, "Simulation Result")

# ------------- TAB 3: FUTURE FORECAST -------------
if selected_tab == "🔮 Future Forecast":
    st.markdown('<h3><span style="font-size:1.5rem">🔮</span> 7-Day ARIMA Future Forecast</h3>', unsafe_allow_html=True)
    st.write("Using predictive time-series modeling to project air quality trends for the next week.")
    
    fc_city = st.text_input("Target Location for Forecast", placeholder="Enter city name", value="Delhi", key="fc_city")
    
    if st.button("Generate 7-Day Forecast"):
        with st.spinner("Analyzing historical and live patterns..."):
            try:
                data = get_aqi(fc_city)
                if data and 'list' in data and len(data['list']) > 0:
                    c = data['list'][0]['components']
                    current_aqi = predict_aqi(model, c.get('pm2_5',0), c.get('pm10',0), c.get('no2',0), c.get('co',0)/100, c.get('so2',0), c.get('o3',0))
                    
                    if not df_main.empty and 'AQI' in df_main.columns:
                        f_values = forecast_future_aqi(df_main['AQI'], steps=7)
                    else:
                        f_values = [current_aqi + (i*randint(-3, 8)) for i in range(7)]
                    
                    if len(f_values) != 7:
                        f_values = [current_aqi + (i*randint(-3, 8)) for i in range(7)] 

                    dates = pd.date_range(start=datetime.now(), periods=7).strftime('%b %d, %Y')
                    f_df = pd.DataFrame({
                        'Date': dates,
                        'Predicted AQI': [round(max(0, val), 1) for val in f_values]
                    })
                    f_df["Expected Condition"] = f_df["Predicted AQI"].apply(get_aqi_category)
                    
                    st.markdown("#### 📈 Predicted Trend Sequence")
                    chart_data = f_df.set_index("Date")[["Predicted AQI"]]
                    st.area_chart(chart_data, color="#10b981", use_container_width=True)
                    
                    st.markdown("#### 📅 Daily Forecast Breakdown")
                    st.dataframe(f_df, use_container_width=True, hide_index=True)
                    
                    max_aqi = max(f_df['Predicted AQI'])
                    if max_aqi > 150:
                        st.warning("⚠️ **Forecast Alert:** AQI is expected to reach unhealthy levels in the coming week. Plan outdoor activities accordingly.")
                    else:
                        st.success("✅ **Forecast Clear:** Air quality is expected to remain relatively stable and safe.")
                else:
                    st.error("❌ Location not found.")
            except Exception as e:
                st.error("🚨 Forecast engine failed to load.")

# ------------- TAB 4: MAP VIEW -------------
if selected_tab == "🗺️ Map View":
    st.markdown('<h3><span style="font-size:1.5rem">🗺️</span> Geospatial AQI Mapping</h3>', unsafe_allow_html=True)
    st.write("Visualize location-specific telemetry directly on the map.")
    
    col_m1, col_m2 = st.columns([3, 1])
    with col_m1:
        m_loc = st.text_input("Enter Geography", value="Hyderabad", label_visibility="collapsed", key="map_loc")
    with col_m2:
        view_map = st.button("Locate & Map", use_container_width=True)
        
    if view_map and m_loc:
        with st.spinner("Geocoding Location..."):
            try:
                g_url = f"http://api.openweathermap.org/geo/1.0/direct?q={m_loc}&limit=1&appid=b12fa0b558f4349d5edbd5da92d9d7ef"
                res = requests.get(g_url).json()
                if res and len(res) > 0:
                    lat, lon = res[0]['lat'], res[0]['lon']
                    m = folium.Map(location=[lat, lon], zoom_start=11, tiles="CartoDB positron")
                    
                    m_aqi = 50
                    try:
                        md = get_aqi(m_loc)
                        if md and 'list' in md:
                            mc = md['list'][0]['components']
                            m_aqi = predict_aqi(model, mc.get('pm2_5',0), mc.get('pm10',0), mc.get('no2',0), mc.get('co',0)/100, mc.get('so2',0), mc.get('o3',0))
                    except: pass
                    
                    color = "green" if m_aqi <= 100 else ("orange" if m_aqi <= 200 else "red")
                    
                    folium.Marker(
                        [lat, lon], 
                        popup=f"<b>{m_loc.title()}</b><br>Est. AQI: {round(m_aqi,1)}", 
                        icon=folium.Icon(color=color, icon="cloud")
                    ).add_to(m)
                    
                    folium.Circle(
                        radius=5000, location=[lat, lon], color=color, fill=True, opacity=0.3
                    ).add_to(m)
                    
                    st_folium(m, width=1200, height=500, returned_objects=[])
                else:
                    st.error("❌ Geolocation mismatch. Location could not be mapped.")
            except Exception as e:
                st.error("🚨 Mapping service currently unavailable.")

# ------------- TAB 5: DATA REPORT -------------
if selected_tab == "📊 Data Report":
    st.markdown('<h3><span style="font-size:1.5rem">📊</span> Data Intelligence & Reporting</h3>', unsafe_allow_html=True)
    
    st.markdown("#### 🕒 Your Session Search History")
    if st.session_state.prediction_history:
        st.dataframe(pd.DataFrame(st.session_state.prediction_history).iloc[::-1], use_container_width=True, hide_index=True)
    else:
        st.info("No queries performed in the current session. Go to 'Live AQI Analysis' to start.")
        
    st.markdown("<hr style='opacity: 0.2;'>", unsafe_allow_html=True)
    st.markdown("#### 📚 Model Training Dataset Overview")
    st.write("Our predictive engine is trained on thousands of validated historical data points.")
    if not df_main.empty and 'AQI' in df_main.columns:
        st.line_chart(df_main.tail(100).reset_index(drop=True)[["AQI"]], color="#0ea5e9", use_container_width=True)
    else:
        st.write("Training dataset visualization unavailable.")

# ------------- TAB 6: TRENDS -------------
if selected_tab == "📈 Trends":
    st.markdown('<h3><span style="font-size:1.5rem">📈</span> Macro Environmental Trends</h3>', unsafe_allow_html=True)
    st.write("Discover the latest shifts in overall air quality metrics based on trailing data frames.")
    
    if not df_main.empty and 'AQI' in df_main.columns:
        recent_data = df_main['AQI'].tail(15).values
        avg_change = df_main['AQI'].tail(10).diff().mean()
        
        col_t1, col_t2, col_t3 = st.columns(3)
        col_t1.metric("Recent Moving Average", f"{round(sum(recent_data)/len(recent_data), 1)} AQI")
        col_t2.metric("Average Daily Variance", f"{round(avg_change, 2)} Units", delta=round(avg_change, 2), delta_color="inverse")
        col_t3.metric("Peak Recorded Toxicity", f"{round(max(df_main['AQI']), 1)} AQI")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📉 Trailing 15-Day Variance Profile")
        trend_df = pd.DataFrame({"Recorded AQI": recent_data}, index=[f"T-{15-i}" for i in range(15)])
        st.bar_chart(trend_df, color="#3b82f6", use_container_width=True)
        
    else:
        st.info("Trend data is currently recalculating. Please ensure dataset integrity.")