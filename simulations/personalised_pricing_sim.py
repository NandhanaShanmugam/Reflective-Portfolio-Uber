import numpy as np
from collections import defaultdict

np.random.seed(42)

NUM_RIDERS = 500
BASE_FARE = 15.0
SURGE = 2.0  # peak-hour scenario


class Rider:
    def __init__(self, rid):
        self.id = rid
        self.income = np.random.lognormal(mean=10.5, sigma=0.6)
        self.booking_freq = np.random.poisson(lam=8)
        self.device_tier = np.random.choice(
            ["budget", "mid", "premium"], p=[0.4, 0.35, 0.25]
        )


def wtp_score(rider):
    """Predict willingness-to-pay from personal features."""
    score = 0.5
    if rider.device_tier == "premium":
        score += 0.2
    if rider.booking_freq > 12:
        score += 0.15
    if rider.income > 60_000:
        score += 0.15
    return min(score, 1.0)


def personalised_fare(rider, surge):
    return BASE_FARE * surge * (1 + 0.3 * wtp_score(rider))


def uniform_fare(rider, surge):
    return BASE_FARE * surge


def main():
    riders = [Rider(i) for i in range(NUM_RIDERS)]

    # Compare fares
    by_device = defaultdict(list)
    by_freq = {"low": [], "medium": [], "high": []}

    for r in riders:
        p_fare = personalised_fare(r, SURGE)
        u_fare = uniform_fare(r, SURGE)
        premium_pct = (p_fare - u_fare) / u_fare * 100
        by_device[r.device_tier].append(premium_pct)

        if r.booking_freq <= 5:
            by_freq["low"].append(premium_pct)
        elif r.booking_freq <= 12:
            by_freq["medium"].append(premium_pct)
        else:
            by_freq["high"].append(premium_pct)

    print("=" * 50)
    print("PERSONALISED vs UNIFORM PRICING")
    print("=" * 50)

    print("\nBy device tier:")
    for tier in ["budget", "mid", "premium"]:
        avg = np.mean(by_device[tier])
        print(f"  {tier:>8s}: avg premium = {avg:+.1f}%")

    print("\nBy booking frequency:")
    for label in ["low", "medium", "high"]:
        avg = np.mean(by_freq[label])
        count = len(by_freq[label])
        print(f"  {label:>8s} ({count:3d} riders): avg premium = {avg:+.1f}%")

    print("\nKey finding: frequent bookers (often commuters) pay MORE")
    print("because high frequency signals captive demand, not wealth.")


if __name__ == "__main__":
    main()
