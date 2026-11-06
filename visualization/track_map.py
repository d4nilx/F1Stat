import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

def plot_track_speed(session, driver):
    lap = session.laps.pick_drivers(driver).pick_fastest()
    tel = lap.get_telemetry()

    x = tel['X'].values
    y = tel['Y'].values
    speed = tel['Speed'].values

    #Lines
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')

    norm = plt.Normalize(speed.min(), speed.max())
    lc = LineCollection(segments, cmap='RdYlGn', norm=norm, linewidth=3)
    lc.set_array(speed)
    ax.add_collection(lc)

    cbar = fig.colorbar(lc, ax=ax)
    cbar.set_label('Speed (km/h)', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')

    ax.autoscale()
    ax.axis('off')
    ax.set_title(f'Monaco 2024 — {driver} — Speed',
                 color='white', fontsize=14)

    plt.tight_layout()
    plt.show()