import pytest
from laundry_service import extra_weight_charge, order_acceptable, dropoff_status


def test_within_included_weight():
    assert extra_weight_charge("regular", 4, "standard", False) == 0

def test_order_acceptable():
    assert order_acceptable(10, 20, False) is True


def test_unknown_garment_raises():         
    with pytest.raises(ValueError):
        extra_weight_charge("silk", 3, "standard", False)

def test_negative_weight_raises():        
    with pytest.raises(ValueError):
        extra_weight_charge("regular", -1, "standard", False)

def test_member_bonus_applied():           
    assert extra_weight_charge("regular", 7, "standard", True) == 0

def test_standard_small_extra():           
    assert extra_weight_charge("regular", 8, "standard", False) == 90     

def test_express_large_extra():           
    assert extra_weight_charge("regular", 20, "express", False) == 1125  


def test_delicate_order():                
    assert order_acceptable(2, 3, True) is True

def test_too_heavy_order():                
    assert order_acceptable(30, 10, False) is False


def test_dropoff_accepted_bedding_express():  
    assert dropoff_status(200, True, True) == "accepted"

def test_dropoff_late_no_bedding():     
    assert dropoff_status(50, False, False) == "late"

def test_dropoff_rejected():              
    assert dropoff_status(10, False, False) == "rejected"
