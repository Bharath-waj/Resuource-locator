# 💻 TECH STACK & ARCHITECTURE

The **Rescue AI** Emergency System leverages a modern, offline-capable, and privacy-first tech stack capable of understanding unstructured data through Deep Learning and querying live Global Information Systems.

---

### 1. 🧠 Core Artificial Intelligence (Local/Edge AI)
* **Ollama (Local AI Engine):** Hosts and runs large language models entirely offline for 100% privacy compliance and sub-second latency. No cloud API keys or external server dependencies.
* **Meta Llama 3.2 (Model):** Deep learning model optimized for reasoning. Natively parses free-form emergency texts to execute strict JSON extraction for intent classification (`Medical`, `Accident`, `Fire`) and severity assessment (`Low`, `Medium`, `Critical`).
* **Python SpeechRecognition:** Native audio pipeline enabling live voice-to-text translations from browser microphone streams. Transcribes localized accents seamlessly.

### 2. 🌍 Geospatial & Routing Intelligence
* **OpenStreetMap (OSM) Overpass API:** Real-world map database queries. Provides live, structured GIS metrics about nearby hospitals, police hubs, and fire stations without requiring dummy data.
* **Geopy (Nominatim):** Converts generic natural-language text inputs (e.g., "T Nagar, Chennai") into exact latitudinal and longitudinal coordinate integers instantly.
* **Haversine Math Processor:** Custom backend algorithms determining the spherical distance between the user's location and nearest retrieved OSM resources for priority ranking.

### 3. 🖥️ Frontend Architecture & User Interface
* **Streamlit Framework:** High velocity, pure-Python web component framework. Drives the single-page application (SPA), multi-tab navigation, and fluid state management.
* **Folium & Streamlit-Folium:** Embedded interactive radar mapping. Generates dynamic geographical overlays indicating the user origin versus dispatched destination coordinates.
* **Session State Reactivity:** Custom Streamlit data caching preventing DOM reloads upon map interactions, ensuring the deep-learning output remains robustly rendered.

### 4. 📰 Data Operations & Analytics Dashboard
* **Pandas:** Real-time data manipulation framework formatting historical disaster inferences into multi-dimensional aggregation views.
* **xml.etree (RSS DOM Parsing):** Consumes the live Web 2.0 RSS protocol from GDACS (Global Disaster Alert and Coordination System) continuously fetching global incidents on the "Live News Feed" asynchronously.

### 5. 🛠 Environment Dependencies
* `requests`
* `pandas`
* `folium`
* `geopy`
* `speechrecognition`
* `soundfile`
* `streamlit`
