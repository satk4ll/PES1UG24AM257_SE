import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


def test_parking_fee_free_period():
    assert parking_fee("bike", 30, False, False) == 0


def test_parking_fee_hourly_charge():
    assert parking_fee("car", 61, False, False) == 60


def test_parking_fee_ev_discount():
    assert parking_fee("car", 60, True, False) == 15


def test_parking_fee_lost_ticket():
    assert parking_fee("bike", 30, False, True) == 200


def test_parking_fee_invalid_vehicle():
    with pytest.raises(ValueError):
        parking_fee("bus", 60, False, False)


def test_parking_fee_negative_duration():
    with pytest.raises(ValueError):
        parking_fee("car", -1, False, False)


def test_find_slot_full():
    assert find_slot("car", 0, False) == "full"


def test_find_slot_disabled():
    assert find_slot("car", 5, True) == "ground floor"


def test_find_slot_truck():
    assert find_slot("truck", 5, False) == "basement"


def test_find_slot_any_floor():
    assert find_slot("bike", 5, False) == "any floor"


def test_monthly_pass_prices():
    assert monthly_pass("bike", False) == 500
    assert monthly_pass("car", False) == 1500


def test_monthly_pass_resident_discount():
    assert monthly_pass("bike", True) == 400
    assert monthly_pass("car", True) == 1200


def test_monthly_pass_invalid_vehicle():
    with pytest.raises(ValueError):
        monthly_pass("truck", False)
