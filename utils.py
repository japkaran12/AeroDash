import pandas as pd

def format_aircraft_row(r):
    return {
        "icao24": r.get("icao24") or r.get("ICAO24") or "",
        "callsign": (r.get("callsign") or "").strip(),
        "lat": r.get("lat") or r.get("latitude") or None,
        "lon": r.get("lon") or r.get("longitude") or None,
        "alt_m": r.get("alt_m") or r.get("baro_altitude") or None,
        "velocity": r.get("velocity") or r.get("speed") or None,
        "origin_country": r.get("origin_country") or ""
    }
