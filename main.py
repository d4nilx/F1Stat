from data.loader import load_session
from visualization.charts import plot_positions
from visualization.track_map import plot_track_speed_comparison


def get_drivers_input():
    drivers = input("Give drivers name: ")
    return [d.strip().upper() for d in drivers.split(',')]


def main():
    print("=== F1 Stat ===")
    year = int(input("Year: "))
    circuit = input("Grand Prix: ")

    print("\nGetting some data...")
    session = load_session(year, circuit)

    print("\nWhat do you want to see?")
    print("1 — Positions")
    print("2 — Speed map comparison")
    choice = input("Choice: ")

    if choice == '1':
        plot_positions(session)
    elif choice == '2':
        drivers = get_drivers_input()
        plot_track_speed_comparison(session, drivers)


if __name__ == '__main__':
    main()