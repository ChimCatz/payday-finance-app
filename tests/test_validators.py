"""Tests for validators module."""

import pytest
from decimal import Decimal
from src.models import BudgetConfig, PayoutInput
from src.validators import validate_payout_input


def test_validate_payout_input_valid():
    """Test validation of valid payout input."""
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

    # Should not raise
    validate_payout_input(payout)


def test_validate_payout_input_invalid_amount():
    """Test validation of payout input with invalid amount."""
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
            amount=Decimal("0.00"),
            retained_bdo=Decimal("500.00"),
            budget=budget
        )