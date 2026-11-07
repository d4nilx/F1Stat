import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

def plot_track_speed(session, driver):
    if isinstance(driver, str):
        drivers = [driver]
    else:
        drivers = driver

    driver_telemetry = []
    for current_driver in drivers:
        lap = session.laps.pick_drivers(current_driver).pick_fastest()
        if lap.empty:
            print(f'No lap data found for {current_driver}')
            continue
        tel = lap.get_telemetry()
        if tel.empty or 'Speed' not in tel.columns:
            print(f'No telemetry found for {current_driver}')
            continue
        driver_telemetry.append((current_driver, tel))

    if not driver_telemetry:
        print('No telemetry data found for the selected drivers.')
        return

    all_speeds = np.concatenate([
        tel['Speed'].values for _, tel in driver_telemetry
    ])
    norm = plt.Normalize(all_speeds.min(), all_speeds.max())

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')

    for _, tel in driver_telemetry:
        x = tel['X'].values
        y = tel['Y'].values
        speed = tel['Speed'].values

        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        lc = LineCollection(segments, cmap='RdYlGn', norm=norm, linewidth=3)
        lc.set_array(speed[:-1])
        ax.add_collection(lc)

    cbar = fig.colorbar(lc, ax=ax)
    cbar.set_label('Speed (km/h)', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')

    ax.autoscale()
    ax.axis('off')
    driver_names = ', '.join(d for d, _ in driver_telemetry)
    ax.set_title(
        f'{session.event["EventName"]} {session.event.year} — {driver_names} — Speed',
        color='white', fontsize=14
    )

    plt.tight_layout()
    plt.show()
