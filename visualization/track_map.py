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
        try:
            lap = session.laps.pick_drivers(current_driver).pick_fastest()
            if lap is None:
                print(f'No lap found for {current_driver}')
                continue

            car_data = lap.get_car_data().add_distance()
            pos_data = lap.get_pos_data()

            if car_data.empty or pos_data.empty:
                print(f'No data for {current_driver}')
                continue

            driver_telemetry.append((current_driver, car_data, pos_data))
        except Exception as e:
            print(f'Skipping {current_driver}: {e}')
            continue

    if not driver_telemetry:
        print('No telemetry data found for the selected drivers.')
        return

    fig, axes = plt.subplots(
        1, len(driver_telemetry),
        figsize=(10 * len(driver_telemetry), 8)
    )
    fig.patch.set_facecolor('black')

    if len(driver_telemetry) == 1:
        axes = [axes]

    for ax, (current_driver, car_data, pos_data) in zip(axes, driver_telemetry):
        x = pos_data['X'].values
        y = pos_data['Y'].values

        speed_interp = np.interp(
            np.linspace(0, 1, len(x)),
            np.linspace(0, 1, len(car_data)),
            car_data['Speed'].values
        )

        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        ax.set_facecolor('black')
        norm = plt.Normalize(speed_interp.min(), speed_interp.max())
        lc = LineCollection(segments, cmap='RdYlGn', norm=norm, linewidth=3)
        lc.set_array(speed_interp[:-1])
        ax.add_collection(lc)

        cbar = fig.colorbar(lc, ax=ax)
        cbar.set_label('Speed (km/h)', color='white')
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')

        ax.autoscale()
        ax.axis('off')
        ax.set_title(current_driver, color='white', fontsize=16)

    fig.suptitle(
        f'{session.event["EventName"]} {session.event.year} — Speed Comparison',
        color='white', fontsize=14
    )

    plt.tight_layout()
    plt.show()