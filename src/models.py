"""Data models for the Payday Finance App."""

from decimal import Decimal
from typing import Dict
from pydantic import BaseModel, Field, field_validator, model_validator


class BudgetConfig(BaseModel):
    """Configuration for budget percentages."""
    offering: Decimal = Field(..., ge=0, le=1)
    savings: Decimal = Field(..., ge=0, le=1)
    emergency: Decimal = Field(..., ge=0, le=1)
    food: Decimal = Field(..., ge=0, le=1)
    bills: Decimal = Field(..., ge=0, le=1)
    fun: Decimal = Field(..., ge=0, le=1)
    buffer: Decimal = Field(..., ge=0, le=1)

    @field_validator('offering', 'savings', 'emergency', 'food', 'bills', 'fun', 'buffer', mode='after')
    @classmethod
    def validate_percentage(cls, v):
        if not (0 <= v <= 1):
            raise ValueError("Percentage must be between 0 and 1")
        return v

    @model_validator(mode='after')
    def validate_total_percentage(self):
        total = (
            self.offering + self.savings + self.emergency +
            self.food + self.bills + self.fun + self.buffer
        )
        if total != Decimal("1.0"):
            raise ValueError(f"Budget percentages must sum to 1.0, got {total}")
        return self


class PayoutInput(BaseModel):
    """Input for a payout allocation."""
    amount: Decimal = Field(..., gt=0)
    retained_bdo: Decimal = Field(..., ge=0)
    budget: BudgetConfig


class AllocationResult(BaseModel):
    """Result of allocation calculation."""
    offering_bdo: Decimal
    retained_bdo: Decimal
    gotyme_savings: Decimal
    gotyme_emergency: Decimal
    gcash_food: Decimal
    gcash_bills: Decimal
    gcash_fun: Decimal
    gcash_buffer: Decimal
    total_allocated: Decimal
    unallocated_or_rounding_difference: Decimal


class HistoryEntry(BaseModel):
    """Entry for allocation history."""
    date: str
    payout_input: PayoutInput
    allocation: AllocationResult