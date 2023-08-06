import examplecurves
from arithmeticmeancurve import ArithmeticMeanCurve

sample_curves = examplecurves.Static.create(
   family_name="nonlinear0",
   predefined_offset=1,
)
a_mean_curve = ArithmeticMeanCurve(sample_curves)
mean_curve = a_mean_curve.mean_curve

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 5), dpi=96)
gspec = fig.add_gridspec(1, 3)
axis = fig.add_subplot(gspec[:, :2])
for index, curve in enumerate(sample_curves):
   current_label = "Sample curve {}".format(index)
   axis.plot(curve, marker="o", markersize=3, label=current_label)

axis.plot(
   a_mean_curve.mean_curve,
   "--ko",
   markersize=5,
   label="Arithmetic mean curve"
)

axis.legend(bbox_to_anchor=(1.05, 1.02), loc='upper left')
plt.show()