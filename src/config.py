"""Configuration settings for the Payday Finance App."""

from decimal import Decimal

# Default budget percentages
DEFAULT_BUDGET = {
    "offering": Decimal("0.10"),
    "savings": Decimal("0.17"),
    "emergency": Decimal("0.07"),
    "food": Decimal("0.20"),
    "bills": Decimal("0.09"),
    "fun": Decimal("0.12"),
    "buffer": Decimal("0.25"),
}

# Minimum retained BDO amount
MIN_BDO_RETAINED = Decimal("500.00")

# Account routing
ACCOUNT_ROUTING = {
    "offering": "BDO",
    "retained": "BDO",
    "savings": "GoTyme",
    "emergency": "GoTyme",
    "food": "GCash",
    "bills": "GCash",
    "fun": "GCash",
    "buffer": "GCash",
}