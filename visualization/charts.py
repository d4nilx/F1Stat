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

COMPOUND_COLORS = {
    'SOFT': '#FF3333',
    'MEDIUM': '#FFD700',
    'HARD': '#FFFFFF',
    'INTERMEDIATE': '#39B54A',
    'WET': '#0067FF',
    'UNKNOWN': '#888888'
}
def plot_pitstops(session, pitstops):
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_facecolor('#1a1a2e')
    fig.patch.set_facecolor('#1a1a2e')

    # Унікальний лейбл для кожного пітстопу
    pitstops = pitstops.copy()
    pitstops['StopLabel'] = pitstops.apply(
        lambda r: f"{r['Driver']} (Lap {int(r['LapNumber'])})", axis=1
    )

    bar_colors = [
        COMPOUND_COLORS.get(c, '#888888')
        for c in pitstops['CompoundAfterStop'].fillna('UNKNOWN')
    ]

    bars = ax.barh(
        pitstops['StopLabel'],
        pitstops['PitDuration'],
        color=bar_colors,
        edgecolor='white',
        linewidth=0.5
    )

    for bar, (_, row) in zip(bars, pitstops.iterrows()):
        ax.text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f"{row['PitDuration']:.2f}s — {row['CompoundAfterStop'] or 'Unknown'}",
            va='center',
            color='white',
            fontsize=9
        )

    # Легенда шин
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=color, edgecolor='white', label=compound)
        for compound, color in COMPOUND_COLORS.items()
        if compound in pitstops['CompoundAfterStop'].values
    ]
    ax.legend(handles=legend_elements, loc='lower right',
              facecolor='#1a1a2e', labelcolor='white')

    ax.set_xlabel('Pitstop time (seconds)', color='white')
    ax.set_title(
        f'{session.event["EventName"]} {session.event.year} — Pitstops by Compound',
        color='white', fontsize=14
    )
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.show()