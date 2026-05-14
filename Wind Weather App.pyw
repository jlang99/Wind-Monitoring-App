from tkinter import *
from tkinter import messagebox
import datetime as dt
import requests
import re
import json
from PIL import ImageTk, Image
import ctypes, os, sys
from collections import Counter
import threading
from googleapiclient.discovery import build

# Add the parent directory ('NCC Automations') to the Python path
# This allows us to import the 'PythonTools' package from there.
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from PythonTools import SITES_CONFIG, get_google_credentials


POD_SHEET_ID = "1JJuRhdVz5kirThENxUkCup5zwCvmZM9Rc9Tw65U9rRw"
regions = {
    "NC Local Region":        {"Warbler", "CDIA", "Violet"},
    "NC North Region":        {"Hayes", "Longleaf Pine"},
    "NC Piedmont Region":     {"Washington", "Thunderhead"},
    "NC Raleigh Region":      {"Cougar", "Wellons", "Williams"},
    "NC Fayetteville Region": {"Harrison", "Van Buren", "Gray Fox", "Holly Swamp", "Elk"},
    "NC Eastern Region":      {"Conetoe", "Wayne I", "Wayne II", "Wayne III", "Harding", "PG", "Freight Line", "Duplin", "Hickory"},
    "SC Tip Region":          {"Bluebird"},
    "SC Piedmont Region":     {"Hickson", "Ogburn", "McLean", "Shorthorn"},
    "Darlington Region":      {"Bishopville II", "Jefferson", "Marshall", "Tedder", "Whitehall"},
    "SC Coastal Region":      {"Cherry", "Cardinal", "Sunflower", "Whitetail"},
    "Georgia Region":         {"Bulloch 1A", "Bulloch 1B", "Richmond", "Lily"},
    "Georgia Mainland Region":{"Upson"},
}

service_tech = {
    "NC Local Region":        "Isaac Million",
    "NC North Region":        "Isaac Million",
    "NC Piedmont Region":     "Isaac Million",
    "NC Raleigh Region":      "Jon Wieber",
    "NC Fayetteville Region": "Thorne Locklear",
    "NC Eastern Region":      "Jon Wieber/Thorne Locklear",
    "SC Tip Region":          "Isaac Million",
    "SC Piedmont Region":     "Parker Wilson",
    "Darlington Region":      "Parker Wilson",
    "SC Coastal Region":      "Parker Wilson",
    "Georgia Region":         "Zach Duggan",
    "Georgia Mainland Region":"Zach Duggan",
}

