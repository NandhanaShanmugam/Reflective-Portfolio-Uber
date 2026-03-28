"""
Simple data classes used by the surge engines, auditor, and monitor.
"""

from dataclasses import dataclass, field


@dataclass
class Zone:
    id: str
    demand: int
    supply: int
    median_income: float = 50_000.0


@dataclass
class Context:
    is_emergency: bool = False


@dataclass
class Trip:
    rider_fare: float
    driver_pay: float
    surge: float
    base_rate: float
