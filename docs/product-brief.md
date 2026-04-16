# Product Brief

## Goal
Build a Python-first MVP for a personal finance app focused on payday allocation, multi-account routing, and percentage-based budgeting for Philippine users. The main value is a clear finance engine that tells the user what to do with each payout.

## Background
Target user is a Data Analyst with basic-intermediate Python skills using VS Code and AI-assisted coding. Project structured for long-term maintainability and easy context loading.

## Vision
Help users:
- Enter payout amounts
- Apply budget percentages and fixed rules
- Keep required retained amount in main bank account
- Separate offering, savings, emergency fund, daily spending, guilt-free spending, and buffer
- Route money into different account buckets (BDO, GoTyme, GCash)
- Generate per-payout and monthly summaries
- Keep simple history
- Support changing percentages later

## Core Finance Logic
Default budgeting model:
- Offering: 10%
- Savings: 17%
- Emergency fund: 7%
- Food: 20%
- Bills: 9%
- Fun money: 12%
- Buffer: 25%

Adjustments:
- Always retain at least PHP 500 in BDO
- Offering stays in BDO
- Savings and Emergency go to GoTyme as separate categories
- Daily spending categories go to GCash
- Fun money = guilt-free spending
- Savings and emergency never mixed

## Scope
Build: Python logic, local storage, tests, clean docs, repo structure for Flet later.
Do NOT build: mobile packaging, bank APIs, auth, cloud sync, OCR, AI chat, investments, debt, notifications.