import streamlit as st
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
import pandas as pd
from backend import analyze_emergency, get_nearby_resources, get_historical_analysis, get_emergency_news, transcribe_audio

# Page config & styling
st.set_page_config(page_title="Rescue AI Dashboard", page_icon="🚨", layout="wide")

st.markdown("""
<style>
    /* Premium App Styling */
    .stApp {
        background-color: #f8f9fa;
    }
    .main-header {
        font-family: 'Inter', sans-serif;
        color: #1e3d59;
        font-weight: 800;
        letter-spacing: -1px;
    }
    .stButton>button { 
        border-radius: 12px; 
        font-weight: bold; 
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 4px 15px rgba(255, 65, 108, 0.4);
    }
    .card-style {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .news-card {
        padding: 20px; 
        border-radius: 12px; 
        margin-bottom: 15px; 
        border-left: 6px solid;
        background: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }
    .badge-critical { background: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 20px; font-weight: bold; }
    .badge-medium { background: #fef3c7; color: #92400e; padding: 4px 10px; border-radius: 20px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "search_executed" not in st.session_state:
    st.session_state.search_executed = False

# Sidebar Navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/912/912301.png", width=60)
    st.title("🚨 Rescue AI")
    st.markdown("Advanced Deep Learning Emergency System")
    st.divider()
    page = st.radio("Navigation", ["📟 Dispatch Center", "📈 Analysis Dashboard", "📰 Live News Feed"], label_visibility="collapsed")
    st.divider()
    st.caption("Powered by Llama 3.2 & OpenStreetMap")

if page == "📟 Dispatch Center":
    st.markdown("<h1 class='main-header'>📟 AI Dispatch Center</h1>", unsafe_allow_html=True)
    st.markdown("Instantly decode natural language emergencies and locate immediate nearby resources. Speak or type your request.")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("<div class='card-style'>", unsafe_allow_html=True)
        st.subheader("📍 Target Area")
        location_input = st.text_input("Current location or landmark", "T Nagar, Chennai", help="Enter a general city or precise address.")
        lang = st.selectbox("🌐 Translation / Target Language", ["English", "Tamil", "Hindi", "Spanish", "French"], help="Translate the AI thoughts to this language.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card-style'>", unsafe_allow_html=True)
        st.subheader("🗣️ Emergency Audio or Text")
        audio_bytes = st.audio_input("Record Emergency Voice Note")
        em_text = st.text_area("Or type the situation...", 
                               "Massive accident on the highway! Two cars involved, people are trapped.", 
                               height=85)
        st.markdown("</div>", unsafe_allow_html=True)
        
    find_button = st.button("🚀 DEPLOY AI & FIND HELP", use_container_width=True)

    geolocator = Nominatim(user_agent="emergency_finder_app")

    if find_button:
        # Resolve audio vs text
        final_input = em_text
        if audio_bytes is not None:
            with st.spinner("🎙️ Transcribing Audio format..."):
                transcribed = transcribe_audio(audio_bytes.getvalue(), lang=lang)
                if transcribed:
                    final_input = transcribed
                    st.toast(f"Transcribed successfully!", icon="✅")
                else:
                    st.toast("Audio format unrecognized. Using text fallback.", icon="⚠️")

        if not final_input.strip() or not location_input.strip():
            st.error("Hold on! Please provide both location and emergency details.")
        else:
            with st.status("Deploying Rescue AI Pipeline...", expanded=True) as status:
                st.session_state.search_executed = False 
                
                status.update(label="🌍 Pinpointing geometric coordinates...", state="running")
                location = geolocator.geocode(location_input)
                if not location:
                    st.error("Invalid location. Try a broader city or area name.")
                    st.stop()
                
                st.session_state.user_lat = location.latitude
                st.session_state.user_lon = location.longitude
                
                status.update(label=f"🧠 Local Llama3.2 reading: '{final_input}'", state="running")
                analysis = analyze_emergency(final_input, lang=lang)
                st.session_state.intent = analysis.get("intent", "medical").upper()
                st.session_state.severity = analysis.get("severity", "critical").upper()
                st.session_state.reason = analysis.get("reason", "No reason provided")
                
                status.update(label=f"📡 Querying global OSM API for '{st.session_state.intent}' facilities... (with Redundant Fallbacks)", state="running")
                st.session_state.resources = get_nearby_resources(
                    st.session_state.user_lat, 
                    st.session_state.user_lon, 
                    st.session_state.intent.lower(), 
                    radius_meters=7000
                )
                
                st.session_state.search_executed = True
                status.update(label="Mission plan assembled successfully.", state="complete")

    if st.session_state.search_executed:
        st.divider()
        st.markdown("<h2 class='main-header'>🎯 Mission Overview</h2>", unsafe_allow_html=True)
        
        info_col, map_col = st.columns([1.2, 1.5])
        
        with info_col:
            st.markdown("<div class='card-style'>", unsafe_allow_html=True)
            st.subheader("🧠 Deep Learning Inference")
            met1, met2 = st.columns(2)
            met1.metric(label="Detected Intent", value=st.session_state.intent)
            met2.metric(label="Threat Level", value=st.session_state.severity)
            
            with st.expander("Show AI Reasoning Engine", expanded=True):
                st.write(f"*{st.session_state.reason}*")
                
            if st.session_state.severity == "CRITICAL":
                st.markdown("<span class='badge-critical'>⚠️ EXPEDITING RESPONSE</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span class='badge-medium'>🟠 STABLE PRIORITY</span>", unsafe_allow_html=True)
            st.write("")
            
            st.subheader(f"🏥 Top {len(st.session_state.resources)} Live Assets Dispatched")
            if not st.session_state.resources:
                st.error("API Limit Reached or no resources found. Fallback to global dispatch hotline: 911 / 112")
            else:
                for idx, res in enumerate(st.session_state.resources):
                    st.info(f"**#{idx+1} {res['name']}**\n\n📍 {res['distance_km']} km away  |  📞 {res['phone']}")
            st.markdown("</div>", unsafe_allow_html=True)

        with map_col:
            st.markdown("<div class='card-style'>", unsafe_allow_html=True)
            st.subheader("📡 Live Radar Vectoring")
            m = folium.Map(location=[st.session_state.user_lat, st.session_state.user_lon], zoom_start=13, tiles="CartoDB positron")
            
            folium.Marker(
                [st.session_state.user_lat, st.session_state.user_lon], 
                popup="Incident Origin", 
                tooltip="You are here", 
                icon=folium.Icon(color="darkred", icon="warning-sign", prefix='glyphicon')
            ).add_to(m)
            
            for res in st.session_state.resources:
                folium.Marker(
                    [res['lat'], res['lon']],
                    popup=res['name'],
                    tooltip=f"{res['name']} ({res['distance_km']}km)",
                    icon=folium.Icon(color="blue", icon="plus", prefix='glyphicon')
                ).add_to(m)
            
            # Use returned data silently to prevent reruns from destroying state
            st_folium(m, width="100%", height=450, returned_objects=[])
            st.markdown("</div>", unsafe_allow_html=True)

elif page == "📈 Analysis Dashboard":
    st.markdown("<h1 class='main-header'>📈 Intelligence Analyst Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("Macro-level view of emergency vectors processed over the last 30 days.")
    
    df = get_historical_analysis()
    
    st.markdown("<div class='card-style'>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Incidents Executed (30d)", f"{df['Incidents'].sum():,}", "+12% MoM")
    m2.metric("Critical Red Alerts", f"{int(df['Incidents'].sum() * 0.15):,}", "-2% MoM")
    m3.metric("Avg Dispatch Reaction", "2.1 mins", "-0.8 mins globally")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card-style'>", unsafe_allow_html=True)
    st.subheader("Timeline: Historical Incidents by Classification Category")
    pivot_df = df.pivot(index='Date', columns='Type', values='Incidents')
    st.area_chart(pivot_df, use_container_width=True)
    

elif page == "📰 Live News Feed":
    st.markdown("<h1 class='main-header'>🌍 Live Global Dispatch Feed</h1>", unsafe_allow_html=True)
    st.markdown("Real-time disaster data aggregated from GDACS Inter-agency API.")
    
    news = get_emergency_news()
    for item in news:
        color = "#e74c3c" if item['type'] == 'error' else "#f1c40f" if item['type'] == 'warning' else "#2ecc71"
        st.markdown(f"""
        <div class="news-card" style="border-left-color: {color};">
            <span style="color: #7f8c8d; font-size: 0.9em; font-weight: 600;">🕒 {item['time']}</span><br>
            <h4 style="margin-top: 5px;">
                <a href="{item.get('url', '#')}" target="_blank" style="color: #2c3e50; text-decoration: none; border-bottom: 1px dotted #2c3e50;">
                    {item['alert']} ↗
                </a>
            </h4>
        </div>
        """, unsafe_allow_html=True)
