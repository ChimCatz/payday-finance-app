"""Validation functions for inputs and configurations."""

from decimal import Decimal
from typing import NoReturn
from .models import BudgetConfig, PayoutInput


def validate_payout_input(payout: PayoutInput) -> None:
    """Validate payout input parameters."""
    if payout.amount <= 0:
        raise ValueError("Payout amount must be greater than 0")
    if payout.retained_bdo < 0:
        raise ValueError("Retained BDO amount must be non-negative")
    # Budget validation is now in the model


def validate_allocation_result(result: dict) -> None:
    """Validate that allocation result is consistent."""
    # TODO: Implement validation for allocation totals
    pass