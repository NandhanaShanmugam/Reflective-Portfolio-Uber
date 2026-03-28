"""
Fairness auditor.
Tests whether surge pricing disproportionately affects certain
neighbourhoods based on median income (EG-6, EG-7).
"""

from scipy.stats import pearsonr


class FairnessAuditor:
    """Audit surge history for neighbourhood-level disparities."""

    def audit(self, surge_log, demographics):
        """Check correlation between average surge and zone income.

        Args:
            surge_log: dict {zone_id: [list of multipliers]}
            demographics: dict {zone_id: {'median_income': float}}

        Returns:
            dict with correlation coefficient, p-value, and per-zone stats.
        """
        zone_stats = {}
        surges, incomes = [], []

        for zone_id, multipliers in surge_log.items():
            avg_surge = sum(multipliers) / len(multipliers)
            income = demographics[zone_id]["median_income"]
            zone_stats[zone_id] = {
                "avg_surge": round(avg_surge, 2),
                "median_income": income,
            }
            surges.append(avg_surge)
            incomes.append(income)

        corr, pval = pearsonr(surges, incomes)

        result = {
            "correlation": round(corr, 4),
            "p_value": round(pval, 6),
            "significant": pval < 0.05,
            "zone_stats": zone_stats,
        }

        if result["significant"]:
            print(
                f"WARNING: significant correlation between surge and income "
                f"(r={corr:.3f}, p={pval:.4f})"
            )
        else:
            print(f"OK: no significant correlation (r={corr:.3f}, p={pval:.4f})")

        return result
