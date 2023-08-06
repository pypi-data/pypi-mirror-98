import numpy
import examplecurves
from arithmeticmeancurve import extract_end_points, ArithmeticMeanCurve

sample_curves = examplecurves.Static.create(
    family_name="nonlinear0", predefined_offset=1,
)
extrapolating_mean_curve = ArithmeticMeanCurve(curves=sample_curves)
end_points = extract_end_points(extrapolating_mean_curve.family_of_curves)
x_values, y_values = end_points[:, 0], end_points[:, 1]

import matplotlib.pyplot as plt

# Setup figure
fig = plt.figure(figsize=(9, 5), dpi=96)
gspec = fig.add_gridspec(1, 1)
axis = fig.add_subplot(gspec[0, 0])
axis.set_title("extrapolated arithmetic mean curve")

axis.plot(
    *extrapolating_mean_curve.std_bars.horizontal,
    "-|",
    markersize=20,
    label="Horizontal standard deviation",
)
axis.plot(
    *extrapolating_mean_curve.std_bars.vertical,
    "-_",
    markersize=20,
    label="Vertical standard deviation",
)
axis.plot(
    x_values,
    y_values,
    "ok",
    markersize=8,
    label="end points of family of curves",
)
axis.plot(extrapolating_mean_curve.std_circle, "--k", label="Standard deviation circle")
axis.plot(extrapolating_mean_curve.family_of_curves)
# Finishing touch
axis.set_xlim(0.9, 1.4)
axis.set_ylim(8.5, 12.0)

# Finishing touch
axis.legend()
plt.show()