import numpy as np

np.random.seed(42)

WEEKS = 52
TRIPS_PER_WEEK = 45
BASE_FARE = 15.0


def simulate_weekly_income(base_share, model):
    """Simulate a driver's income over one year.

    Args:
        base_share: float, the base driver share (e.g. 0.75 or 0.65)
        model: 'fixed' or 'split'

    Returns:
        list of 52 weekly income values.
    """
    weekly_incomes = []

    for _ in range(WEEKS):
        income = 0.0
        surge_trips = 0

        for _ in range(TRIPS_PER_WEEK):
            r = np.random.random()
            if r < 0.80:
                surge = 1.0
            elif r < 0.95:
                surge = np.random.uniform(1.1, 1.5)
            else:
                surge = np.random.uniform(1.5, 3.0)
                surge_trips += 1

            fare = BASE_FARE * surge

            if model == "fixed":
                income += fare * base_share
            else:
                # base share on base fare, 100% of surge increment to driver
                base_part = BASE_FARE * base_share
                surge_increment = max(0, fare - BASE_FARE)
                income += base_part + surge_increment

        weekly_incomes.append(round(income, 2))

    return weekly_incomes


def main():
    fixed = simulate_weekly_income(0.75, "fixed")
    split = simulate_weekly_income(0.65, "split")

    print("=" * 50)
    print("DRIVER INCOME COMPARISON")
    print("=" * 50)

    print(f"\nFixed 75% model:")
    print(f"  Annual income:  EUR {sum(fixed):,.0f}")
    print(f"  Avg weekly:     EUR {np.mean(fixed):,.0f}")
    print(f"  Min week:       EUR {min(fixed):,.0f}")
    print(f"  Max week:       EUR {max(fixed):,.0f}")

    print(f"\nChatGPT split model (65% base + 100% surge):")
    print(f"  Annual income:  EUR {sum(split):,.0f}")
    print(f"  Avg weekly:     EUR {np.mean(split):,.0f}")
    print(f"  Min week:       EUR {min(split):,.0f}")
    print(f"  Max week:       EUR {max(split):,.0f}")

    diff = sum(fixed) - sum(split)
    print(f"\nDifference: EUR {diff:,.0f}/year in favour of fixed model")

    if diff > 0:
        print("\nConclusion: Fixed 75% is better for drivers overall.")
        print("The lower base share in the split model outweighs the")
        print("surge bonus because surge trips are only ~5% of all trips.")


if __name__ == "__main__":
    main()
