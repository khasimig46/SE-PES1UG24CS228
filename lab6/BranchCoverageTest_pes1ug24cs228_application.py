import pytest
from laundry_service import extra_weight_charge, order_acceptable, dropoff_status


def test_unknown_garment_raises():
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge("silk", 3, "standard", False)

def test_negative_weight_raises():
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -1, "standard", False)

def test_zero_weight_is_valid():          
    assert extra_weight_charge("regular", 0, "standard", False) == 0

def test_within_included_weight():
    assert extra_weight_charge("regular", 4, "standard", False) == 0

def test_member_gets_bonus_regular():      
    assert extra_weight_charge("regular", 7, "standard", True) == 0

def test_non_member_no_bonus():             
    assert extra_weight_charge("regular", 7, "standard", False) == 60    

def test_member_bedding_no_bonus():        
    assert extra_weight_charge("bedding", 10, "standard", True) == 60    
def test_delicate_member_bonus():
    assert extra_weight_charge("delicate", 6, "standard", True) == 30     
def test_exactly_included_weight_is_free():
    assert extra_weight_charge("regular", 5, "standard", False) == 0

def test_standard_rate():
    assert extra_weight_charge("regular", 8, "standard", False) == 90    

def test_express_rate():
    assert extra_weight_charge("regular", 8, "express", False) == 150     

def test_other_speed_uses_non_standard_rate():
    assert extra_weight_charge("regular", 8, "overnight", False) == 150   

def test_extra_exactly_10_no_surcharge():
    assert extra_weight_charge("regular", 15, "standard", False) == 300  

def test_extra_11_standard_surcharge_only():  
    assert extra_weight_charge("regular", 16, "standard", False) == 495   

def test_extra_large_standard():
    assert extra_weight_charge("regular", 20, "standard", False) == 675   

def test_extra_large_express():           
    assert extra_weight_charge("regular", 20, "express", False) == 1125   

def test_order_acceptable():
    assert order_acceptable(10, 20, False) is True

def test_delicate_within_limit():           
    assert order_acceptable(2, 5, True) is True

def test_delicate_over_limit():
    assert order_acceptable(2, 6, True) is False

def test_delicate_ignores_weight():
    assert order_acceptable(100, 5, True) is True

def test_normal_at_limits():               
    assert order_acceptable(25, 40, False) is True

def test_too_heavy_order():               
    assert order_acceptable(26, 10, False) is False

def test_too_many_items():
    assert order_acceptable(10, 41, False) is False


@pytest.mark.parametrize("minutes, bedding, express, expected", [

    (60, False, False, "accepted"),
    (59, False, False, "late"),
    (40, False, False, "late"),
    (39, False, False, "rejected"),
   
    (90, True,  False, "accepted"),
    (89, True,  False, "late"),
    (70, True,  False, "late"),
    (69, True,  False, "rejected"),
    
    (90, False, True,  "accepted"),
    (70, False, True,  "late"),
    (69, False, True,  "rejected"),
   
    (120, True, True,  "accepted"),
    (100, True, True,  "late"),
    (99,  True, True,  "rejected"),
])
def test_dropoff_status(minutes, bedding, express, expected):
    assert dropoff_status(minutes, bedding, express) == expected
