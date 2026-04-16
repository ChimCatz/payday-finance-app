# Architecture

## Overview
The Payday Finance App follows a modular architecture with clear separation of concerns to ensure maintainability and testability.

## Core Modules

### models.py
Contains Pydantic data models for:
- PayoutInput
- BudgetConfig
- AllocationResult
- HistoryEntry

### finance_engine.py
Implements core business logic:
- Percentage calculations
- Minimum balance enforcement
- Rounding logic

### allocator.py
Handles account routing:
- Maps categories to specific accounts
- Generates structured allocation output

### validators.py
Input validation:
- Payout amount validation
- Percentage total validation
- Configuration validation

### storage.py
Data persistence:
- Save/load allocation history
- Configuration storage
- Uses JSON or SQLite backend

### reporting.py
Output generation:
- Text summaries
- Per-payout reports
- Monthly aggregation

### app.py
Entry point:
- CLI interface
- Orchestrates the flow
- Replaceable with UI later

## Design Principles
- Dependency injection for testability
- Pure functions where possible
- Clear error handling
- Type safety with hints
- Documentation first