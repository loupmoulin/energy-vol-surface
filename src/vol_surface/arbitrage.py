"""Static no-arbitrage validation for volatility surfaces."""
import numpy as np
from vol_surface.black76 import black76_price

def check_calendar_arbitrage(vols_grid: np.ndarray, maturities: np.ndarray, tol: float = 1e-7) -> bool:
    """Verifies total variance is non-decreasing along maturities."""
    vols=np.asarray(vols_grid,dtype=float)
    T=np.asarray(maturities,dtype=float)[:,None]
    w=vols**2*T
    dw=np.diff(w,axis=0)
    return bool(np.all(dw>=-tol))

def compute_density(F: float, strikes: np.ndarray, vols: np.ndarray, T: float, r: float = 0.0) -> np.ndarray:
    """Computes Breeden-Litzenberger risk-neutral density via finite differences."""
    K=np.asarray(strikes,dtype=float)
    prices=np.array([black76_price(F,k,T,r,v) for k,v in zip(K,vols)])
    dK=np.diff(K)
    dC_dK=np.diff(prices)/dK
    mid_dK=0.5*(dK[:-1]+dK[1:])
    d2C_dK2=np.diff(dC_dK)/mid_dK
    return np.exp(r*T)*d2C_dK2

def check_butterfly_arbitrage(F: float, strikes: np.ndarray, vols: np.ndarray, T: float, r: float = 0.0, tol: float = 1e-6) -> bool:
    """Checks convexity of call prices to guarantee non-negative state prices."""
    density=compute_density(F,strikes,vols,T,r)
    return bool(np.all(density>=-tol))