import fastf1
import os
from config import CACHE_DIR

#Session loader
def load_session(year, circuit, session_type='R'):
    os.makedirs(CACHE_DIR, exist_ok=True)
    fastf1.Cache.configure(cache_dir=CACHE_DIR)

    session = fastf1.get_session(year, circuit, session_type)
    session.load(telemetry=True, laps=True, weather=False)
    return session