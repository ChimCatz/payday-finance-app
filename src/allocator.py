"""Allocator for routing funds to accounts."""

from decimal import Decimal
from typing import Dict
from .models import AllocationResult
from .config import ACCOUNT_ROUTING


def route_to_accounts(allocation: AllocationResult) -> Dict[str, Decimal]:
    """Route allocated amounts to specific accounts."""
    # This is a simple mapping based on the allocation result
    # In a more complex system, this could handle more logic
    return {
        "BDO_offering": allocation.offering_bdo,
        "BDO_retained": allocation.retained_bdo,
        "GoTyme_savings": allocation.gotyme_savings,
        "GoTyme_emergency": allocation.gotyme_emergency,
        "GCash_food": allocation.gcash_food,
        "GCash_bills": allocation.gcash_bills,
        "GCash_fun": allocation.gcash_fun,
        "GCash_buffer": allocation.gcash_buffer,
    }


def get_account_summary(routing: Dict[str, Decimal]) -> Dict[str, Decimal]:
    """Summarize amounts per account."""
    summary = {}
    for key, amount in routing.items():
        account = key.split("_")[0]
        summary[account] = summary.get(account, Decimal("0")) + amount
    return summary