def get_pitstop_analysis(session):
    # PitInTime is usually on the lap before PitOutTime.
    laps = session.laps.sort_values(['Driver', 'LapNumber']).copy()
    laps['PreviousPitInTime'] = laps.groupby('Driver')['PitInTime'].shift(1)
    laps['PitInTimeForStop'] = laps['PreviousPitInTime'].fillna(
        laps['PitInTime']
    )
    laps['PreviousLapNumber'] = laps.groupby('Driver')['LapNumber'].shift(1)
    laps['PitInLap'] = laps['PreviousLapNumber'].where(
        laps['PreviousPitInTime'].notna(), laps['LapNumber']
    )

    laps['CompoundAfterStop'] = laps.groupby('Driver')['Compound'].shift(-1)

    pitstops = laps[laps['PitOutTime'].notna()][
        ['Driver', 'PitInLap', 'Compound', 'PitInTimeForStop', 'PitOutTime']
    ].copy()

    pitstops['PitDuration'] = (
        pitstops['PitOutTime'] - pitstops['PitInTimeForStop']
    ).dt.total_seconds()
    pitstops = pitstops.dropna(subset=['PitInTimeForStop', 'PitDuration'])
    pitstops = pitstops[pitstops['PitDuration'] > 0].copy()

    # Track status 5 means red flag. Each status remains active until the next
    # status message, so these intervals identify stops during a red flag.
    track_status = getattr(session, 'track_status', None)
    red_flag_intervals = []
    if track_status is not None and not track_status.empty:
        track_status = track_status.sort_values('Time').reset_index(drop=True)
        for index, status in track_status.iterrows():
            if str(status['Status']) == '5' and index + 1 < len(track_status):
                red_flag_intervals.append(
                    (status['Time'], track_status.iloc[index + 1]['Time'])
                )

    stop_types = []
    for _, stop in pitstops.iterrows():
        during_red_flag = any(
            stop['PitInTimeForStop'] <= flag_end
            and stop['PitOutTime'] >= flag_start
            for flag_start, flag_end in red_flag_intervals
        )

        if during_red_flag:
            stop_types.append('Red Flag')
        elif stop['PitDuration'] < 120:
            stop_types.append('Green Flag')
        else:
            stop_types.append('Long / unclassified')

    pitstops['StopType'] = stop_types

    # The elapsed red-flag interval is not pit-lane service time. Keep a
    # duration only for ordinary stops so it cannot be mistaken for a 39 min stop.
    pitstops.loc[pitstops['StopType'] != 'Green Flag', 'PitDuration'] = float('nan')

    return pitstops.sort_values(['StopType', 'PitInTimeForStop'])
