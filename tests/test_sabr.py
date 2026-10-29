import numpy as np
import pytest
from vol_surface.sabr import sabr_vol

def test_sabr_atm():
    F,T,alpha,beta,rho,nu=100.0,1.0,0.3,0.7,-0.2,0.4
    vol_atm=sabr_vol(F,F,T,alpha,beta,rho,nu)
    vol_near=sabr_vol(F,F+1e-5,T,alpha,beta,rho,nu)
    assert np.isclose(vol_atm,vol_near,atol=1e-4)

def test_sabr_positive():
    F,T,alpha,beta,rho,nu=80.0,0.5,0.25,0.5,-0.1,0.3
    for K in [50.0,70.0,80.0,90.0,120.0]:
        assert sabr_vol(F,K,T,alpha,beta,rho,nu)>0.0

def test_sabr_rho_bounds():
    with pytest.raises(ValueError):
        sabr_vol(100.0,100.0,1.0,0.2,0.5,1.0,0.3)
