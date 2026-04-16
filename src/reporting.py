"""Reporting module for generating summaries."""

from decimal import Decimal
from .models import AllocationResult
from .allocator import route_to_accounts, get_account_summary


def generate_payout_report(allocation: AllocationResult) -> str:
    """Generate a text report for a payout allocation."""
    routing = route_to_accounts(allocation)
    account_summary = get_account_summary(routing)

    report = f"""
Payday Allocation Report
========================

Total Payout: PHP {allocation.total_allocated + allocation.unallocated_or_rounding_difference:.2f}

Allocations:
- Offering (BDO): PHP {allocation.offering_bdo:.2f}
- Retained (BDO): PHP {allocation.retained_bdo:.2f}
- Savings (GoTyme): PHP {allocation.gotyme_savings:.2f}
- Emergency (GoTyme): PHP {allocation.gotyme_emergency:.2f}
- Food (GCash): PHP {allocation.gcash_food:.2f}
- Bills (GCash): PHP {allocation.gcash_bills:.2f}
- Fun (GCash): PHP {allocation.gcash_fun:.2f}
- Buffer (GCash): PHP {allocation.gcash_buffer:.2f}

Account Summary:
"""
    for account, total in account_summary.items():
        report += f"- {account}: PHP {total:.2f}\n"

    report += f"\nTotal Allocated: PHP {allocation.total_allocated:.2f}\n"
    if allocation.unallocated_or_rounding_difference != 0:
        report += f"Rounding Difference: PHP {allocation.unallocated_or_rounding_difference:.2f}\n"

    return report


def generate_monthly_summary(history: List[dict]) -> str:
    """Generate a monthly summary from history."""
    # TODO: Implement monthly aggregation
    return "Monthly summary not yet implemented."