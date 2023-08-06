import examplecurves
from arithmeticmeancurve import ArithmeticMeanCurve, MeanCurvePlotter

sample_curves = examplecurves.Static.create(
    family_name="nonlinear0", predefined_offset=1
)
a_mean_curve = ArithmeticMeanCurve(sample_curves)

import matplotlib.pyplot as plt
# Setup figure
fig = plt.figure(figsize=(10, 5), dpi=96)
gspec = fig.add_gridspec(1, 1)

upper_axis = fig.add_subplot(gspec[:, :])
MeanCurvePlotter.plot_default(axis=upper_axis, a_mean_curve=a_mean_curve)

# Finishing touch
plt.tight_layout()
plt.legend()
plt.show()