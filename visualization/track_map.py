import fastf1.plotting
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

def plot_track_speed_comparison(session, drivers):
    fig, axes = plt.subplots(1, len(drivers), figsize=(12 * len(drivers), 8))
    fig.patch.set_facecolor('black')

    if len(drivers) == 1:
        axes = [axes]

    for ax, driver in zip(axes, drivers):
        try:
            lap = session.laps.pick_drivers(driver).pick_fastest()
            tel = lap.get_telemetry()

            x = tel['X'].values
            y = tel['Y'].values
            speed = tel['Speed'].values

            points = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)

            ax.set_facecolor('black')
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
            ax.set_title(f'{driver}', color='white', fontsize=14)

        except Exception as e:
            print(f"Error for {driver}: {e}")

    fig.suptitle(
        f'{session.event["EventName"]} {session.event.year} — Speed comparison',
        color='white', fontsize=16
    )
    plt.tight_layout()
    plt.show()