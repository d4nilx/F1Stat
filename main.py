from data.loader import load_session
from visualization.charts import plot_positions
from config import F1_YEAR
from visualization.track_map import plot_track_speed

session = load_session(F1_YEAR, 'Monaco')
plot_positions(session)
plot_track_speed(session, 'LEC')