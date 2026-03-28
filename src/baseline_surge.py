"""
Baseline surge pricing engine.
Computes a surge multiplier from supply-demand ratio alone.
No ethical constraints are applied.
"""


class BaselineSurgeEngine:
    """Pure supply-demand surge calculator."""

    def calculate_surge(self, zone):
        """Return a multiplier (float) for the given zone.

        Args:
            zone: object with .demand (int) and .supply (int) attributes.
        """
        ratio = zone.demand / max(zone.supply, 1)

        if ratio > 2.0:
            return min(round(ratio * 0.8, 1), 5.0)
        elif ratio > 1.2:
            return round(1.0 + (ratio - 1.0) * 0.5, 1)
        return 1.0
