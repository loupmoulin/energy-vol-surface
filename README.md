# Energy Commodity Volatility Surface Calibration

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-12%20passing-brightgreen)](#running-tests)

Front-office quantitative library for energy commodity derivatives (**WTI**, **Brent**, **Natural Gas**).

It implements Black-76 implied volatility inversion, the Hagan asymptotic SABR smile expansion, static calendar and butterfly no-arbitrage checks, and interactive 3D volatility surface visualizations with Plotly.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Project Structure](#project-structure)
- [Mathematical Formulation](#mathematical-formulation)
- [Running Tests](#running-tests)
- [References](#references)

---

## Features

- **Black-76 pricing**: closed-form call/put prices, Greeks, and a robust implied volatility solver
- **SABR calibration**: Hagan (2002) expansion with a numerically stable `z → 0` (ATM) limit
- **Slice optimization**: L-BFGS-B calibration per maturity with RMSE diagnostics
- **No-arbitrage checks**: butterfly (Breeden-Litzenberger density) and calendar spread tests
- **Visualization**: 2D smile slices and interactive 3D volatility surfaces (Plotly)

---

## Installation

```bash
git clone https://github.com/<your-username>/energy-vol-surface.git
cd energy-vol-surface
pip install -e .
```

Requires Python 3.10 or newer.

---

## Quickstart

Run the main.py

## Project Structure

```text
energy-vol-surface/
├── src/vol_surface/
│   ├── __init__.py               # Top-level API exports
│   ├── black76.py                # Black-76 closed forms, Greeks, and IV solver
│   ├── sabr.py                   # Hagan SABR expansion with z -> 0 stability
│   ├── calibrator.py             # L-BFGS-B slice optimization and RMSE metrics
│   ├── arbitrage.py              # Breeden-Litzenberger and calendar tests
│   └── visualization.py          # 2D smile slice and 3D surface renderers
├── tests/                        # Automated unit tests
├── pyproject.toml                # Build configuration and dependencies
└── README.md
```

---

## Mathematical Formulation

### 1. Black-76 Framework

For options on commodity futures, where $F$ is the forward price:

$$\text{Call} = e^{-rT}\left[F\,\Phi(d_1) - K\,\Phi(d_2)\right]$$

$$\text{Put} = e^{-rT}\left[K\,\Phi(-d_2) - F\,\Phi(-d_1)\right]$$

with

$$d_1 = \frac{\ln(F/K) + \tfrac{1}{2}\sigma^2 T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}$$

### 2. Hagan SABR Expansion (2002)

Under the forward dynamics

$$dF_t = \sigma_t F_t^{\beta}\, dW_t^1, \qquad d\sigma_t = \nu\,\sigma_t\, dW_t^2, \qquad d\langle W^1, W^2\rangle_t = \rho\, dt$$

the implied Black volatility is approximated by

$$\sigma_{\text{SABR}}(F,K) \approx \frac{\alpha}{(FK)^{\frac{1-\beta}{2}}\left[1 + \frac{(1-\beta)^2}{24}\ln^2\frac{F}{K} + \frac{(1-\beta)^4}{1920}\ln^4\frac{F}{K}\right]} \cdot \frac{z}{x(z)} \cdot \left[1 + \left(\frac{(1-\beta)^2}{24}\frac{\alpha^2}{(FK)^{1-\beta}} + \frac{1}{4}\frac{\rho\beta\nu\alpha}{(FK)^{\frac{1-\beta}{2}}} + \frac{2-3\rho^2}{24}\nu^2\right)T\right]$$

where

$$z = \frac{\nu}{\alpha}(FK)^{\frac{1-\beta}{2}}\ln\frac{F}{K}, \qquad x(z) = \ln\!\left(\frac{\sqrt{1-2\rho z + z^2} + z - \rho}{1-\rho}\right)$$

**ATM limit** ($K \to F$, i.e. $z \to 0$), used for numerical stability:

$$\frac{z}{x(z)} = 1 - \frac{\rho}{2}\,z + O(z^2)$$

### 3. Static No-Arbitrage Conditions

- **Calendar spread:** total implied variance $w(K,T) = \sigma^2(K,T)\,T$ must be non-decreasing in maturity:

  $$\frac{\partial w(K,T)}{\partial T} \ge 0$$

- **Butterfly spread:** the Breeden-Litzenberger risk-neutral density must be non-negative:

  $$g(K) = e^{rT}\,\frac{\partial^2 C(K)}{\partial K^2} \ge 0 \qquad \forall K > 0$$

---

## Running Tests

```bash
pytest -v
```

---

## References

- Hagan, P. S., Kumar, D., Lesniewski, A. S., & Woodward, D. E. (2002). *Managing Smile Risk*. Wilmott Magazine.
- Black, F. (1976). *The pricing of commodity contracts*. Journal of Financial Economics, 3(1-2), 167-179.
- Breeden, D. T., & Litzenberger, R. H. (1978). *Prices of state-contingent claims implicit in option prices*. Journal of Business, 51(4), 621-651.

---

