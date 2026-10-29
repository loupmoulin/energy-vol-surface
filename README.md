\# Energy Commodity Volatility Surface Calibration



\[!\[Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)

\[!\[License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



Front-office quantitative library for energy commodity derivatives (WTI, Brent, Natural Gas). Implements Black-76 implied volatility inversion, Hagan asymptotic SABR smile expansion, static calendar and butterfly no-arbitrage checks, and interactive 3D volatility surface visualizations via Plotly.



\## Mathematical Formulation



\### 1. Black-76 Framework

For commodity futures options where $F\_t$ is the forward price:



$$\\text{Call} = e^{-rT} \\left\[ F \\Phi(d\_1) - K \\Phi(d\_2) \\right]$$

$$\\text{Put} = e^{-rT} \\left\[ K \\Phi(-d\_2) - F \\Phi(-d\_1) \\right]$$



with:

$$d\_1 = \\frac{\\ln(F/K) + \\frac{1}{2}\\sigma^2 T}{\\sigma \\sqrt{T}}, \\quad d\_2 = d\_1 - \\sigma \\sqrt{T}$$



\### 2. Hagan SABR Expansion (2002)

Under forward dynamics $dF\_t = \\sigma\_t F\_t^\\beta dW\_t^1$ and $d\\sigma\_t = \\nu \\sigma\_t dW\_t^2$ with $d\\langle W^1, W^2 \\rangle\_t = \\rho dt$:



$$\\sigma\_{\\text{SABR}}(F, K) \\approx \\frac{\\alpha}{(FK)^{\\frac{1-\\beta}{2}} \\left\[ 1 + \\frac{(1-\\beta)^2}{24}\\ln^2\\left(\\frac{F}{K}\\right) + \\frac{(1-\\beta)^4}{1920}\\ln^4\\left(\\frac{F}{K}\\right) \\right]} \\cdot \\left(\\frac{z}{x(z)}\\right) \\cdot \\left\[ 1 + \\left( \\frac{(1-\\beta)^2}{24}\\frac{\\alpha^2}{(FK)^{1-\\beta}} + \\frac{1}{4}\\frac{\\rho \\beta \\nu \\alpha}{(FK)^{\\frac{1-\\beta}{2}}} + \\frac{2-3\\rho^2}{24}\\nu^2 \\right) T \\right]$$



where:

$$z = \\frac{\\nu}{\\alpha}(FK)^{\\frac{1-\\beta}{2}} \\ln\\left(\\frac{F}{K}\\right), \\quad x(z) = \\ln\\left( \\frac{\\sqrt{1 - 2\\rho z + z^2} + z - \\rho}{1 - \\rho} \\right)$$



Taylor expansion at ATM boundary $K \\to F$ ($z \\to 0$):

$$\\lim\_{z \\to 0} \\frac{z}{x(z)} = 1 + \\frac{1}{2}\\rho z$$



\### 3. Static No-Arbitrage Conditions

\* \*\*Calendar Arbitrage:\*\* Total variance $w(K, T) = \\sigma^2(K, T) \\cdot T$ must be non-decreasing across maturities:

&#x20; $$\\frac{\\partial w(K, T)}{\\partial T} \\ge 0$$

\* \*\*Butterfly Arbitrage:\*\* Breeden-Litzenberger risk-neutral density must be non-negative:

&#x20; $$g(K) = e^{rT} \\frac{\\partial^2 C(K)}{\\partial K^2} \\ge 0 \\quad \\forall K > 0$$



\## Project Structure



text

energy-vol-surface/

├── data/                         # Sample market option chains

├── notebooks/                    # Jupyter demonstration notebooks

├── src/vol\_surface/

│   ├── init.py               # Top-level API exports

│   ├── black76.py                # Black-76 closed forms, Greeks, and IV solver

│   ├── sabr.py                   # Hagan SABR expansion with z -> 0 stability

│   ├── calibrator.py             # L-BFGS-B slice optimization and RMSE metrics

│   ├── arbitrage.py              # Breeden-Litzenberger and calendar tests

│   └── visualization.py          # 2D smile slice and 3D surface renderers

├── tests/                        # Automated unit tests (12 passing tests)

├── pyproject.toml                # Build configuration and dependencies

└── README.md





\## Quickstart



python



import numpy as np

from vol\_surface import calibrate\_sabr\_slice, plot\_sabr\_slice, check\_butterfly\_arbitrage



F, T, beta = 82.50, 0.5, 0.7

strikes = np.array(\[65.0, 70.0, 75.0, 80.0, 82.5, 85.0, 90.0, 95.0, 100.0])

market\_vols = np.array(\[0.38, 0.35, 0.33, 0.31, 0.305, 0.30, 0.295, 0.30, 0.31])



params = calibrate\_sabr\_slice(F, strikes, market\_vols, T, beta=beta)

print(f"Alpha: {params.alpha:.4f}, Rho: {params.rho:.4f}, Nu: {params.nu:.4f}, RMSE: {params.rmse:.6f}")



valid = check\_butterfly\_arbitrage(F, strikes, market\_vols, T)

print(f"Arbitrage-free: {valid}")



fig = plot\_sabr\_slice(F, strikes, market\_vols, params, T)

fig.show()





\## Running Tests



bash 



pytest -v

