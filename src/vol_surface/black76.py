"""Black-76 pricing, greeks and implied volatility solver."""
import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

def black76_price(F: float, K: float, T: float, r: float, sigma: float, option_type: str = "call") -> float:
    if F<=0 or K<=0:
        raise ValueError("F and K must be positive")
    disc=np.exp(-r*T)
    if T<=0 or sigma<=0:
        return disc*max(0.0,F-K) if option_type=="call" else disc*max(0.0,K-F)
    d1=(np.log(F/K)+0.5*sigma**2*T)/(sigma*np.sqrt(T))
    d2=d1-sigma*np.sqrt(T)
    if option_type=="call":
        return disc*(F*norm.cdf(d1)-K*norm.cdf(d2))
    elif option_type=="put":
        return disc*(K*norm.cdf(-d2)-F*norm.cdf(-d1))
    raise ValueError("option_type must be 'call' or 'put'")

def black76_vega(F: float, K: float, T: float, r: float, sigma: float) -> float:
    if T<=0 or sigma<=0 or F<=0 or K<=0:
        return 0.0
    d1=(np.log(F/K)+0.5*sigma**2*T)/(sigma*np.sqrt(T))
    return np.exp(-r*T)*F*np.sqrt(T)*norm.pdf(d1)

def black76_delta(F: float, K: float, T: float, r: float, sigma: float, option_type: str = "call") -> float:
    if T<=0 or sigma<=0:
        if option_type=="call":
            return np.exp(-r*T) if F>K else 0.0
        return -np.exp(-r*T) if F<K else 0.0
    d1=(np.log(F/K)+0.5*sigma**2*T)/(sigma*np.sqrt(T))
    disc=np.exp(-r*T)
    return disc*norm.cdf(d1) if option_type=="call" else -disc*norm.cdf(-d1)

def black76_gamma(F: float, K: float, T: float, r: float, sigma: float) -> float:
    if T<=0 or sigma<=0 or F<=0 or K<=0:
        return 0.0
    d1=(np.log(F/K)+0.5*sigma**2*T)/(sigma*np.sqrt(T))
    return (np.exp(-r*T)*norm.pdf(d1))/(F*sigma*np.sqrt(T))

def implied_volatility(price: float, F: float, K: float, T: float, r: float, option_type: str = "call", tol: float = 1e-8, max_iter: int = 100) -> float:
    disc=np.exp(-r*T)
    intrinsic=disc*(max(0.0,F-K) if option_type=="call" else max(0.0,K-F))
    if price<=intrinsic:
        return 0.0
    max_price=disc*F if option_type=="call" else disc*K
    if price>=max_price:
        return np.nan
    sigma=0.3
    for _ in range(max_iter):
        p=black76_price(F,K,T,r,sigma,option_type)
        v=black76_vega(F,K,T,r,sigma)
        diff=p-price
        if abs(diff)<tol:
            return sigma
        if v<1e-12:
            break
        sigma-=diff/v
        if sigma<=0 or sigma>5.0:
            break
    def obj(s: float) -> float:
        return black76_price(F,K,T,r,s,option_type)-price
    try:
        return brentq(obj,1e-5,5.0,xtol=tol)
    except (ValueError,RuntimeError):
        return np.nan