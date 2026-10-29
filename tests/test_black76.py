import numpy as np
import pytest
from vol_surface.black76 import black76_price, black76_vega, black76_delta, implied_volatility

def test_put_call_parity():
    F,K,T,r,sigma=75.0,80.0,0.5,0.04,0.35
    call=black76_price(F,K,T,r,sigma,"call")
    put=black76_price(F,K,T,r,sigma,"put")
    assert np.isclose(call-put,np.exp(-r*T)*(F-K),atol=1e-10)

def test_implied_volatility_roundtrip():
    F,T,r,target_sigma=65.0,0.75,0.03,0.28
    for K in [50.0,65.0,85.0]:
        for opt in ["call","put"]:
            p=black76_price(F,K,T,r,target_sigma,opt)
            iv=implied_volatility(p,F,K,T,r,opt)
            assert np.isclose(iv,target_sigma,atol=1e-6)

def test_vega_positive():
    assert black76_vega(100.0,100.0,1.0,0.05,0.20)>0.0

def test_delta_bounds():
    assert 0.0<black76_delta(100.0,100.0,0.5,0.02,0.25,"call")<1.0
    assert -1.0<black76_delta(100.0,100.0,0.5,0.02,0.25,"put")<0.0