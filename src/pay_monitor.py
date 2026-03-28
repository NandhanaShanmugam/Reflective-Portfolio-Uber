class PayMonitor:
    """Monitor platform commission and driver pay per trip."""

    MAX_PLATFORM_TAKE = 0.25  # platform keeps at most 25%

    def check(self, trip):
        
        alerts = []
        take_rate = 1 - (trip.driver_pay / trip.rider_fare)

        if take_rate > self.MAX_PLATFORM_TAKE:
            alerts.append(
                f"EXCESSIVE_TAKE: platform took {take_rate:.0%} "
                f"(cap: {self.MAX_PLATFORM_TAKE:.0%})"
            )

        if trip.surge > 1.0 and trip.driver_pay <= trip.base_rate:
            alerts.append(
                "SURGE_NOT_PASSED: rider paid surge but driver got base rate"
            )

        return alerts
