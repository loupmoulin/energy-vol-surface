"""SABR implied volatility formula (Hagan et al., 2002)."""
import numpy as np

def sabr_vol(F: float, K: float, T: float, alpha: float, beta: float, rho: float, nu: float) -> float:
    """Computes Black-76 implied volatility using Hagan's SABR expansion."""
    if F<=0 or K<=0 or alpha<=0 or nu<0 or T<=0:
        return 0.0
    if abs(rho)>=1.0:
        raise ValueError("rho must lie in (-1, 1)")
    if abs(F-K)<1e-6:
        f_b=F**(1-beta)
        t1=alpha/f_b
        t2=1+(((1-beta)**2/24)*(alpha**2/(F**(2-2*beta)))+0.25*(rho*beta*nu*alpha)/f_b+((2-3*rho**2)/24)*(nu**2))*T
        return t1*t2
    log_fk=np.log(F/K)
    fk_b=(F*K)**((1-beta)/2)
    z=(nu/alpha)*fk_b*log_fk
    if abs(z)<1e-5:
        xz_ratio=1.0+0.5*rho*z
    else:
        arg=np.sqrt(1-2*rho*z+z**2)+z-rho
        if arg<=0 or (1-rho)<=0:
            return 0.0
        xz_ratio=z/np.log(arg/(1-rho))
    denom=fk_b*(1+((1-beta)**2/24)*(log_fk**2)+((1-beta)**4/1920)*(log_fk**4))
    num=1+(((1-beta)**2/24)*(alpha**2/((F*K)**(1-beta)))+0.25*(rho*beta*nu*alpha)/fk_b+((2-3*rho**2)/24)*(nu**2))*T
    return (alpha/denom)*xz_ratio*num
