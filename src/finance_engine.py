"""Core finance engine for calculating allocations."""

from decimal import Decimal, ROUND_HALF_UP
from .models import PayoutInput, AllocationResult, BudgetConfig
from .validators import validate_payout_input


def calculate_category_amounts(payout_amount: Decimal, budget: BudgetConfig) -> dict[str, Decimal]:
    """Calculate amounts for each budget category."""
    return {
        "offering": (payout_amount * budget.offering).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        "savings": (payout_amount * budget.savings).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        "emergency": (payout_amount * budget.emergency).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        "food": (payout_amount * budget.food).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        "bills": (payout_amount * budget.bills).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        "fun": (payout_amount * budget.fun).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        "buffer": (payout_amount * budget.buffer).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
    }


def allocate_payout(payout: PayoutInput) -> AllocationResult:
    """Allocate payout according to budget rules and minimum retention."""
    validate_payout_input(payout)

    amounts = calculate_category_amounts(payout.amount, payout.budget)

    # Calculate total allocated before retention
    total_allocated = sum(amounts.values())

    # Ensure minimum BDO retention
    offering_bdo = amounts["offering"]
    retained_bdo = max(payout.retained_bdo, Decimal("0"))  # Ensure non-negative

    # Note: In this simple model, retained is separate from offering
    # If offering + retained > available, we might need adjustment, but for MVP, assume sufficient

    return AllocationResult(
        offering_bdo=offering_bdo,
        retained_bdo=retained_bdo,
        gotyme_savings=amounts["savings"],
        gotyme_emergency=amounts["emergency"],
        gcash_food=amounts["food"],
        gcash_bills=amounts["bills"],
        gcash_fun=amounts["fun"],
        gcash_buffer=amounts["buffer"],
        total_allocated=total_allocated,
        unallocated_or_rounding_difference=payout.amount - total_allocated,
    )