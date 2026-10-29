"""Interactive Plotly visualizations for volatility surfaces and smiles."""
import numpy as np
import plotly.graph_objects as go
from vol_surface.sabr import sabr_vol
from vol_surface.calibrator import SabrParams

def plot_sabr_slice(
    F: float,
    strikes: np.ndarray,
    market_vols: np.ndarray,
    params: SabrParams,
    T: float,
) -> go.Figure:
    """Plots market volatility quotes against the calibrated SABR smile."""
    k_min,k_max=float(np.min(strikes)),float(np.max(strikes))
    K_dense=np.linspace(k_min*0.95,k_max*1.05,100)
    fitted_vols=np.array([sabr_vol(F,k,T,params.alpha,params.beta,params.rho,params.nu) for k in K_dense])
    fig=go.Figure()
    fig.add_trace(go.Scatter(
        x=strikes,y=market_vols,mode="markers",name="Market Quotes",
        marker=dict(size=8,color="royalblue")
    ))
    fig.add_trace(go.Scatter(
        x=K_dense,y=fitted_vols,mode="lines",name=f"SABR Fit (T={T:.2f}y)",
        line=dict(color="firebrick",width=2)
    ))
    fig.update_layout(
        title=f"SABR Smile Fit (T={T:.2f}y, RMSE={params.rmse:.4f})",
        xaxis_title="Strike (K)",yaxis_title="Implied Volatility",
        template="plotly_white"
    )
    return fig

def plot_vol_surface_3d(
    strikes_grid: np.ndarray,
    maturities_grid: np.ndarray,
    vols_grid: np.ndarray,
) -> go.Figure:
    """Renders an interactive 3D SABR volatility surface."""
    fig=go.Figure(data=[go.Surface(
        x=strikes_grid,y=maturities_grid,z=vols_grid,
        colorscale="Viridis",colorbar=dict(title="Implied Vol")
    )])
    fig.update_layout(
        title="3D SABR Implied Volatility Surface",
        scene=dict(
            xaxis_title="Strike (K)",
            yaxis_title="Maturity (T)",
            zaxis_title="Implied Volatility"
        ),
        autosize=True,template="plotly_white"
    )
    return fig