import examplecurves
from arithmeticmeancurve import FrozenStdExtrapolation, VisualIterationTester

sample_curves = examplecurves.Static.create(family_name="horizontallinear0")

# from arithmeticmeancurve import ArithmeticMeanCurve
#
# a_mean_curves =ArithmeticMeanCurve(sample_curves)
#
# import matplotlib.pyplot as plt
#
# plt.plot(a_mean_curves.family_of_curves, "-o")
# plt.ylim(bottom=9.4, top=10.1)
# plt.xlim(left=0.96, right=1.04)
# plt.plot(a_mean_curves.mean_curve, "-k")
# plt.legend()
# plt.show()


# print(a_mean_curves.mean_curve)

# VisualIterationTester.plot_extrapolation_test(
#     curves=sample_curves, extrapolates=FrozenStdExtrapolation(use_previous_iteration=False)
# )
