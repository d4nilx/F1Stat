from data.loader import load_session
from visualization.charts import plot_positions
from config import F1_YEAR

session = load_session(F1_YEAR, 'Monaco')
plot_positions(session)