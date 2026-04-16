"""Storage module for persisting data locally."""

import json
from pathlib import Path
from typing import List
from .models import HistoryEntry


class Storage:
    """Simple JSON-based storage for history."""

    def __init__(self, data_dir: Path = Path("data")):
        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)
        self.history_file = self.data_dir / "history.json"

    def save_history_entry(self, entry: HistoryEntry) -> None:
        """Save a history entry."""
        history = self.load_history()
        history.append(entry.dict())
        with open(self.history_file, "w") as f:
            json.dump(history, f, indent=2, default=str)

    def load_history(self) -> List[dict]:
        """Load history entries."""
        if not self.history_file.exists():
            return []
        with open(self.history_file, "r") as f:
            return json.load(f)

    # TODO: Add methods for configuration storage