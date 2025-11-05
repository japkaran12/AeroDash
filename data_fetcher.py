import os
import json
import requests
from cachetools import TTLCache, cached

cache = TTLCache(maxsize=50, ttl=10)
SAMPLE = os.path.join("assets", "samples", "aircraft_sample.json")

@cached(cache)
def fetch_states(bbox: str = None, use_sample: bool = True):
    """
    Demo-first: if SAMPLE file exists, always return its contents (ignore bbox).
    This forces the app to show sample planes regardless of UI filters — for debugging/demo.
    """
    # If sample file exists, read it and return states_parsed
    if os.path.exists(SAMPLE):
        try:
            with open(SAMPLE, "rb") as f:
                raw = f.read()
            # decode robustly (strip BOM if present)
            try:
                text = raw.decode("utf-8-sig")
            except Exception:
                try:
                    text = raw.decode("utf-8")
                except Exception:
                    text = raw.decode("latin-1", errors="ignore")
            data = json.loads(text)
            return data.get("states_parsed", [])
        except Exception:
            # fallback: return empty list if sample can't be read
            return []

    # If sample missing, fall back to online fetch (preserve original behavior)
    url = "https://opensky-network.org/api/states/all"
    params = {}
    if bbox:
        params["bbox"] = bbox
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        payload = r.json()
        states = payload.get("states", [])
        out = []
        for s in states:
            out.append({
                "icao24": s[0],
                "callsign": s[1] or "",
                "origin_country": s[2] or "",
                "time_position": s[3],
                "last_contact": s[4],
                "lon": s[5],
                "lat": s[6],
                "baro_altitude": s[7],
                "on_ground": s[8],
                "velocity": s[9]
            })
        return out
    except Exception:
        return []

def fetch_weather(lat, lon):
    # demo synthetic weather
    if lat is None or lon is None:
        return {"temp_c": None, "pressure_hpa": None, "note": "demo"}
    temp = round(30 - (lat - 8) * 0.6, 1)
    if temp < -10: temp = -10
    if temp > 45: temp = 45
    base_pressure = 1013.25
    pressure = round(base_pressure - (lat - 20) * 0.6 + (lon - 78) * 0.05, 1)
    return {"temp_c": temp, "pressure_hpa": pressure, "note": "synthetic"}