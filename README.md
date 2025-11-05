# AeroDash

AeroDash is a simple Streamlit-based aerospace dashboard made for practice and college portfolio.  
It shows aircraft data (sample or real from OpenSky API), their location, altitude, speed, and basic stats on an interactive map.

---

## Setup

### 1. Clone or make folder
If you made the folder manually in VS Code then skip this step.

```bash
git clone https://github.com/your-username/AeroDash.git
cd AeroDash
2. Create virtual environment and install modules
bash
Copy code
python -m venv venv
venv\Scripts\activate   # on windows
# or
source venv/bin/activate  # on linux / mac
pip install -r requirements.txt
How to Run
bash
Copy code
streamlit run app.py
Then it will open automatically in your browser (something like http://localhost:8501).

If it does not open, go manually to that link in Chrome.

Features
Live or sample aircraft data (OpenSky API)

Interactive map view

Table with aircraft details

Weather lookup (demo)

Auto refresh option

Download CSV option

Simple stats panel

Folder Structure
pgsql
Copy code
AeroDash/
├─ app.py
├─ data_fetcher.py
├─ utils.py
├─ requirements.txt
├─ .gitignore
├─ README.md
├─ LICENSE
├─ assets/
│  └─ samples/
│     └─ aircraft_sample.json
└─ notebooks/
   └─ dev-notes.ipynb
Sample Data
If you don’t have internet or API access, the app loads sample data from
assets/samples/aircraft_sample.json.
You can add your own JSON with same structure.

Example structure:

json
Copy code
{
  "states_parsed": [
    {
      "icao24": "abc123",
      "callsign": "INDIGO",
      "origin_country": "India",
      "latitude": 28.61,
      "longitude": 77.23,
      "baro_altitude": 10000,
      "velocity": 250
    }
  ]
}
Notes
The OpenSky API sometimes gives limited data due to rate limits.

You can change bounding box in sidebar to see different areas.

Auto refresh helps to update live data without manual reload.

Default mode uses sample data for offline demo.

Requirements
Python 3.9 or above
Modules listed in requirements.txt

Made By
Japkaran Singh Arneja
Lovely Professional University
(Just a student project made for practice and portfolio)

License
MIT License — free to use and modify