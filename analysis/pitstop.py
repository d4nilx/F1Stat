def get_pitstop_analysis(session):
    # FastF1 usually stores PitInTime on the lap before PitOutTime.
    # Sort laps so we can pair each pit exit with the previous lap's pit entry.
    laps = session.laps.sort_values(['Driver', 'LapNumber']).copy()
    laps['PreviousPitInTime'] = laps.groupby('Driver')['PitInTime'].shift(1)
    laps['PitInTimeForStop'] = laps['PreviousPitInTime'].fillna(
        laps['PitInTime']
    )

    pitstops = laps[laps['PitOutTime'].notna()][
        ['Driver', 'LapNumber', 'PitInTimeForStop', 'PitOutTime']
    ].copy()

    pitstops['PitDuration'] = (
            pitstops['PitOutTime'] - pitstops['PitInTimeForStop']
    ).dt.total_seconds()

    pitstops = pitstops[pitstops['PitDuration'] > 0]
    pitstops = pitstops[pitstops['PitDuration'] < 120]

    return pitstops.sort_values('PitDuration')
