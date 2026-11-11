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
    green_stops = pitstops[pitstops['StopType'] == 'Green Flag'].copy()
    other_stops = pitstops[pitstops['StopType'] != 'Green Flag'].copy()

    figure_height = max(8, len(other_stops) * 0.42 + 2)
    fig, (green_ax, other_ax) = plt.subplots(
        1, 2, figsize=(16, figure_height),
        gridspec_kw={'width_ratios': [1, 1.25]}
    )
    green_ax.set_facecolor('#1a1a2e')
    other_ax.set_facecolor('#1a1a2e')
    fig.patch.set_facecolor('#1a1a2e')

    if green_stops.empty:
        green_ax.text(0.5, 0.5, 'No green-flag pit stops recorded',
                      ha='center', va='center', color='white',
                      transform=green_ax.transAxes)
        green_ax.set_axis_off()
    else:
        green_stops = green_stops.sort_values('PitDuration')
        labels = []
        for row in green_stops.itertuples():
            compound = (row.Compound if isinstance(row.Compound, str)
                        and row.Compound else 'compound unknown')
            labels.append(
                f'{row.Driver} — Lap {int(row.PitInLap)} — {compound}'
            )
        colors = [
            fastf1.plotting.get_driver_color(driver, session)
            for driver in green_stops['Driver']
        ]

        bars = green_ax.barh(
            labels,
            green_stops['PitDuration'],
            color=colors,
            edgecolor='white',
            linewidth=0.5
        )

        for bar, stop in zip(bars, green_stops.itertuples()):
            total_seconds = stop.PitInTimeForStop.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = total_seconds % 60
            session_time = f'{hours:02d}:{minutes:02d}:{seconds:06.3f}'
            green_ax.text(
                bar.get_width() + 0.2,
                bar.get_y() + bar.get_height() / 2,
                f'{stop.PitDuration:.2f}s | entry {session_time}',
                va='center',
                color='white',
                fontsize=9
            )

        green_ax.set_xlim(0, green_stops['PitDuration'].max() + 45)
        green_ax.tick_params(colors='white')
        green_ax.spines['bottom'].set_color('white')
        green_ax.spines['left'].set_color('white')
        green_ax.spines['top'].set_visible(False)
        green_ax.spines['right'].set_visible(False)
        green_ax.set_xlabel('Pit-lane time (seconds)', color='white')

    other_ax.set_axis_off()
    other_ax.text(0.03, 1.0, 'RED FLAG / LONG UNCLASSIFIED EVENTS',
                  color='white', fontsize=12, weight='bold',
                  transform=other_ax.transAxes, va='top')
    if other_stops.empty:
        other_ax.text(0.03, 0.9, 'No red-flag or unclassified stops recorded',
                      color='white', transform=other_ax.transAxes)
    else:
        for index, stop in enumerate(other_stops.itertuples()):
            compound = (stop.Compound if isinstance(stop.Compound, str)
                        and stop.Compound else 'compound unknown')
            if stop.StopType == 'Red Flag':
                description = 'red-flag tyre change; duration not comparable'
            else:
                description = 'long stop; type not identified'
            label = (
                f'{stop.Driver} — Lap {int(stop.PitInLap)} — '
                f'{compound} — {description}'
            )
            y_position = 0.92 - index * (0.86 / max(len(other_stops), 1))
            other_ax.text(0.03, y_position, label, color='white', fontsize=9,
                          transform=other_ax.transAxes, va='top')

    green_ax.set_title('GREEN FLAG PIT STOPS', color='white', fontsize=12)
    fig.suptitle(
        f'{session.event["EventName"]} {session.event.year} — Pit Stops',
        color='white', fontsize=14
    )
    plt.tight_layout(rect=(0, 0, 1, 0.96))
    plt.show()
