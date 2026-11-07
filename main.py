from data.loader import load_session
from analysis.pitstop import get_pitstop_analysis
from visualization.charts import plot_positions, plot_pitstops
from visualization.track_map import plot_track_speed

def get_drivers_input():
    drivers = input("Enter drivers: ")
    return [d.strip().upper() for d in drivers.split(',')]

def main():
    print("=== F1 Stat ===")
    year = int(input("Year: "))
    circuit = input("Grand Prix: ")

    print("\nGetting data...")
    session = load_session(year, circuit)

    while True:
        print("\nWhat do you want to see?")
        print("1 — Positions by each circle")
        print("2 — Speed map")
        print("3 — Pitstops")
        print("0 — Exit")
        choice = input("Choice: ")

        if choice == '1':
            plot_positions(session)
        elif choice == '2':
            drivers = get_drivers_input()
            plot_track_speed(session, drivers)
        elif choice == '3':
            pitstops = get_pitstop_analysis(session)
            plot_pitstops(session, pitstops)
        elif choice == '0':
            break
        else:
            print("Try again")

if __name__ == '__main__':
    main()