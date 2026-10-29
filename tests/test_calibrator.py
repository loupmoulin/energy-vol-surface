import numpy as np
from vol_surface.sabr import sabr_vol
from vol_surface.calibrator import calibrate_sabr_slice

def test_sabr_calibration_recovery():
    F,T,beta=100.0,0.5,0.7
    true_alpha,true_rho,true_nu=0.28,-0.25,0.45
    strikes=np.linspace(70.0,130.0,13)
    synth_vols=np.array([sabr_vol(F,K,T,true_alpha,beta,true_rho,true_nu) for K in strikes])
    fit=calibrate_sabr_slice(F,strikes,synth_vols,T,beta=beta)
    assert fit.rmse<1e-4
    assert np.isclose(fit.alpha,true_alpha,atol=2e-2)
    assert np.isclose(fit.rho,true_rho,atol=5e-2)
    assert np.isclose(fit.nu,true_nu,atol=5e-2)