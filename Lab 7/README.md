# Lab 7 — Fuzz Testing (Parking Fee)

## Files
- `parking_fee.py`: validated parking-fee application.
- `test_parking_fee.py`: Hypothesis property-based tests.

## Install dependencies
```bash
python -m pip install hypothesis pytest
```

## Run the application
```bash
python parking_fee.py
```

## Run tests
```bash
python -m pytest -v test_parking_fee.py
```

## Validation behaviour
- `minutes_parked` accepts `HH:MM-HH:MM`, validates 24-hour clock values, and treats an earlier exit time as an overnight stay.
- `hourly_rate` accepts `bike`, `car`, or `truck`, ignoring case and surrounding whitespace.
- `format_plate` accepts the ten-character Indian-style pattern `AA00AA0000` and formats it as `AA 00 AA 0000`.
- Invalid values raise a clear `ValueError`; the interactive application catches these errors and displays a helpful message.
