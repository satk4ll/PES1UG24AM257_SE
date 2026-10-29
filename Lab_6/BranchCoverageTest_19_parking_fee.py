import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


def test_parking_fee_vehicle_validation():
    with pytest.raises(ValueError):
        parking_fee("bus", 60, False, False)


def test_parking_fee_duration_validation():
    with pytest.raises(ValueError):
        parking_fee("car", -1, False, False)


def test_parking_fee_free_and_paid():
    assert parking_fee("bike", 30, False, False) == 0
    assert parking_fee("bike", 31, False, False) == 10


def test_parking_fee_exact_and_partial_hours():
    assert parking_fee("car", 60, False, False) == 30
    assert parking_fee("car", 61, False, False) == 60


def test_parking_fee_ev_conditions():
    assert parking_fee("car", 60, True, False) == 15
    assert parking_fee("car", 60, False, False) == 30
    assert parking_fee("truck", 60, True, False) == 60


def test_parking_fee_lost_ticket_conditions():
    assert parking_fee("bike", 60, False, False) == 10
    assert parking_fee("bike", 60, False, True) == 210


def test_find_slot_full_condition():
    assert find_slot("car", 0, False) == "full"
    assert find_slot("car", 2, False) == "any floor"


def test_find_slot_disabled_condition():
    assert find_slot("car", 2, True) == "ground floor"
    assert find_slot("car", 2, False) == "any floor"


def test_find_slot_truck_condition():
    assert find_slot("truck", 2, False) == "basement"
    assert find_slot("bike", 2, False) == "any floor"


def test_monthly_pass_vehicle_conditions():
    assert monthly_pass("bike", False) == 500
    assert monthly_pass("car", False) == 1500
    with pytest.raises(ValueError):
        monthly_pass("truck", False)


def test_monthly_pass_resident_conditions():
    assert monthly_pass("bike", True) == 400
    assert monthly_pass("car", True) == 1200
