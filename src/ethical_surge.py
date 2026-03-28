"""
Ethical surge pricing engine.
Extends BaselineSurgeEngine with constraints derived from:
  - Utilitarianism (EG-3): driver share guarantee
  - Deontology (EG-5): transparency logging
  - Care Ethics (EG-2, EG-7): emergency and low-income caps
"""

import json
import datetime
from src.baseline_surge import BaselineSurgeEngine

POVERTY_LINE = 30_000  # annual median income threshold


class EthicalSurgeEngine(BaselineSurgeEngine):
    """Surge engine with ethical constraints layered on top."""

    def __init__(self, min_driver_share=0.75):
        self.min_driver_share = min_driver_share
        self.transparency_log = []

    def calculate_surge(self, zone, context):
        """Compute a constrained surge multiplier.

        Args:
            zone: object with .demand, .supply, .median_income, .id
            context: object with .is_emergency (bool)
        """
        mult = super().calculate_surge(zone)
        constraints = []

        # Care Ethics EG-7: lower cap in low-income zones
        if zone.median_income < POVERTY_LINE:
            capped = min(mult, 1.5)
            if capped < mult:
                constraints.append("low_income_cap_1.5x")
            mult = capped

        # Care Ethics EG-2: emergency cap
        if context.is_emergency:
            capped = min(mult, 1.2)
            if capped < mult:
                constraints.append("emergency_cap_1.2x")
            mult = capped

        # Deontological EG-5: log reasoning
        self._log(zone, mult, constraints)

        return mult

    def enforce_driver_share(self, rider_fare, base_fare):
        """Return the minimum driver payment for a trip.

        Ensures the driver receives at least self.min_driver_share of the
        total fare, implementing EG-3 (utilitarian) and EG-9 (care ethics).
        """
        return max(rider_fare * self.min_driver_share, base_fare)

    def _log(self, zone, mult, constraints):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "zone_id": zone.id,
            "demand": int(zone.demand),
            "supply": int(zone.supply),
            "ratio": round(float(zone.demand) / max(int(zone.supply), 1), 2),
            "median_income": float(zone.median_income),
            "multiplier": mult,
            "constraints_applied": constraints if constraints else ["none"],
        }
        self.transparency_log.append(entry)

    def print_log(self, last_n=5):
        """Print the most recent log entries."""
        for entry in self.transparency_log[-last_n:]:
            print(json.dumps(entry, indent=2))
