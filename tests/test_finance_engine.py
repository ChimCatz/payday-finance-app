"""Tests for finance_engine module."""

import pytest
from decimal import Decimal
from src.models import PayoutInput, BudgetConfig
from src.finance_engine import allocate_payout, calculate_category_amounts


def test_calculate_category_amounts():
    """Test category amount calculations."""
    amount = Decimal("1000.00")
    budget = BudgetConfig(
        offering=Decimal("0.10"),
        savings=Decimal("0.20"),
        emergency=Decimal("0.10"),
        food=Decimal("0.30"),
        bills=Decimal("0.10"),
        fun=Decimal("0.10"),
        buffer=Decimal("0.10")
    )

    amounts = calculate_category_amounts(amount, budget)

    assert amounts["offering"] == Decimal("100.00")
    assert amounts["savings"] == Decimal("200.00")
    assert amounts["food"] == Decimal("300.00")


def test_allocate_payout_basic():
    """Test basic payout allocation."""
    budget = BudgetConfig(
        offering=Decimal("0.10"),
        savings=Decimal("0.17"),
        emergency=Decimal("0.07"),
        food=Decimal("0.20"),
        bills=Decimal("0.09"),
        fun=Decimal("0.12"),
        buffer=Decimal("0.25")
    )

    payout = PayoutInput(
        amount=Decimal("7500.00"),
        retained_bdo=Decimal("500.00"),
        budget=budget
    )

    result = allocate_payout(payout)

    assert result.offering_bdo == Decimal("750.00")  # 10% of 7500
    assert result.retained_bdo == Decimal("500.00")
    assert result.gotyme_savings == Decimal("1275.00")  # 17% of 7500
    assert result.gotyme_emergency == Decimal("525.00")  # 7% of 7500
    assert result.gcash_food == Decimal("1500.00")  # 20% of 7500


def test_allocate_payout_invalid_amount():
    """Test validation for invalid payout amount."""
    budget = BudgetConfig(
        offering=Decimal("0.10"),
        savings=Decimal("0.17"),
        emergency=Decimal("0.07"),
        food=Decimal("0.20"),
        bills=Decimal("0.09"),
        fun=Decimal("0.12"),
        buffer=Decimal("0.25")
    )

    with pytest.raises(Exception):  # Pydantic ValidationError
        PayoutInput(
            amount=Decimal("-100.00"),
            retained_bdo=Decimal("500.00"),
            budget=budget
        )