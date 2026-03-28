from scipy.stats import pearsonr


class FairnessAuditor:
    """Audit surge history for neighbourhood-level disparities."""

    def audit(self, surge_log, demographics):
        
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
