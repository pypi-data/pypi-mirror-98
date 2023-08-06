import examplecurves
from arithmeticmeancurve import FrozenStdExtrapolation, VisualIterationTester

sample_curves = examplecurves.Static.create(family_name="verticallinear0")

VisualIterationTester.plot_extrapolation_test(
    curves=sample_curves, extrapolates=FrozenStdExtrapolation()
)
