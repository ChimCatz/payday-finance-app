# Payday Finance App

## Product Summary
A Python-based personal finance tool designed for Philippine users to manage payday allocations with percentage-based budgeting, multi-account routing, and clear financial guidance for each payout.

## Target User/Problem
Filipino workers who receive irregular or fixed paydays and need structured guidance on allocating funds across savings, expenses, and emergency reserves while maintaining minimum balances in primary accounts.

## MVP Scope
This MVP focuses on core finance logic for payout allocation, local storage of history, and text-based reporting. It does not include mobile packaging, bank integrations, authentication, or AI features.

## Features
- Percentage-based budget allocation with customizable rules
- Multi-account routing (BDO, GoTyme, GCash)
- Minimum retained balance enforcement
- Per-payout and monthly summary reports
- Simple history tracking
- Configurable budget percentages

## Stack
- Python 3.8+
- Pydantic for data validation
- pytest for testing
- Local JSON/SQLite storage

## Folder Structure
```
payday-finance-app/
├── README.md
├── AGENTS.md
├── .gitignore
├── pyproject.toml
├── .env.example
├── app.py
├── config.py
├── requirements.txt
├── docs/
│   ├── architecture.md
│   ├── product-brief.md
│   └── finance-rules.md
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── finance_engine.py
│   ├── allocator.py
│   ├── validators.py
│   ├── storage.py
│   ├── reporting.py
│   └── constants.py
├── tests/
│   ├── test_finance_engine.py
│   ├── test_allocator.py
│   └── test_validators.py
├── data/
│   └── .gitkeep
└── output/
    └── .gitkeep
```

## Setup Instructions
1. Clone or download the repository
2. Ensure Python 3.8+ is installed
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment: `venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`

## How to Run
Run the CLI app: `python app.py`

This will execute a sample payout calculation and display the allocation breakdown.

## How to Run Tests
Run tests with pytest: `pytest`

## Roadmap
- [ ] Add Flet UI for mobile/desktop interface
- [ ] Implement more storage backends
- [ ] Add export functionality
- [ ] Enhance reporting with charts
- [ ] Add configuration UI

## Design Principles
- Simple, maintainable Python code
- Clear separation of concerns
- Type hints and docstrings throughout
- Test-driven development
- Human-readable outputs
- Finance logic isolated from UI/storage

## Example Finance Flow
For a payout of PHP 7,500 with minimum BDO retention of PHP 500:

- Offering: 10% = PHP 750 (stays in BDO)
- Retained BDO: PHP 500 minimum
- Savings: 17% = PHP 1,275 (GoTyme)
- Emergency: 7% = PHP 525 (GoTyme)
- Food: 20% = PHP 1,500 (GCash)
- Bills: 9% = PHP 675 (GCash)
- Fun: 12% = PHP 900 (GCash)
- Buffer: 25% = PHP 1,875 (GCash)

Total allocated: PHP 7,500

## Disclaimer
This is a personal planning tool and not financial advice. Always consult with qualified financial professionals for personalized financial decisions.