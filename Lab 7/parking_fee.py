"""Parking fee utilities used in Lab 7 fuzz-testing exercises."""

import re

RATES = {"bike": 10, "car": 30, "truck": 60}

_TIME_RANGE_RE = re.compile(r"^(\d{2}):(\d{2})\s*-\s*(\d{2}):(\d{2})$")
_PLATE_RE = re.compile(r"^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$")


def minutes_parked(times):
    """Return elapsed parking minutes for 'HH:MM-HH:MM'.

    If the exit time is earlier than the entry time, it is treated as
    an overnight stay ending on the following day.
    """
    if not isinstance(times, str):
        raise ValueError("Parking times must be provided as a string.")

    match = _TIME_RANGE_RE.fullmatch(times.strip())
    if not match:
        raise ValueError("Use the time format HH:MM-HH:MM (for example, 09:30-11:45).")

    h1, m1, h2, m2 = map(int, match.groups())
    if not (0 <= h1 <= 23 and 0 <= h2 <= 23):
        raise ValueError("Hours must be between 00 and 23.")
    if not (0 <= m1 <= 59 and 0 <= m2 <= 59):
        raise ValueError("Minutes must be between 00 and 59.")

    entry_minutes = h1 * 60 + m1
    exit_minutes = h2 * 60 + m2
    if exit_minutes < entry_minutes:
        exit_minutes += 24 * 60

    return exit_minutes - entry_minutes


def hourly_rate(vehicle):
    """Return the hourly rate for bike, car, or truck."""
    if not isinstance(vehicle, str):
        raise ValueError("Vehicle type must be a string.")

    vehicle_key = vehicle.strip().lower()
    if vehicle_key not in RATES:
        raise ValueError("Unknown vehicle type. Choose bike, car, or truck.")

    return RATES[vehicle_key]


def format_plate(plate):
    """Validate and format an Indian-style registration number.

    Expected format: two letters, two digits, two letters, four digits.
    Example: ka01ab1234 -> KA 01 AB 1234.
    """
    if not isinstance(plate, str):
        raise ValueError("Number plate must be provided as a string.")

    normalized = plate.strip().upper()
    if not _PLATE_RE.fullmatch(normalized):
        raise ValueError(
            "Invalid number plate. Expected format: AA00AA0000 "
            "(for example, KA01AB1234)."
        )

    return f"{normalized[:2]} {normalized[2:4]} {normalized[4:6]} {normalized[6:]}"


def main():
    print("==== Running minutes_parked ====")
    user_input = input("Enter entry and exit time (e.g. 09:30-11:45): ")
    try:
        result = minutes_parked(user_input)
        print("Minutes Parked:", result)
    except ValueError as error:
        print("Invalid parking time:", error)

    print("\n==== Running hourly_rate ====")
    user_input = input("Enter vehicle type (bike/car/truck): ")
    try:
        result = hourly_rate(user_input)
        print("Hourly Rate:", result)
    except ValueError as error:
        print("Invalid vehicle type:", error)

    print("\n==== Running format_plate ====")
    user_input = input("Enter a number plate (e.g. ka01ab1234): ")
    try:
        result = format_plate(user_input)
        print("Formatted Plate:", result)
    except ValueError as error:
        print("Invalid number plate:", error)


if __name__ == "__main__":
    main()
