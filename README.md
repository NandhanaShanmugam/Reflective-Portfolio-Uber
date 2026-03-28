# Reflective Portfolio: Uber Surge Pricing Ethics

**COMP41820 – AI and Ethics**  
UCD School of Computer Science, MSc in Advanced AI  
Supervisor: Vivek Nallur

## Team
- Vishal Jayasankar (25228377)
- Nandhana Shanmugam Vijayalakshmi (25220650)

## Overview

This repository contains the code for our reflective portfolio analysing the ethical dimensions of Uber's surge pricing algorithm. The project examines tensions between functional goals (supply-demand balancing, revenue) and ethical goals (fairness, transparency, vulnerability protection) using three ethical frameworks: Utilitarianism, Deontological Ethics, and Care Ethics.

## Structure

```
├── src/
│   ├── models.py             # Data classes (Zone, Context, Trip)
│   ├── baseline_surge.py     # Baseline surge engine (no ethical constraints)
│   ├── ethical_surge.py      # Ethical surge engine (with constraints)
│   ├── fairness_audit.py     # Neighbourhood fairness auditor
│   ├── pay_monitor.py        # Driver pay transparency monitor
│   └── run_demo.py           # Main demo script (Chapter 3 validation)
├── simulations/
│   ├── personalised_pricing_sim.py   # Chapter 5: personalised vs uniform pricing
│   └── driver_share_sim.py           # Chapter 6: fixed vs split driver share
└── README.md
```

## Requirements

```
Python 3.9+
numpy
scipy
```

Install: `pip install numpy scipy`

## Running

```bash
# Chapter 3 validation (all components)
python src/run_demo.py

# Chapter 5 simulation (Vishal's argument)
python simulations/personalised_pricing_sim.py

# Chapter 6 simulation (Nandhana's argument)
python simulations/driver_share_sim.py
```

## Components

### Baseline Surge Engine
Pure supply-demand pricing with no ethical constraints. Calculates a multiplier from the demand/supply ratio, capped at 5.0x.

### Ethical Surge Engine
Extends the baseline with:
- **Emergency cap** (1.2x) during declared emergencies (Care Ethics EG-2)
- **Low-income zone cap** (1.5x) for zones below the poverty threshold (Care Ethics EG-7)
- **Transparency logging** for every pricing decision (Deontology EG-5)
- **Driver share guarantee** of 75% minimum (Utilitarianism EG-3)

### Fairness Auditor
Tests for statistically significant correlation between average surge multiplier and neighbourhood median income. Flags potential disparate impact.

### Pay Monitor
Checks each trip for excessive platform commission (>25%) and whether surge revenue is actually passed to drivers.
