import requests
import pandas as pd
from datetime import datetime, timedelta
from astropy.time import Time
import os

# Define USNO API endpoint
USNO_API_URL = "https://aa.usno.navy.mil/api/moon/phases/year/{year}"

# Set date range (last 5 years)
start_year = datetime.today().year - 5
end_year = datetime.today().year

# Create a list to store lunar data
lunar_data = []

def fetch_from_usno(year):
    """Fetch lunar phases from the USNO API."""
    try:
        print(f"📡 Fetching lunar data for {year} from USNO API...")
        response = requests.get(USNO_API_URL.format(year=year), timeout=10)

        if response.status_code != 200 or not response.text.strip():
            print(f"❌ USNO API returned status {response.status_code} for {year}")
            return None  # API failed

        data = response.json()
        if "phasedata" not in data:
            print(f"⚠️ Unexpected USNO API response for {year}")
            return None  # Unexpected response

        return [{"Date": entry["date"], "Phase": entry["phase"]} for entry in data["phasedata"]]

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error for {year}: {e}")
        return None  # API failure

def calculate_lunar_phase(date):
    """Compute lunar phase using AstroPy if API fails."""
    moon_phases = {
        0: "New Moon", 1: "Waxing Crescent", 2: "First Quarter", 3: "Waxing Gibbous",
        4: "Full Moon", 5: "Waning Gibbous", 6: "Last Quarter", 7: "Waning Crescent"
    }
    moon_phase_number = int((Time(date).mjd - Time("2000-01-06").mjd) % 29.53 // 3.69)
    return moon_phases[moon_phase_number]

def generate_local_moon_data():
    """Generate lunar phases locally if the API fails."""
    print("🔄 Switching to local lunar phase calculation (AstroPy)...")
    start_date = datetime.today() - timedelta(days=5 * 365)
    date_range = [start_date + timedelta(days=i) for i in range(5 * 365)]
    
    return [{"Date": date.strftime("%Y-%m-%d"), "Phase": calculate_lunar_phase(date)} for date in date_range]

# Fetch data for each year, or fallback to local computation
for year in range(start_year, end_year + 1):
    data = fetch_from_usno(year)
    if data:
        lunar_data.extend(data)

# If API failed for all years, use local lunar phase calculation
if not lunar_data:
    lunar_data = generate_local_moon_data()

# Convert to DataFrame and save to CSV
df = pd.DataFrame(lunar_data)
df["Date"] = pd.to_datetime(df["Date"]).dt.date
df.to_csv("data/lunar_phases.csv", index=False)

print("✅ Lunar phases saved to data/lunar_phases.csv")