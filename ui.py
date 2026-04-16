"""Flet UI prototype for Payday Finance App."""

import flet as ft
from decimal import Decimal
from datetime import datetime
from src.config import DEFAULT_BUDGET, MIN_BDO_RETAINED
from src.models import PayoutInput, BudgetConfig, HistoryEntry
from src.finance_engine import allocate_payout
from src.reporting import generate_payout_report, generate_monthly_summary
from src.storage import Storage


def main(page: ft.Page):
    """Main Flet app function."""
    page.title = "Payday Finance App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1200
    page.window_height = 900  # Increased height
    page.window_maximized = True  # Full height
    page.padding = 15

    # Title with icon
    title = ft.Row([
        ft.Icon(ft.Icons.CALCULATE, size=28, color=ft.Colors.BLUE),
        ft.Text("Payday Finance App", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Input fields with better styling
    payout_input = ft.TextField(
        label="Payout Amount (PHP)",
        value="7500.00",
        width=220,
        height=50,
        prefix_icon=ft.Icons.MONEY,
        border_color=ft.Colors.BLUE_400,
        text_size=14
    )

    retained_input = ft.TextField(
        label="Retained BDO Amount (PHP)",
        value=str(MIN_BDO_RETAINED),
        width=220,
        height=50,
        prefix_icon=ft.Icons.ACCOUNT_BALANCE,
        border_color=ft.Colors.BLUE_400,
        text_size=14
    )

    # Result display with better font
    result_text = ft.Text("", size=12, font_family="Consolas", selectable=True, no_wrap=False)

    # Monthly summary display with better font
    monthly_text = ft.Text("", size=12, font_family="Consolas", selectable=True, no_wrap=False)

    def calculate_allocation(e):
        """Handle calculate button click."""
        try:
            payout_amount = Decimal(payout_input.value)
            retained_bdo = Decimal(retained_input.value)

            budget = BudgetConfig(**DEFAULT_BUDGET)
            payout = PayoutInput(
                amount=payout_amount,
                retained_bdo=retained_bdo,
                budget=budget
            )

            allocation = allocate_payout(payout)

            # Generate reports
            report = generate_payout_report(allocation, payout_amount)
            result_text.value = report
            result_text.update()

            # Save to history
            storage = Storage()
            entry = HistoryEntry(
                date=datetime.now().isoformat(),
                payout_input=payout,
                allocation=allocation
            )
            storage.save_history_entry(entry)

            # Update monthly summary
            current_month = datetime.now().month
            current_year = datetime.now().year
            monthly_history = storage.get_history_by_month(current_year, current_month)
            monthly_report = generate_monthly_summary(monthly_history)
            monthly_text.value = monthly_report
            monthly_text.update()

        except Exception as ex:
            result_text.value = f"Error: {str(ex)}"
            result_text.update()
            monthly_text.value = ""
            monthly_text.update()

    # Calculate button with icon
    calc_button = ft.Button(
        "Calculate Allocation",
        icon=ft.Icons.PLAY_ARROW,
        on_click=calculate_allocation,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE
        ),
        height=50
    )

    # Input section
    input_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Enter Payout Details", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([payout_input, retained_input, calc_button], alignment=ft.MainAxisAlignment.START, spacing=15),
            ]),
            padding=15
        )
    )

    # Results section - side by side with scrollable content
    results_row = ft.Row([
        # Payout Allocation
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.RECEIPT, size=18, color=ft.Colors.BLUE),
                    ft.Text("Payout Allocation", size=14, weight=ft.FontWeight.BOLD)
                ], spacing=8),
                ft.Container(
                    content=ft.ListView(
                        controls=[result_text],
                        height=500,
                        spacing=0,
                        padding=10
                    ),
                    bgcolor=ft.Colors.BLUE_GREY_50,
                    border_radius=8,
                    expand=True
                )
            ]),
            width=550,
            height=550
        ),
        ft.VerticalDivider(width=1),
        # Monthly Summary
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.BAR_CHART, size=18, color=ft.Colors.GREEN),
                    ft.Text("Monthly Summary", size=14, weight=ft.FontWeight.BOLD)
                ], spacing=8),
                ft.Container(
                    content=ft.ListView(
                        controls=[monthly_text],
                        height=500,
                        spacing=0,
                        padding=10
                    ),
                    bgcolor=ft.Colors.GREEN_50,
                    border_radius=8,
                    expand=True
                )
            ]),
            width=550,
            height=550
        )
    ], alignment=ft.MainAxisAlignment.START, spacing=10)

    # Main layout
    page.add(
        title,
        ft.Container(height=10),
        input_card,
        ft.Container(height=15),
        results_row
    )


if __name__ == "__main__":
    ft.app(target=main)