"""Reporting module for generating summaries."""

from collections import defaultdict
from decimal import Decimal
from typing import List, Dict
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
    """Generate a monthly summary from history entries."""
    if not history:
        return "No payout history available for this period."
    
    # Aggregate totals
    total_payouts = len(history)
    total_amount = Decimal("0")
    
    category_totals = defaultdict(Decimal)
    account_totals = defaultdict(Decimal)
    
    for entry in history:
        allocation = entry["allocation"]
        total_amount += Decimal(str(allocation["total_allocated"])) + Decimal(str(allocation["unallocated_or_rounding_difference"]))
        
        # Sum categories
        category_totals["offering_bdo"] += Decimal(str(allocation["offering_bdo"]))
        category_totals["retained_bdo"] += Decimal(str(allocation["retained_bdo"]))
        category_totals["gotyme_savings"] += Decimal(str(allocation["gotyme_savings"]))
        category_totals["gotyme_emergency"] += Decimal(str(allocation["gotyme_emergency"]))
        category_totals["gcash_food"] += Decimal(str(allocation["gcash_food"]))
        category_totals["gcash_bills"] += Decimal(str(allocation["gcash_bills"]))
        category_totals["gcash_fun"] += Decimal(str(allocation["gcash_fun"]))
        category_totals["gcash_buffer"] += Decimal(str(allocation["gcash_buffer"]))
    
    # Calculate account totals from category totals
    account_totals["BDO"] = category_totals["offering_bdo"] + category_totals["retained_bdo"]
    account_totals["GoTyme"] = category_totals["gotyme_savings"] + category_totals["gotyme_emergency"]
    account_totals["GCash"] = (
        category_totals["gcash_food"] + category_totals["gcash_bills"] + 
        category_totals["gcash_fun"] + category_totals["gcash_buffer"]
    )
    
    # Generate report
    report = f"""
Monthly Allocation Summary
==========================

Total Payouts: {total_payouts}
Total Amount Processed: PHP {total_amount:.2f}

Monthly Category Totals:
- Offering (BDO): PHP {category_totals["offering_bdo"]:.2f}
- Retained (BDO): PHP {category_totals["retained_bdo"]:.2f}
- Savings (GoTyme): PHP {category_totals["gotyme_savings"]:.2f}
- Emergency (GoTyme): PHP {category_totals["gotyme_emergency"]:.2f}
- Food (GCash): PHP {category_totals["gcash_food"]:.2f}
- Bills (GCash): PHP {category_totals["gcash_bills"]:.2f}
- Fun (GCash): PHP {category_totals["gcash_fun"]:.2f}
- Buffer (GCash): PHP {category_totals["gcash_buffer"]:.2f}

Monthly Account Totals:
"""
    for account, total in account_totals.items():
        report += f"- {account}: PHP {total:.2f}\n"
    
    return report