def get_pitstop_analysis(session):
    laps = session.laps.sort_values(['Driver', 'LapNumber']).copy()
    laps['PreviousPitInTime'] = laps.groupby('Driver')['PitInTime'].shift(1)
    laps['PitInTimeForStop'] = laps['PreviousPitInTime'].fillna(
        laps['PitInTime']
    )

    laps['CompoundAfterStop'] = laps.groupby('Driver')['Compound'].shift(-1)

    pitstops = laps[laps['PitOutTime'].notna()][
        ['Driver', 'LapNumber', 'PitInTimeForStop', 'PitOutTime', 'CompoundAfterStop']
    ].copy()

    pitstops['PitDuration'] = (
        pitstops['PitOutTime'] - pitstops['PitInTimeForStop']
    ).dt.total_seconds()

    pitstops = pitstops[pitstops['PitDuration'] > 0]
    pitstops = pitstops[pitstops['PitDuration'] < 120]

    return pitstops.sort_values(['Driver', 'LapNumber'])