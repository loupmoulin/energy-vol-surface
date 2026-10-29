import numpy as np
from vol_surface.arbitrage import check_calendar_arbitrage, check_butterfly_arbitrage, compute_density

def test_calendar_arbitrage():
    maturities=np.array([0.25,0.5,1.0])
    valid_vols=np.full((3,5),0.20)
    assert check_calendar_arbitrage(valid_vols,maturities)

    invalid_vols=np.array([[0.5],[0.3],[0.1]])
    mat_test=np.array([0.1,0.2,0.3])
    assert not check_calendar_arbitrage(invalid_vols,mat_test)

def test_butterfly_arbitrage_flat_vol():
    F,T,r=100.0,1.0,0.0
    strikes=np.linspace(70.0,130.0,13)
    vols=np.full_like(strikes,0.25)
    assert check_butterfly_arbitrage(F,strikes,vols,T,r)

def test_butterfly_arbitrage_violation():
    F,T,r=100.0,1.0,0.0
    strikes=np.array([80.0,90.0,100.0,110.0,120.0])
    distorted_vols=np.array([0.60,0.05,0.70,0.05,0.60])
    assert not check_butterfly_arbitrage(F,strikes,distorted_vols,T,r)

def test_density_positive_on_valid_slice():
    F,T,r=100.0,0.5,0.02
    strikes=np.linspace(80.0,120.0,17)
    vols=np.full_like(strikes,0.22)
    density=compute_density(F,strikes,vols,T,r)
    assert np.all(density>=0.0)