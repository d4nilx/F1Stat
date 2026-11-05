import fastf1.plotting
import matplotlib.pyplot as plt

def plot_positions(session):
    fig, ax = plt.subplots(figsize=(15, 8))

    for drv in session.drivers:
        drv_laps = session.laps.pick_drivers(drv)
        if drv_laps.empty:
            continue

        abbr = drv_laps['Driver'].iloc[0]
        color = fastf1.plotting.get_driver_color(abbr, session)

        ax.plot(drv_laps['LapNumber'], drv_laps['Position'],
                label=abbr, color=color, linewidth=2)

    ax.set_ylim([20.5, 0.5])
    ax.set_xlabel('Circle')
    ax.set_ylabel('Position')
    ax.set_title(f'{session.event["EventName"]} {session.event.year} — Positions by each circle')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()