# F1Stat

A small Python project for exploring Formula 1 race data. It uses [FastF1](https://docs.fastf1.dev/) to load session data and Matplotlib to display charts.

## Features

- View driver positions by lap.
- View speed maps for selected drivers' fastest laps.
- View pit stop durations and tyre compounds.

This project is a work in progress. More analysis and visualizations may be added later.

## Run the project

Install the required libraries:

```bash
python -m pip install fastf1 matplotlib numpy
```

Start the program from the project folder:

```bash
python main.py
```

Enter a season year and Grand Prix name when prompted. To view a speed map, enter driver abbreviations separated by commas, for example `VER, HAM`.

FastF1 downloads session data as needed and stores it in the local cache folder.
