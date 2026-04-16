# Payday Finance App - Agent Guidelines

## Project Purpose
Build a Python-first MVP for personal finance app focused on payday allocation, multi-account routing, and percentage-based budgeting for Philippine users. Priority: solid Python logic, testability, and clean repo structure.

## Coding Standards
- Use type hints everywhere reasonable
- Write simple code over clever code
- Include docstrings for all public functions/classes
- Avoid overengineering
- Keep modules focused
- Make output human-readable
- Follow PEP 8

## Architecture Summary
- `models.py`: Data structures and Pydantic models
- `finance_engine.py`: Core business rules and calculations
- `allocator.py`: Converts rules into account routing output
- `validators.py`: Input validation and error handling
- `storage.py`: Local persistence (JSON/SQLite)
- `reporting.py`: Text summaries and reports
- `app.py`: CLI entry point (replaceable with Flet UI later)

## Logic Placement
- Finance calculations: `finance_engine.py`
- Data validation: `validators.py`
- Account routing: `allocator.py`
- UI concerns: Keep out of core logic (prepare for Flet)

## Naming Conventions
- Functions: snake_case
- Classes: PascalCase
- Constants: UPPER_SNAKE_CASE
- Variables: snake_case
- Use descriptive names

## Testing Rules
- Write unit tests for all core logic
- Test edge cases and validation
- Use pytest framework
- Maintain high test coverage

## Rule: Avoid Changing Finance Logic Silently
Always document changes to finance calculations. Update tests and docs when modifying business rules.

## Rule: Update Docs When Behavior Changes
Keep README.md, AGENTS.md, and /docs in sync with code changes.

## Rule: Ask for Confirmation Before Large Refactors
For significant architectural changes, seek user confirmation.

## Rule: Keep AGENTS.md Short
Point to deeper docs in /docs for detailed information.