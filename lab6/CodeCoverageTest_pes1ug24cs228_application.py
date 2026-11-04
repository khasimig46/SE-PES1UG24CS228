import pytest
from laundry_service import extra_weight_charge, order_acceptable, dropoff_status

# ---------- Starter tests ----------
def test_within_included_weight():
    assert extra_weight_charge("regular", 4, "standard", False) == 0

def test_order_acceptable():
    assert order_acceptable(10, 20, False) is True

# ---------- extra_weight_charge ----------
def test_unknown_garment_raises():          # covers line 6
    with pytest.raises(ValueError):
        extra_weight_charge("silk", 3, "standard", False)

def test_negative_weight_raises():          # covers line 8
    with pytest.raises(ValueError):
        extra_weight_charge("regular", -1, "standard", False)

def test_member_bonus_applied():            # covers line 11 (member gets +2 kg)
    assert extra_weight_charge("regular", 7, "standard", True) == 0

def test_standard_small_extra():            # covers lines 12-16, 19, 23 (rate = 30)
    assert extra_weight_charge("regular", 8, "standard", False) == 90     # 3 kg * 30

def test_express_large_extra():             # covers lines 18, 20, 22 (rate 50 +15 +10)
    assert extra_weight_charge("regular", 20, "express", False) == 1125   # 15 kg * 75

# ---------- order_acceptable ----------
def test_delicate_order():                  # covers line 28
    assert order_acceptable(2, 3, True) is True

def test_too_heavy_order():                 # covers line 30
    assert order_acceptable(30, 10, False) is False

# ---------- dropoff_status ----------
def test_dropoff_accepted_bedding_express():  # covers lines 36, 40, 42
    assert dropoff_status(200, True, True) == "accepted"

def test_dropoff_late_no_bedding():         # covers lines 38, 44
    assert dropoff_status(50, False, False) == "late"

def test_dropoff_rejected():                # covers line 45
    assert dropoff_status(10, False, False) == "rejected"
