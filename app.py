"""CLI entry point for the Payday Finance App."""

from datetime import datetime
from decimal import Decimal
from src.config import DEFAULT_BUDGET, MIN_BDO_RETAINED
from src.models import PayoutInput, BudgetConfig, HistoryEntry
from src.finance_engine import allocate_payout
from src.reporting import generate_payout_report, generate_monthly_summary
from src.storage import Storage


def main():
    """Run a sample payout calculation."""
    # Sample payout
    payout_amount = Decimal("7500.00")
    retained_bdo = MIN_BDO_RETAINED
    budget = BudgetConfig(**DEFAULT_BUDGET)

    payout_input = PayoutInput(
        amount=payout_amount,
        retained_bdo=retained_bdo,
        budget=budget
    )

    # Calculate allocation
    allocation = allocate_payout(payout_input)

    # Generate report
    report = generate_payout_report(allocation)
    print(report)

    # Save to history
    storage = Storage()
    entry = HistoryEntry(
        date=datetime.now().isoformat(),
        payout_input=payout_input,
        allocation=allocation
    )
    storage.save_history_entry(entry)

    # Show monthly summary
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_history = storage.get_history_by_month(current_year, current_month)
    monthly_report = generate_monthly_summary(monthly_history)
    print("\n" + monthly_report)


if __name__ == "__main__":
    main()