# 🚨 AI Emergency Resource Finder (Hackathon Build)

A fully local, Deep-Learning powered Emergency Dispatch system that understands the context of free-form emergency texts and voice notes automatically prioritizing and routing to life-saving infrastructure.

## 🌟 Key Features
- **Local AI Intent Parsing:** Driven by `llama3.2` locally via Ollama. It understands panic, determining severity (`Critical/Medium`) and classifying the emergency type without relying on keyword matching.
- **Microphone Support:** Integrates Python `SpeechRecognition` to instantly transcribe emergency live-audio via Streamlit.
- **Multilingual Support:** Recognizes and translates regional accents natively. 
- **Live World Mapping (No Mock Data):** Queries OpenStreetMap's Overpass APIs globally to instantly locate the closest hospitals, fire responders, and police units precisely plotted via geographic multi-dimensional distance (`Haversine`).
- **Live RSS News:** Connects to the GDACS XML APIs to show real global disaster bulletins. 

## ⚙️ Installation & Setup (Local)

1. Ensure Python 3.10+ is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install and run [Ollama](https://ollama.com/) locally. Pull the required Llama 3.2 model:
   ```bash
   ollama run llama3.2:latest
   ```

## 🚀 Running the App
Once Ollama is running in the background, launch the Streamlit dashboard:
```bash
streamlit run app.py
```
View the Dispatch Center at `http://localhost:8501`.

*Developed for the Hackathon.*