class SolarSite:
    def __init__(self, name, var_name, lat, lon, localx, localy, has_tracker):
        self.name = name
        self.var_name = var_name
        self.lat = lat
        self.lon = lon
        self.localx = localx
        self.localy = localy
        self.has_tracker = has_tracker
        self.station = None
        self.gridx = None
        self.gridy = None
        
    def fetch_grid_points(self):
        if not self.lat or not self.lon:
            return False
        url = f"https://api.weather.gov/points/{self.lat},{self.lon}"
        headers = {
            'Content-Type': 'application/ld+json',
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.station = data.get('properties', {}).get('gridId')
                self.gridx = data.get('properties', {}).get('gridX')
                self.gridy = data.get('properties', {}).get('gridY')
                return True
            else:
                print(f"Grid points API for {self.name} failed: HTTP {response.status_code} \n {response.text}")
        except Exception as e:
            print(f"Error fetching grid points for {self.name}: {e}")
        return False

    def make_windapi_request(self):
        if not self.station or self.gridx is None or self.gridy is None:
            if not self.fetch_grid_points():
                return None
        url = f"https://api.weather.gov/gridpoints/{self.station}/{self.gridx},{self.gridy}/forecast"
        headers = {
            'Content-Type': 'application/ld+json',
        }
        try:
            return requests.get(url, headers=headers, timeout=10)
        except Exception as e:
            print(f"Error making forecast API request for {self.name}: {e}")
            return None

# --- Color Palette for Weather Conditions ---
# Sunny/Clear Scale (Yellows)
SUNNY = '#FFD700'          # Gold - For clear, sunny days
MOSTLY_SUNNY = '#FAFAD2'    # LightGoldenrodYellow - Predominantly sunny
PARTLY_SUNNY = '#EEE8AA'    # PaleGoldenrod - Sun is present but not dominant

# Cloudy/Transitional Scale (Greys/Muted Tones)
MIXED_CONDITIONS = '#D8D8BF' # Pale, muted beige for sun-to-cloud/rain transitions
PARTLY_CLOUDY = '#D3D3D3'    # LightGray - a neutral cloudy state
MOSTLY_CLOUDY = '#A9A9A9'    # DarkGray - Overcast is likely

# Precipitation Scale (Blues/Slates)
SLIGHT_CHANCE_RAIN = '#B0E0E6' # PowderBlue - Low probability of rain
CHANCE_RAIN = '#87CEEB'        # SkyBlue - A definite chance of rain
RAIN_LIKELY = '#4682B4'        # SteelBlue - Rain is probable
THUNDERSTORMS = '#778899'       # LightSlateGray - Storms are possible
HEAVY_THUNDERSTORMS = '#2F4F4F' # DarkSlateGray - Severe storms are likely
ICY_BLUE = '#ADD8E6'           # LightBlue, for frost
SNOW = '#ecfffd'
LIGHT_SNOW = '#ffffff'
HEAVY_SNOW = "#d0eceb"
SMOKE = '#C8C8C8'              # Smoky gray


def get_weather_color(short_forecast):
    """
    Determines a background color based on keywords in the weather forecast.
    Keywords are checked in order of priority (most severe to least severe).
    If the forecast contains 'then', it only considers the conditions *before* it.
    """
    # Convert forecast to lowercase for case-insensitive matching
    forecast = short_forecast.lower()

    # Check for smoke anywhere in the forecast first (highest priority)
    if 'smoke' in forecast:
        return SMOKE

    # If 'then' is in the forecast, only consider the part before it
    if ' then ' in forecast:
        primary_forecast = forecast.split(' then ')[0]
    else:
        primary_forecast = forecast

    # This list is ordered by priority. The first keyword found determines the color.
    weather_keywords = [
        # Highest priority: Storms and severe weather
        ("thunderstorms", HEAVY_THUNDERSTORMS),
        ("snow", SNOW),
        ("heavy snow", HEAVY_SNOW),
        ("light snow", LIGHT_SNOW),
        

        # Next priority: High probability of rain
        ("rain likely", RAIN_LIKELY),
        ("rain", RAIN_LIKELY),
        ("heavy rain", RAIN_LIKELY),
        ("sleet", RAIN_LIKELY),
        

        # Next priority: A definite chance of precipitation
        ("chance rain", CHANCE_RAIN),
        ("light rain", CHANCE_RAIN),
        ("rain showers", CHANCE_RAIN),
        ("scattered showers", CHANCE_RAIN),
        ("chance sleet", CHANCE_RAIN),
        

        # Next priority: Low or slight chance of precipitation
        ("slight chance", SLIGHT_CHANCE_RAIN),
        ("isolated showers", SLIGHT_CHANCE_RAIN),
        ("drizzle", SLIGHT_CHANCE_RAIN),
        ("chance light rain", SLIGHT_CHANCE_RAIN),


        # Next priority: Obscured or overcast conditions
        ("fog", PARTLY_CLOUDY),
        ("mostly cloudy", MOSTLY_CLOUDY),
        ("cloudy", MOSTLY_CLOUDY), # General "cloudy" as a fallback
        ("frost", ICY_BLUE),

        # Next priority: Mixed sun and clouds
        ("partly sunny", PARTLY_SUNNY),
        ("partly cloudy", PARTLY_CLOUDY), # Catches "partly cloudy" specifically

        # Lowest priority: Predominantly clear
        ("mostly sunny", MOSTLY_SUNNY),
        ("mostly clear", MOSTLY_SUNNY),
        ("sunny", SUNNY),
        ("clear", SUNNY),
    ]

    # Find the first matching keyword in the primary forecast and return its color
    for keyword, color in weather_keywords:
        if keyword in primary_forecast:
            return color

    # If no keywords match, return a neutral default color
    messagebox.showinfo(title="NCC Weather App New Function", message=f"Color not found for {forecast}")
    return MIXED_CONDITIONS

warningspdlower = 30
warningspdupper = 34
gustwarninglow = 36
gustwarningup = 39

stowspd = 35
guststowspd = 40

site_data_dict = {}

def get_wind_speed(site_obj, prev_weather_colors=None):
    gust1 = gust2 = gust3 = gust4 = spd1 = spd2 = spd3 = spd4 = None
    weather_color = 'pink'
    weather_data_response = site_obj.make_windapi_request()
    
    if weather_data_response and weather_data_response.status_code == 200:
        weather_data = weather_data_response.json()

        #See the output from the API response. 
        #if site_obj.name == "Cherry":
        #    print(json.dumps(weather_data, indent=4))
        
        periods = weather_data['properties']['periods']

        for i, period in enumerate(periods[:4], start=1):
            period_name = f"{period['name']}:"
            if i == 1:
                forecast_now = period['shortForecast']
                weather_color = get_weather_color(forecast_now)
                if site_obj.has_tracker is False:
                    globals()[f'{site_obj.var_name}lbl'].config(bg=weather_color)

                
                with open(f"G:\\Shared drives\\O&M\\NCC Automations\\Daily Automations\\Weather Data\\{site_obj.name} Weather Forecast.txt", "w") as file:
                    file.write(f"{dt.datetime.now()}\n{period_name:<18} {period['detailedForecast']}")
            else:
                with open(f"G:\\Shared drives\\O&M\\NCC Automations\\Daily Automations\\Weather Data\\{site_obj.name} Weather Forecast.txt", "a") as file:
                    file.write(f"\n{period_name:<18} {period['detailedForecast']}")

            speed_match = re.search(r'(\d+) mph', period['windSpeed'])
            gust_match = re.search(r'gusts as high as (\d+) mph', period['detailedForecast'])
            if speed_match:
                speed = speed_match.group(1)
            else:
                speed = "N/A"
            if gust_match:
                gust = gust_match.group(1)
            else:
                gust = 0

            if i == 1:
                spd1 = speed
                gust1 = gust
            elif i == 2:
                spd2 = speed
                gust2 = gust

            elif i == 3:
                gust3 = gust
                spd3 = speed
            elif i == 4:
                spd4 = speed
                gust4 = gust

    else:
        if weather_data_response:
            print(weather_data_response.status_code, '\n', weather_data_response.text)
        else:
            print(f"Failed to fetch forecast API response for {site_obj.name}")
        spd1 = "N/A"
        spd2 = "N/A"
        spd3 = "N/A"
        spd4 = "N/A"
        gust1 = "N/A"
        gust2 = "N/A"
        gust3 = "N/A"
        gust4 = "N/A"
        if prev_weather_colors and site_obj.name in prev_weather_colors:
            weather_color = prev_weather_colors[site_obj.name]

    site_data_dict[site_obj.name] = [spd1, spd2, spd3, spd4, gust1, gust2, gust3, gust4, weather_color]


def generate_regional_summary():
    # Representative sites for Inland and Coastal regions to generate a general blurb
    # Will need to fine tune this to improve the teams operatonal efficiency. This is simply and example of can be generated from the Weather API we utilize.
    rep_sites = {
        'Inland': 'Harrison',
        'Coastal': 'Cardinal'
    }
    
    summaries = {}
    
    for region, site_name in rep_sites.items():
        # Find site data in the global site_objects list
        site_info = next((s for s in site_objects if s.name == site_name), None)
        if not site_info:
            summaries[region] = "Site configuration not found."
            continue
            
        try:
            response = site_info.make_windapi_request()
            if not response or response.status_code != 200:
                summaries[region] = "Data unavailable."
                continue
                
            data = response.json()
            periods = data['properties']['periods']
            
            # Filter for daytime periods to get daily highs and general conditions for the next 7 days
            day_periods = [p for p in periods if p['isDaytime']]
            
            if not day_periods:
                summaries[region] = "No forecast data available."
                continue
                
            temps = [p['temperature'] for p in day_periods]
            min_temp = min(temps)
            max_temp = max(temps)
            
            conditions = [p['shortForecast'] for p in day_periods]
            
            # Find the most common weather condition (e.g., "Mostly Sunny")
            common_cond = Counter(conditions).most_common(1)[0][0]
            
            # Identify days with precipitation keywords
            rain_days = []
            for p in day_periods:
                desc = p['shortForecast'].lower()
                if any(x in desc for x in ["rain", "showers", "thunderstorms", "drizzle", "snow"]):
                    rain_days.append(p['name'])
            
            rain_str = ""
            if rain_days:
                if len(rain_days) > 4:
                    rain_str = "Chance of precipitation throughout the week."
                else:
                    rain_str = f"Chance of precipitation on {', '.join(rain_days)}."
            else:
                rain_str = "Little to no precipitation expected."
                
            summary = f"Highs {min_temp}-{max_temp}°F. Predominantly {common_cond.lower()}. {rain_str}"
            summaries[region] = summary
            
        except Exception as e:
            summaries[region] = f"Error generating forecast: {e}"

    # Construct the final message, merging if conditions are identical
    if summaries.get('Inland') == summaries.get('Coastal'):
        final_text = f"Regional Forecast (Next 7 Days):\n\n{summaries['Inland']}"
    else:
        final_text = f"Regional Forecast (Next 7 Days):\n\nInland (e.g., NC Piedmont):\n{summaries.get('Inland', 'N/A')}\n\nCoastal (e.g., NC/SC Coast):\n{summaries.get('Coastal', 'N/A')}"
        
    messagebox.showinfo("7-Day Regional Forecast", final_text)

def _parse_sheet_date(date_str):
    s = date_str.strip().split(' ')[0]
    parts = re.split(r'[/\-]', s)
    if len(parts) == 3:
        try:
            if len(parts[0]) == 4:
                return dt.date(int(parts[0]), int(parts[1]), int(parts[2]))
            else:
                year = int(parts[2])
                if year < 100:
                    year += 2000
                return dt.date(year, int(parts[0]), int(parts[1]))
        except Exception:
            pass
    return None


def get_site_forecast_for_date(site_obj, target_date):
    response = site_obj.make_windapi_request()
    if not response or response.status_code != 200:
        return None
    periods = response.json().get('properties', {}).get('periods', [])
    for period in periods:
        try:
            period_date = dt.datetime.fromisoformat(period['startTime']).date()
        except Exception:
            continue
        if period_date == target_date and period.get('isDaytime', True):
            speed_match = re.search(r'(\d+) mph', period.get('windSpeed', ''))
            wind_spd = speed_match.group(1) if speed_match else "N/A"
            gust_match = re.search(r'gusts as high as (\d+) mph', period.get('detailedForecast', ''))
            parts = [period.get('shortForecast', 'N/A'), f"Wind: {wind_spd} mph"]
            if gust_match:
                parts.append(f"Gusts: {gust_match.group(1)} mph")
            return ", ".join(parts)
    return None


def write_pod_weather():
    def _run():
        try:
            start_date = dt.date.today()
            end_date = dt.date.today() + dt.timedelta(days=7)
            tabs_to_check = sorted({f"Wk {start_date.isocalendar()[1]}", f"Wk {end_date.isocalendar()[1]}"})
            print(f"[POD Weather] Date range: {start_date} to {end_date} | Tabs to check: {tabs_to_check}")

            creds = get_google_credentials()
            service = build('sheets', 'v4', credentials=creds)

            meta = service.spreadsheets().get(spreadsheetId=POD_SHEET_ID).execute()
            tab_names = [s['properties']['title'] for s in meta['sheets']]
            print(f"[POD Weather] Tabs found: {tab_names}")

            site_lookup = {s.name: s for s in site_objects}
            total_updates = 0

            for sheet_tab in tabs_to_check:
                if sheet_tab not in tab_names:
                    print(f"[POD Weather] Tab '{sheet_tab}' not found, skipping.")
                    continue

                result = service.spreadsheets().values().get(
                    spreadsheetId=POD_SHEET_ID,
                    range=f"'{sheet_tab}'!B1:F500"
                ).execute()
                rows = result.get('values', [])
                print(f"[POD Weather] Tab '{sheet_tab}': {len(rows)} rows read")

                updates = []
                current_section_date = None

                for row_idx, row in enumerate(rows):
                    date_f = row[4].strip() if len(row) > 4 else ""

                    if date_f:
                        parsed = _parse_sheet_date(date_f)
                        if parsed:
                            current_section_date = parsed
                            print(f"[POD Weather] Row {row_idx + 1}: New section date -> {current_section_date}")
                            continue  # Confirmed date header row, skip
                        # F has content but isn't a date — still read B and D below

                    if current_section_date is None or not (start_date <= current_section_date <= end_date):
                        continue

                    site_b = row[0].strip() if len(row) > 0 else ""
                    site_d = row[2].strip() if len(row) > 2 else ""
                    print(f"[POD Weather] Row {row_idx + 1} (section {current_section_date}): B='{site_b}' D='{site_d}'")

                    site_b_obj = site_lookup.get(site_b)
                    site_d_obj = site_lookup.get(site_d)
                    print(f"[POD Weather]   Site B '{site_b}': {'FOUND' if site_b_obj else 'not found'}")
                    print(f"[POD Weather]   Site D '{site_d}': {'FOUND' if site_d_obj else 'not found'}")
                    if not site_b_obj and not site_d_obj:
                        continue

                    b_weather = get_site_forecast_for_date(site_b_obj, current_section_date) if site_b_obj else ""
                    d_weather = get_site_forecast_for_date(site_d_obj, current_section_date) if site_d_obj else ""
                    print(f"[POD Weather]   B weather: {b_weather}")
                    print(f"[POD Weather]   D weather: {d_weather}")

                    if not b_weather and not d_weather:
                        continue

                    updates.append({
                        'range': f"'{sheet_tab}'!H{row_idx + 1}:K{row_idx + 1}",
                        'values': [[
                            site_b if b_weather else "", b_weather or "",
                            site_d if d_weather else "", d_weather or ""
                        ]]
                    })
                    print(f"[POD Weather]   Queued write to {sheet_tab}!H{row_idx + 1}:K{row_idx + 1}")

                if updates:
                    service.spreadsheets().values().batchUpdate(
                        spreadsheetId=POD_SHEET_ID,
                        body={'valueInputOption': 'USER_ENTERED', 'data': updates}
                    ).execute()
                    total_updates += len(updates)
                    print(f"[POD Weather] Wrote {len(updates)} row(s) to '{sheet_tab}'")

            if total_updates:
                messagebox.showinfo("POD Weather", f"Updated {total_updates} row(s) across {len(tabs_to_check)} tab(s).")
            else:
                messagebox.showinfo("POD Weather", f"No matching rows found for {start_date.strftime('%m/%d/%Y')} – {end_date.strftime('%m/%d/%Y')}.")

        except Exception as e:
            messagebox.showerror("POD Weather", f"Error: {e}")
            print(f"POD weather error: {e}")

    threading.Thread(target=_run, daemon=True).start()


def write_forecast_sheet():
    def _run():
        try:
            today = dt.date.today()
            forecast_dates = [today + dt.timedelta(days=i) for i in range(7)]
            NUM_COLS = 8  # Col A (site) + 7 day columns

            # Pre-fetch all site forecasts keyed by site name
            site_forecasts = {}
            for site_obj in site_objects:
                response = site_obj.make_windapi_request()
                if response and response.status_code == 200:
                    periods = response.json().get('properties', {}).get('periods', [])
                    date_fc = {}
                    for period in periods:
                        try:
                            period_date = dt.datetime.fromisoformat(period['startTime']).date()
                        except Exception:
                            continue
                        if period.get('isDaytime', True) and period_date not in date_fc:
                            speed_match = re.search(r'(\d+) mph', period.get('windSpeed', ''))
                            wind_spd = speed_match.group(1) if speed_match else "N/A"
                            gust_match = re.search(r'gusts as high as (\d+) mph', period.get('detailedForecast', ''))
                            short_fc = period.get('shortForecast', 'N/A')
                            parts = [short_fc, f"Wind: {wind_spd} mph"]
                            if gust_match:
                                parts.append(f"Gusts: {gust_match.group(1)} mph")
                            date_fc[period_date] = (", ".join(parts), short_fc)
                    site_forecasts[site_obj.name] = date_fc
                else:
                    site_forecasts[site_obj.name] = None

            # Build rows grouped by region; track formatting targets
            header_row = ["Site"] + [d.strftime("%a %m/%d") for d in forecast_dates]
            rows = [header_row]
            cell_colors = {}       # (row_idx, col_idx) -> hex color
            region_header_rows = []  # row indices of region label rows
            region_ranges = []       # (start_row_idx, end_row_idx) exclusive, for border

            for region_name, site_names in regions.items():
                region_start = len(rows)
                rows.append([region_name, service_tech.get(region_name, "")] + [""] * 6)
                region_header_rows.append(len(rows) - 1)

                for site_obj in (s for s in site_objects if s.name in site_names):
                    row_idx = len(rows)
                    row_data = [site_obj.name]
                    fc_data = site_forecasts.get(site_obj.name)
                    if fc_data:
                        for col_idx, d in enumerate(forecast_dates, start=1):
                            if d in fc_data:
                                display, short_fc = fc_data[d]
                                row_data.append(display)
                                cell_colors[(row_idx, col_idx)] = get_weather_color(short_fc)
                            else:
                                row_data.append("N/A")
                    else:
                        row_data.extend(["N/A"] * 7)
                    rows.append(row_data)

                region_ranges.append((region_start, len(rows)))

            # Spacing row + color legend
            rows.append([""] * NUM_COLS)

            legend_entries = [
                ("Sunny / Clear",          SUNNY),
                ("Mostly Sunny",           MOSTLY_SUNNY),
                ("Partly Sunny",           PARTLY_SUNNY),
                ("Partly Cloudy / Fog",    PARTLY_CLOUDY),
                ("Mostly Cloudy",          MOSTLY_CLOUDY),
                ("Frost",                  ICY_BLUE),
                ("Slight Chance Rain",     SLIGHT_CHANCE_RAIN),
                ("Chance of Rain",         CHANCE_RAIN),
                ("Rain Likely",            RAIN_LIKELY),
                ("Thunderstorms",          HEAVY_THUNDERSTORMS),
                ("Snow",                   SNOW),
                ("Heavy Snow",             HEAVY_SNOW),
                ("Smoke",                  SMOKE),
            ]

            legend_header_row = len(rows)
            rows.append(["Legend"] + [""] * (NUM_COLS - 1))
            region_header_rows.append(legend_header_row)

            for label, color in legend_entries:
                row_idx = len(rows)
                rows.append([label, ""] + [""] * (NUM_COLS - 2))
                cell_colors[(row_idx, 1)] = color

            # Connect and get/create the sheet tab
            creds = get_google_credentials()
            service = build('sheets', 'v4', credentials=creds)

            meta = service.spreadsheets().get(spreadsheetId=POD_SHEET_ID).execute()
            tab_name = "Weather Forecast"
            existing_sheets = meta['sheets']
            existing_names = [s['properties']['title'] for s in existing_sheets]

            if tab_name not in existing_names:
                add_resp = service.spreadsheets().batchUpdate(
                    spreadsheetId=POD_SHEET_ID,
                    body={'requests': [{'addSheet': {'properties': {'title': tab_name}}}]}
                ).execute()
                sheet_id = add_resp['replies'][0]['addSheet']['properties']['sheetId']
            else:
                sheet_id = next(s['properties']['sheetId'] for s in existing_sheets if s['properties']['title'] == tab_name)

            service.spreadsheets().values().clear(
                spreadsheetId=POD_SHEET_ID, range=f"'{tab_name}'!A:Z"
            ).execute()
            service.spreadsheets().values().update(
                spreadsheetId=POD_SHEET_ID,
                range=f"'{tab_name}'!A1",
                valueInputOption='USER_ENTERED',
                body={'values': rows}
            ).execute()

            # --- Formatting ---
            def hex_to_rgb(hex_color):
                h = hex_color.lstrip('#')
                return int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0

            BLACK = {"red": 0.0, "green": 0.0, "blue": 0.0}
            MEDIUM = {"style": "SOLID_MEDIUM", "color": BLACK}
            format_requests = []

            # Weather cell background colors
            for (row_idx, col_idx), hex_color in cell_colors.items():
                r, g, b = hex_to_rgb(hex_color)
                format_requests.append({"repeatCell": {
                    "range": {"sheetId": sheet_id,
                               "startRowIndex": row_idx, "endRowIndex": row_idx + 1,
                               "startColumnIndex": col_idx, "endColumnIndex": col_idx + 1},
                    "cell": {"userEnteredFormat": {"backgroundColor": {"red": r, "green": g, "blue": b}}},
                    "fields": "userEnteredFormat.backgroundColor"
                }})

            # Region header rows: gray background + bold text spanning all columns
            for row_idx in region_header_rows:
                format_requests.append({"repeatCell": {
                    "range": {"sheetId": sheet_id,
                               "startRowIndex": row_idx, "endRowIndex": row_idx + 1,
                               "startColumnIndex": 0, "endColumnIndex": NUM_COLS},
                    "cell": {"userEnteredFormat": {
                        "backgroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0},
                        "textFormat": {"bold": True}
                    }},
                    "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.textFormat.bold"
                }})

            # Solid medium border box around each region block
            for start_row, end_row in region_ranges:
                format_requests.append({"updateBorders": {
                    "range": {"sheetId": sheet_id,
                               "startRowIndex": start_row, "endRowIndex": end_row,
                               "startColumnIndex": 0, "endColumnIndex": NUM_COLS},
                    "top": MEDIUM, "bottom": MEDIUM, "left": MEDIUM, "right": MEDIUM
                }})

            if format_requests:
                service.spreadsheets().batchUpdate(
                    spreadsheetId=POD_SHEET_ID,
                    body={'requests': format_requests}
                ).execute()

            messagebox.showinfo("Weather Forecast", f"Forecast table updated for {len(site_objects)} sites across {len(regions)} regions.")

        except Exception as e:
            messagebox.showerror("Weather Forecast", f"Error: {e}")
            print(f"Forecast sheet error: {e}")

    threading.Thread(target=_run, daemon=True).start()


def update_gui(site_obj):
    site = site_obj.name
    var = site_obj.var_name
    has_tracker = site_obj.has_tracker
    
    globals()[f'{var}legend'].config(bg=site_data_dict[site][8])
    if has_tracker:
        if site_data_dict[site][0] != "N/A": #Avoids overwriting a successful data pull with N/A
            globals()[f'{var}curspd'].config(text=site_data_dict[site][0])
            globals()[f'{var}nxtspd'].config(text=site_data_dict[site][1])
            globals()[f'{var}3rdspd'].config(text=site_data_dict[site][2])
            globals()[f'{var}finalspd'].config(text=site_data_dict[site][3])
            globals()[f'{var}gcurspd'].config(text=site_data_dict[site][4])
            globals()[f'{var}gnxtspd'].config(text=site_data_dict[site][5])
            globals()[f'{var}g3rdspd'].config(text=site_data_dict[site][6])
            globals()[f'{var}gfinalspd'].config(text=site_data_dict[site][7])
            
            cur_spd = int(site_data_dict[site][0])
            cur_gust = int(site_data_dict[site][4])
            is_stowed = globals().get(f'{var}override_var') and globals()[f'{var}override_var'].get()
            is_over_stow = cur_spd >= stowspd or cur_gust >= guststowspd

            if is_stowed:
                if is_over_stow:
                    bg_color = 'green'
                else:
                    bg_color = 'red'
            else:
                if is_over_stow:
                    bg_color = 'red'
                elif (warningspdlower <= cur_spd <= warningspdupper) or (gustwarninglow <= cur_gust <= gustwarningup):
                    bg_color = 'orange'
                elif (warningspdlower <= int(site_data_dict[site][1])) or (gustwarninglow <= int(site_data_dict[site][5])):
                    bg_color = 'orange'
                elif (warningspdlower <= int(site_data_dict[site][2]) <= warningspdupper) or (warningspdlower <= int(site_data_dict[site][3]) <= warningspdupper) or (gustwarninglow <= int(site_data_dict[site][6]) <= gustwarningup) or (gustwarninglow <= int(site_data_dict[site][7]) <= gustwarningup):
                    bg_color = 'yellow'
                else:
                    bg_color = 'green'

            for label_suffix in ['', 'data', 'lbl', 'lblwind', 'curspd', 'nxtspd', '3rdspd', 'finalspd', 'gcurspd', 'gnxtspd', 'g3rdspd', 'gfinalspd', 'lblgust', 'override_cb']:
                if f'{var}{label_suffix}' in globals():
                    globals()[f'{var}{label_suffix}'].config(bg=bg_color)


def get_data_then_update_gui():
    prev_weather_colors = {site: data[8] for site, data in site_data_dict.items()}
    globals()['site_data_dict'] = {}
    for site_obj in site_objects:
        get_wind_speed(site_obj, prev_weather_colors)

    for site_obj in site_objects:
        update_gui(site_obj)
    update_time = dt.datetime.now() + dt.timedelta(minutes=30)
    update_t = update_time.strftime("%H:%M")
    timenow = dt.datetime.now().strftime("%H:%M")
    globals()['updated'].config(text=f"Updated: {timenow} | Next: {update_t}")
    print("Updating in 30 Minutes...", update_t)
    root.after(1800000, get_data_then_update_gui)

def open_weather_forecast(site):
    os.startfile(f"G:\\Shared drives\\O&M\\NCC Automations\\Daily Automations\\Weather Data\\{site} Weather Forecast.txt")

def save_cb_states():
    state_dict = {}
    for site_obj in site_objects:
        if site_obj.has_tracker:
            var = site_obj.var_name
            if globals().get(f'{var}override_var'):
                state_dict[var] = globals()[f'{var}override_var'].get()
    
    with open(r"G:\Shared drives\O&M\NCC Automations\Daily Automations\Weather Data\checkbox_states.json", "w") as f:
        json.dump(state_dict, f)

def load_cb_states():
    file_path = r"G:\Shared drives\O&M\NCC Automations\Daily Automations\Weather Data\checkbox_states.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                state_dict = json.load(f)
                for site_obj in site_objects:
                    var = site_obj.var_name
                    state = state_dict.get(var)
                    if state is not None and globals().get(f'{var}override_var'):
                        globals()[f'{var}override_var'].set(state)
        except Exception as e:
            print(f"Error loading checkbox states: {e}")









myappid = 'NCC.Wind.Monitor.GUI'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

root = Tk()
root.title("NCC Weather App")
root.geometry("1920x1080")
root.iconbitmap(r"G:\Shared drives\O&M\NCC Automations\Icons\Wind.ico")

image_map = Image.open(r"G:\Shared drives\O&M\NCC Automations\Icons\NC, SC, GA Map.jpg").resize((1920, 1080))
map_tk = ImageTk.PhotoImage(image_map)

maplbl = Label(root, image=map_tk)
maplbl.place(x=0, y=0, relwidth=1, relheight=1)

# DEV BUTTON - remove when confirmed working
dev_pod_butt = Button(root, text="DEV: Update POD Weather", command=lambda: [write_pod_weather(), write_forecast_sheet()], bg='orange', font=('Arial', 10, 'bold'))
dev_pod_butt.place(x=5, y=5)

dataFrame1 = Frame(root)
dataFrame1.place(x=1685, y=490)

dataFrame2 = Frame(root)
dataFrame2.place(x=1445, y=490)

dataFrame3 = Frame(root)
dataFrame3.place(x=1205, y=490)

dataFrame4 = Frame(root)
dataFrame4.place(x=896, y=690)

nonTFrame = Frame(root)
nonTFrame.place(x=1860, y=5)

legend = LabelFrame(root)
legend.place(x=1690, y=290)

legendtitle = Label(legend, text=f"Legend | Units in Mph\nStow = Wind {stowspd}+ or Gusts {guststowspd} Mph\nWarning = Wind {warningspdlower}+ or Gust {gustwarninglow}+ Mph\nRed = Stow/Unstow Action Needed\nOrange = Warning\nYellow = Warning, Tomorrow\nCheckbox = Stowed")
legendtitle.pack()

#TimeStamps
updated = Label(legend, text= "Time Stamps Displayed Here")
updated.pack()

#Update Button
update_butt = Button(legend, text="Update Weather Data Now", command= lambda: get_data_then_update_gui(), bg='light green')
update_butt.pack(fill='x')

#Regional Forecast Button
regional_butt = Button(legend, text="7-Day Regional Forecast", command=generate_regional_summary, bg='light blue')
regional_butt.pack(fill='x', pady=2)


site_objects = []
for site_name, data in SITES_CONFIG.items():
    site_obj = SolarSite(site_name, data['var'], data['lat'], data['lon'], data['x'], data['y'], data['tracker'])
    site_objects.append(site_obj)

spd_wdth = 2
count=0
for site_obj in site_objects:
    site = site_obj.name
    var = site_obj.var_name
    localx = site_obj.localx
    localy = site_obj.localy
    tracker_site = site_obj.has_tracker
    #Placing Button Label on the Map
    globals()[var] = LabelFrame(root)
    globals()[var].place(x=localx, y=localy)
    globals()[f'{var}lbl'] = Button(globals()[var], text=site, command=lambda name=site: open_weather_forecast(name))
    globals()[f'{var}lbl'].pack()

    #Creating Legend for Map
    if tracker_site:
        if count < 11:
            parent_frame = dataFrame1
        elif count < 22:
            parent_frame = dataFrame2
        elif count < 33:
            parent_frame = dataFrame3
        else:
            parent_frame = dataFrame4
        globals()[f'{var}data'] = LabelFrame(parent_frame)
        frame = globals()[f'{var}data']
        frame.pack(anchor=W, fill= 'x')
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=2)
        
        globals()[f'{var}override_var'] = BooleanVar()
        globals()[f'{var}override_cb'] = Checkbutton(frame, variable=globals()[f'{var}override_var'], command=lambda s_obj=site_obj: [update_gui(s_obj), save_cb_states()])
        globals()[f'{var}override_cb'].grid(row=0, column=0, sticky=W, rowspan=2)

        globals()[f'{var}legend'] = Button(frame, text=site, command= lambda name=site: open_weather_forecast(name))
        globals()[f'{var}legend'].grid(row= 0, column= 1, sticky=W, rowspan=2)
        globals()[f'{var}lblwind'] = Label(frame, text= "Wind: ")
        globals()[f'{var}lblwind'].grid(row= 0, column= 2, sticky=E)
        globals()[f'{var}curspd'] = Label(frame, text= "N/A", width=spd_wdth)
        globals()[f'{var}curspd'].grid(row= 0, column= 3, sticky=E)
        globals()[f'{var}nxtspd'] = Label(frame, text= "N/A", width=spd_wdth)
        globals()[f'{var}nxtspd'].grid(row= 0, column= 4, sticky=E)
        globals()[f'{var}3rdspd'] = Label(frame, text= "N/A", width=spd_wdth)
        globals()[f'{var}3rdspd'].grid(row= 0, column= 5, sticky=E)
        globals()[f'{var}finalspd'] = Label(frame, text= "N/A", width=spd_wdth)
        globals()[f'{var}finalspd'].grid(row= 0, column= 6, sticky=E)

        globals()[f'{var}lblgust'] = Label(frame, text= "Gust: ")
        globals()[f'{var}lblgust'].grid(row= 1, column= 2, sticky=E)
        globals()[f'{var}gcurspd'] = Label(frame, text= "N/A", width=spd_wdth)
        globals()[f'{var}gcurspd'].grid(row= 1, column= 3, sticky=E)
        globals()[f'{var}gnxtspd'] = Label(frame, text= "N/A", width=spd_wdth)
        globals()[f'{var}gnxtspd'].grid(row= 1, column= 4, sticky=E)
        globals()[f'{var}g3rdspd'] = Label(frame, text= "N/A", width=spd_wdth)
        globals()[f'{var}g3rdspd'].grid(row= 1, column= 5, sticky=E)
        globals()[f'{var}gfinalspd'] = Label(frame, text= "N/A", width=spd_wdth)
        globals()[f'{var}gfinalspd'].grid(row= 1, column= 6, sticky=E)
        count+=1

    else:
        globals()[f'{var}legend'] = Button(nonTFrame, text=site, command= lambda name=site: open_weather_forecast(name))
        globals()[f'{var}legend'].pack(anchor=W, fill= 'x')


load_cb_states()
get_data_then_update_gui()
write_pod_weather()
write_forecast_sheet()
root.mainloop()
  
