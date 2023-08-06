import examplecurves
from arithmeticmeancurve import FrozenStdExtrapolation, VisualIterationTester

sample_curves = examplecurves.Static.create(family_name="horizontallinear3")

from arithmeticmeancurve import ArithmeticMeanCurve

a_mean_curves = ArithmeticMeanCurve(sample_curves)
# VisualIterationTester.plot_extrapolation_test(
#     curves=a_mean_curve,
#     extrapolates=FrozenStdExtrapolation(
#         use_previous_iteration=True, target_threshold=0.00001
#     ),
# )
# VisualIterationTester.plot_extrapolation_test(
#     curves=a_mean_curve,
#     extrapolates=FrozenStdExtrapolation(
#         use_previous_iteration=True, target_threshold=0.0001
#     ),
# )
