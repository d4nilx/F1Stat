import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D

def plot_track_speed(session, driver):
    if isinstance(driver, str):
        drivers = [driver]
    else:
        drivers = driver or []

    # Remove empty entries and duplicates while preserving the input order.
    drivers = list(dict.fromkeys(
        current_driver.strip().upper()
        for current_driver in drivers
        if current_driver.strip()
    ))

    if not 2 <= len(drivers) <= 4:
        print('Choose between 2 and 4 different drivers.')
        return

    driver_telemetry = []
    for current_driver in drivers:
        try:
            driver_laps = session.laps.pick_drivers(current_driver)
            lap = driver_laps.pick_fastest()
            if lap is None:
                # Some sessions have lap times but no personal-best flag.
                lap = driver_laps.pick_fastest(only_by_time=True)
            if lap is None:
                print(f'Skipping {current_driver}: no valid lap found.')
                continue

            tel = lap.get_telemetry()
            required_columns = {'Distance', 'X', 'Y', 'Speed'}
            if not required_columns.issubset(tel.columns):
                print(f'Skipping {current_driver}: telemetry is missing track data.')
                continue

            tel = (tel[['Distance', 'X', 'Y', 'Speed']]
                   .dropna()
                   .sort_values('Distance')
                   .drop_duplicates('Distance'))
            if len(tel) < 2:
                print(f'Skipping {current_driver}: not enough telemetry points.')
                continue

            driver_telemetry.append((current_driver, tel))
        except Exception as e:
            print(f'Skipping {current_driver}: {e}')
            continue

    if len(driver_telemetry) < 2:
        print('At least two drivers need valid position and speed data.')
        return

    # Compare speeds only over the distance covered by every selected driver.
    start_distance = max(tel['Distance'].iloc[0] for _, tel in driver_telemetry)
    end_distance = min(tel['Distance'].iloc[-1] for _, tel in driver_telemetry)
    if end_distance <= start_distance:
        print('The selected drivers do not have overlapping track data.')
        return

    common_distance = np.linspace(start_distance, end_distance, 1200)
    speeds = np.array([
        np.interp(common_distance, tel['Distance'], tel['Speed'])
        for _, tel in driver_telemetry
    ])

    # Use the first driver's coordinates as the shared track outline.
    reference_tel = driver_telemetry[0][1]
    x = np.interp(common_distance, reference_tel['Distance'], reference_tel['X'])
    y = np.interp(common_distance, reference_tel['Distance'], reference_tel['Y'])
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Each track section gets the color of the driver who is fastest there.
    segment_speeds = (speeds[:, :-1] + speeds[:, 1:]) / 2
    fastest_driver = segment_speeds.argmax(axis=0)
    driver_colors = np.array(plt.get_cmap('tab10').colors[:len(driver_telemetry)])

    fig, ax = plt.subplots(figsize=(12, 9))
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    line = LineCollection(
        segments,
        colors=driver_colors[fastest_driver],
        linewidth=4
    )
    ax.add_collection(line)
    ax.autoscale()
    ax.set_aspect('equal', adjustable='datalim')
    ax.axis('off')

    legend_items = [
        Line2D([0], [0], color=driver_colors[index], linewidth=4,
               label=current_driver)
        for index, (current_driver, _) in enumerate(driver_telemetry)
    ]
    legend = ax.legend(handles=legend_items, loc='upper right',
                       facecolor='#1a1a1a', edgecolor='white')
    for label in legend.get_texts():
        label.set_color('white')

    driver_names = ', '.join(name for name, _ in driver_telemetry)
    fig.suptitle(
        f'{session.event["EventName"]} {session.event.year} — Fastest by section: {driver_names}',
        color='white', fontsize=14
    )
    plt.tight_layout()
    plt.show()
