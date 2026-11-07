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

def plot_pitstops(session, pitstops):
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_facecolor('#1a1a2e')
    fig.patch.set_facecolor('#1a1a2e')

    drivers = pitstops['Driver'].unique()
    colors = [fastf1.plotting.get_driver_color(d, session) for d in drivers]

    bars = ax.barh(
        pitstops['Driver'],
        pitstops['PitDuration'],
        color=[fastf1.plotting.get_driver_color(d, session)
               for d in pitstops['Driver']],
        edgecolor='white',
        linewidth=0.5
    )

    for bar, duration in zip(bars, pitstops['PitDuration']):
        ax.text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f'{duration:.2f}s',
            va='center',
            color='white',
            fontsize=9
        )

    ax.set_xlabel('Pitstop time (seconds)', color='white')
    ax.set_title(
        f'{session.event["EventName"]} {session.event.year} — Pitstops',
        color='white', fontsize=14
    )
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.show()