"""SABR slice calibration using L-BFGS-B."""
from dataclasses import dataclass
import numpy as np
from scipy.optimize import minimize
from vol_surface.sabr import sabr_vol

@dataclass
class SabrParams:
    alpha: float
    beta: float
    rho: float
    nu: float
    rmse: float

def calibrate_sabr_slice(
    F: float,
    strikes: np.ndarray,
    market_vols: np.ndarray,
    T: float,
    beta: float = 0.7,
    weights: np.ndarray | None = None,
) -> SabrParams:
    """Calibrates alpha, rho, nu for a fixed beta on a maturity slice."""
    strikes=np.asarray(strikes,dtype=float)
    market_vols=np.asarray(market_vols,dtype=float)
    weights=np.ones_like(market_vols) if weights is None else np.asarray(weights,dtype=float)
    idx_atm=int(np.argmin(np.abs(strikes-F)))
    alpha_0=float(market_vols[idx_atm]*(F**(1-beta)))
    init_params=[max(alpha_0,1e-3),-0.2,0.4]
    bounds=[(1e-4,5.0),(-0.999,0.999),(1e-4,5.0)]

    def loss(p):
        a,r,n=p
        model_vols=np.array([sabr_vol(F,K,T,a,beta,r,n) for K in strikes])
        return float(np.sum(((model_vols-market_vols)*weights)**2))

    res=minimize(loss,init_params,method="L-BFGS-B",bounds=bounds)
    a_opt,r_opt,n_opt=res.x
    fitted=np.array([sabr_vol(F,K,T,a_opt,beta,r_opt,n_opt) for K in strikes])
    rmse=float(np.sqrt(np.mean((fitted-market_vols)**2)))
    return SabrParams(alpha=a_opt,beta=beta,rho=r_opt,nu=n_opt,rmse=rmse)