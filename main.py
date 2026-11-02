import sys
import webbrowser
from pathlib import Path

# Add src folder to search path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import numpy as np
from vol_surface import calibrate_sabr_slice
from vol_surface.sabr import sabr_vol
from vol_surface.visualization import plot_vol_surface_3d

# 1. Market data across multiple maturities
maturities = np.array([0.25, 0.5, 0.75, 1.0])
forwards = np.array([83.0, 82.5, 81.8, 81.0])
beta = 0.7

market_strikes = np.array([65.0, 70.0, 75.0, 80.0, 82.5, 85.0, 90.0, 95.0, 100.0])
market_vols = [
    np.array([0.41, 0.38, 0.35, 0.33, 0.32, 0.315, 0.31, 0.315, 0.325]),  # 3M
    np.array([0.38, 0.35, 0.33, 0.31, 0.305, 0.30, 0.295, 0.30, 0.31]),    # 6M
    np.array([0.36, 0.33, 0.31, 0.295, 0.29, 0.285, 0.28, 0.285, 0.295]),  # 9M
    np.array([0.34, 0.31, 0.29, 0.28, 0.275, 0.27, 0.268, 0.272, 0.28]),   # 12M
]

# 2. Calibrate SABR parameters for each slice
calibrated_params = []
for F, T, vols in zip(forwards, maturities, market_vols):
    params = calibrate_sabr_slice(F, market_strikes, vols, T, beta=beta)
    calibrated_params.append(params)
    print(f"Slice T={T:.2f}y calibrated (RMSE: {params.rmse:.5f})")

# 3. Build the evaluation mesh
strikes_grid = np.linspace(60.0, 105.0, 60)
vols_grid = np.zeros((len(maturities), len(strikes_grid)))

for i, (F, T, p) in enumerate(zip(forwards, maturities, calibrated_params)):
    for j, K in enumerate(strikes_grid):
        vols_grid[i, j] = sabr_vol(F, K, T, p.alpha, p.beta, p.rho, p.nu)

# 4. Render the 3D surface using plot_vol_surface_3d
fig = plot_vol_surface_3d(strikes_grid, maturities, vols_grid)

# 5. Export to HTML and open in your default browser
html_file = Path(__file__).resolve().parent / "surface.html"
fig.write_html(str(html_file))
print(f"Surface generated: {html_file}")
webbrowser.open(html_file.as_uri())
