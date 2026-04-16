"""Storage module for persisting data locally."""

import json
import sqlite3
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional
from .models import HistoryEntry


class Storage:
    """SQLite-based storage for history with JSON fallback."""

    def __init__(self, data_dir: Path = Path("data")):
        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)
        self.db_file = self.data_dir / "history.db"
        self.history_file = self.data_dir / "history.json"  # Fallback
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database and create tables."""
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    payout_input TEXT NOT NULL,
                    allocation TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_history_entry(self, entry: HistoryEntry) -> None:
        """Save a history entry to SQLite."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute("""
                    INSERT INTO history (date, payout_input, allocation)
                    VALUES (?, ?, ?)
                """, (
                    entry.date,
                    json.dumps(entry.payout_input.dict(), default=str),
                    json.dumps(entry.allocation.dict(), default=str)
                ))
                conn.commit()
        except sqlite3.Error:
            # Fallback to JSON
            self._save_to_json(entry)

    def _save_to_json(self, entry: HistoryEntry) -> None:
        """Fallback JSON storage."""
        history = self._load_from_json()
        history.append(entry.dict())
        with open(self.history_file, "w") as f:
            json.dump(history, f, indent=2, default=str)

    def load_history(self) -> List[dict]:
        """Load history entries from SQLite."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.execute("""
                    SELECT date, payout_input, allocation FROM history
                    ORDER BY date DESC
                """)
                rows = cursor.fetchall()
                history = []
                for row in rows:
                    history.append({
                        "date": row[0],
                        "payout_input": json.loads(row[1]),
                        "allocation": json.loads(row[2])
                    })
                return history
        except sqlite3.Error:
            # Fallback to JSON
            return self._load_from_json()

    def _load_from_json(self) -> List[dict]:
        """Load from JSON fallback."""
        if not self.history_file.exists():
            return []
        with open(self.history_file, "r") as f:
            return json.load(f)

    def get_history_by_date_range(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[dict]:
        """Get history entries within a date range."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                query = "SELECT date, payout_input, allocation FROM history"
                params = []
                
                conditions = []
                if start_date:
                    conditions.append("date >= ?")
                    params.append(start_date.isoformat())
                if end_date:
                    conditions.append("date <= ?")
                    params.append(end_date.isoformat())
                
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
                
                query += " ORDER BY date DESC"
                
                cursor = conn.execute(query, params)
                rows = cursor.fetchall()
                history = []
                for row in rows:
                    history.append({
                        "date": row[0],
                        "payout_input": json.loads(row[1]),
                        "allocation": json.loads(row[2])
                    })
                return history
        except sqlite3.Error:
            # Fallback to JSON filtering
            history = self._load_from_json()
            if not start_date and not end_date:
                return history
            
            filtered = []
            for entry in history:
                entry_date = datetime.fromisoformat(entry["date"]).date()
                if start_date and entry_date < start_date:
                    continue
                if end_date and entry_date > end_date:
                    continue
                filtered.append(entry)
            return filtered

    def get_history_by_month(self, year: int, month: int) -> List[dict]:
        """Get history entries for a specific month."""
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        end_date = end_date.replace(day=1)  # First day of next month
        return self.get_history_by_date_range(start_date, end_date)