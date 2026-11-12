"""Property-based tests for the parking fee application."""

import re

import pytest
from hypothesis import given, strategies as st

from parking_fee import RATES, format_plate, hourly_rate, minutes_parked


# ---------- minutes_parked ----------

@given(
    h1=st.integers(min_value=0, max_value=23),
    m1=st.integers(min_value=0, max_value=59),
    h2=st.integers(min_value=0, max_value=23),
    m2=st.integers(min_value=0, max_value=59),
)
def test_minutes_parked_returns_valid_elapsed_minutes(h1, m1, h2, m2):
    times = f"{h1:02d}:{m1:02d}-{h2:02d}:{m2:02d}"
    start = h1 * 60 + m1
    end = h2 * 60 + m2
    expected = end - start if end >= start else end + 1440 - start
    assert minutes_parked(times) == expected


@given(st.one_of(st.text(), st.none(), st.integers(), st.lists(st.integers())))
def test_minutes_parked_rejects_malformed_inputs(value):
    valid_format = (
        isinstance(value, str)
        and re.fullmatch(r"\d{2}:\d{2}\s*-\s*\d{2}:\d{2}", value.strip())
        and all(
            0 <= int(part) <= limit
            for part, limit in zip(
                re.findall(r"\d+", value), [23, 59, 23, 59]
            )
        )
    )
    if valid_format:
        assert isinstance(minutes_parked(value), int)
    else:
        with pytest.raises(ValueError):
            minutes_parked(value)


def test_minutes_parked_handles_overnight_parking():
    assert minutes_parked("23:30-01:15") == 105


# ---------- hourly_rate ----------

@given(st.sampled_from(list(RATES)))
def test_hourly_rate_returns_configured_rate(vehicle):
    assert hourly_rate(vehicle) == RATES[vehicle]


@given(st.sampled_from(list(RATES)).map(lambda value: f"  {value.upper()}  "))
def test_hourly_rate_is_case_and_whitespace_insensitive(vehicle):
    assert hourly_rate(vehicle) == RATES[vehicle.strip().lower()]


@given(st.one_of(st.text(), st.none(), st.integers(), st.lists(st.text())))
def test_hourly_rate_rejects_unknown_or_invalid_inputs(value):
    valid = isinstance(value, str) and value.strip().lower() in RATES
    if valid:
        assert hourly_rate(value) == RATES[value.strip().lower()]
    else:
        with pytest.raises(ValueError):
            hourly_rate(value)


# ---------- format_plate ----------

@given(
    state=st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=2, max_size=2),
    district=st.integers(min_value=0, max_value=99),
    series=st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=2, max_size=2),
    number=st.integers(min_value=0, max_value=9999),
)
def test_format_plate_formats_valid_registration(state, district, series, number):
    plate = f"{state}{district:02d}{series}{number:04d}"
    assert format_plate(plate.lower()) == (
        f"{state} {district:02d} {series} {number:04d}"
    )


@given(st.one_of(st.text(), st.none(), st.integers(), st.lists(st.text())))
def test_format_plate_rejects_invalid_inputs(value):
    valid = isinstance(value, str) and re.fullmatch(
        r"[A-Za-z]{2}\d{2}[A-Za-z]{2}\d{4}", value.strip()
    )
    if valid:
        assert format_plate(value) == (
            f"{value.strip()[:2].upper()} {value.strip()[2:4]} "
            f"{value.strip()[4:6].upper()} {value.strip()[6:]}"
        )
    else:
        with pytest.raises(ValueError):
            format_plate(value)


def test_format_plate_example():
    assert format_plate("ka01ab1234") == "KA 01 AB 1234"
