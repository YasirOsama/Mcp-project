import streamlit as st
import requests

# 🌍 App Title and Config
st.set_page_config(page_title="Live Weather App", page_icon="⛅")
st.title("🌦️ Live Weather App")

# 📍 API Key (replace with your own)
API_KEY = "d1994e4751b34c3b9b6111620250207"  # ✅ Use your valid key
BASE_URL = "http://api.weatherapi.com/v1/current.json"

# 🏙️ City Input
city = st.text_input("Enter City Name", placeholder="e.g. Karachi")

# 🔍 Get Weather Info
if st.button("Check Weather"):
    if city.strip():
        # ✅ Request
        url = f"{BASE_URL}?key={API_KEY}&q={city}"
        response = requests.get(url)

        try:
            data = response.json()

            if response.status_code == 200 and "current" in data:
                location = data['location']
                current = data['current']

                st.success(f"Weather in {location['name']}, {location['country']}")
                st.write(f"🌡️ Temperature: {current['temp_c']}°C")
                st.write(f"☁️ Condition: {current['condition']['text']}")
                st.image(current['condition']['icon'])
                st.write(f"💧 Humidity: {current['humidity']}%")
                st.write(f"🌬️ Wind: {current['wind_kph']} km/h")
            else:
                st.error("❌ City not found or API limit exceeded.")
                st.code(data, language="json")  # ✅ Show actual error

        except Exception as e:
            st.error("⚠️ Failed to process the API response.")
            st.code(str(e))
    else:
        st.warning("⚠️ Please enter a city name.")



