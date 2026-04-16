"""Tests for allocator module."""

from decimal import Decimal
from src.models import AllocationResult
from src.allocator import route_to_accounts, get_account_summary


def test_route_to_accounts():
    """Test routing to accounts."""
    allocation = AllocationResult(
        offering_bdo=Decimal("750.00"),
        retained_bdo=Decimal("500.00"),
        gotyme_savings=Decimal("1275.00"),
        gotyme_emergency=Decimal("525.00"),
        gcash_food=Decimal("1500.00"),
        gcash_bills=Decimal("675.00"),
        gcash_fun=Decimal("900.00"),
        gcash_buffer=Decimal("1875.00"),
        total_allocated=Decimal("7500.00"),
        unallocated_or_rounding_difference=Decimal("0.00")
    )

    routing = route_to_accounts(allocation)

    assert routing["BDO_offering"] == Decimal("750.00")
    assert routing["BDO_retained"] == Decimal("500.00")
    assert routing["GoTyme_savings"] == Decimal("1275.00")
    assert routing["GoTyme_emergency"] == Decimal("525.00")
    assert routing["GCash_food"] == Decimal("1500.00")


def test_get_account_summary():
    """Test account summary calculation."""
    routing = {
        "BDO_offering": Decimal("750.00"),
        "BDO_retained": Decimal("500.00"),
        "GoTyme_savings": Decimal("1275.00"),
        "GoTyme_emergency": Decimal("525.00"),
        "GCash_food": Decimal("1500.00"),
        "GCash_bills": Decimal("675.00"),
        "GCash_fun": Decimal("900.00"),
        "GCash_buffer": Decimal("1875.00"),
    }

    summary = get_account_summary(routing)

    assert summary["BDO"] == Decimal("1250.00")  # 750 + 500
    assert summary["GoTyme"] == Decimal("1800.00")  # 1275 + 525
    assert summary["GCash"] == Decimal("4950.00")  # 1500 + 675 + 900 + 1875