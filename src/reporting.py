"""Reporting module for generating summaries."""

from collections import defaultdict
from decimal import Decimal
from typing import List, Dict
from .models import AllocationResult
from .allocator import route_to_accounts, get_account_summary


def generate_payout_report(allocation: AllocationResult, payout_amount: Decimal) -> str:
    """Generate a text report for a payout allocation."""
    routing = route_to_accounts(allocation)
    account_summary = get_account_summary(routing)

    def calc_pct(amount: Decimal) -> str:
        if payout_amount == 0:
            return "0.00%"
        return f"{(amount / payout_amount * 100):.2f}%"

    report = f"""Payday Allocation Report
========================

Total Payout: PHP {payout_amount:.2f}

Allocations:
- Offering (BDO): PHP {allocation.offering_bdo:.2f} ({calc_pct(allocation.offering_bdo)})
- Retained (BDO): PHP {allocation.retained_bdo:.2f} ({calc_pct(allocation.retained_bdo)})
- Savings (GoTyme): PHP {allocation.gotyme_savings:.2f} ({calc_pct(allocation.gotyme_savings)})
- Emergency (GoTyme): PHP {allocation.gotyme_emergency:.2f} ({calc_pct(allocation.gotyme_emergency)})
- Food (GCash): PHP {allocation.gcash_food:.2f} ({calc_pct(allocation.gcash_food)})
- Bills (GCash): PHP {allocation.gcash_bills:.2f} ({calc_pct(allocation.gcash_bills)})
- Fun (GCash): PHP {allocation.gcash_fun:.2f} ({calc_pct(allocation.gcash_fun)})
- Buffer (GCash): PHP {allocation.gcash_buffer:.2f} ({calc_pct(allocation.gcash_buffer)})

Account Summary:
"""
    for account, total in account_summary.items():
        report += f"- {account}: PHP {total:.2f} ({calc_pct(total)})\n"

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
        payout_amount = Decimal(str(entry["payout_input"]["amount"]))
        total_amount += payout_amount
        
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
    
    def calc_pct(amount: Decimal) -> str:
        if total_amount == 0:
            return "0.00%"
        return f"{(amount / total_amount * 100):.2f}%"
    
    # Generate report
    report = f"""Monthly Allocation Summary
==========================

Total Payouts: {total_payouts}
Total Amount Processed: PHP {total_amount:.2f}

Monthly Category Totals:
- Offering (BDO): PHP {category_totals["offering_bdo"]:.2f} ({calc_pct(category_totals["offering_bdo"])})
- Retained (BDO): PHP {category_totals["retained_bdo"]:.2f} ({calc_pct(category_totals["retained_bdo"])})
- Savings (GoTyme): PHP {category_totals["gotyme_savings"]:.2f} ({calc_pct(category_totals["gotyme_savings"])})
- Emergency (GoTyme): PHP {category_totals["gotyme_emergency"]:.2f} ({calc_pct(category_totals["gotyme_emergency"])})
- Food (GCash): PHP {category_totals["gcash_food"]:.2f} ({calc_pct(category_totals["gcash_food"])})
- Bills (GCash): PHP {category_totals["gcash_bills"]:.2f} ({calc_pct(category_totals["gcash_bills"])})
- Fun (GCash): PHP {category_totals["gcash_fun"]:.2f} ({calc_pct(category_totals["gcash_fun"])})
- Buffer (GCash): PHP {category_totals["gcash_buffer"]:.2f} ({calc_pct(category_totals["gcash_buffer"])})

Monthly Account Totals:
"""
    for account, total in account_totals.items():
        report += f"- {account}: PHP {total:.2f} ({calc_pct(total)})\n"
    
    return report