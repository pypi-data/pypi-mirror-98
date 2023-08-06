from arithmeticmeancurve import MeanCurvePlotter, ArithmeticMeanCurve
import examplecurves

def test_MeanCurvePlotter_test_plot():
    sample_curves = examplecurves.Static.create("verticallinear0")
    MeanCurvePlotter._test_plot(sample_curves=sample_curves)
    MeanCurvePlotter._test_plot(sample_curves=sample_curves, lower_title="lower title", upper_title="upper title")


def test_MeanCurvePlotter_plot():
    sample_curves = examplecurves.Static.create("verticallinear0")
    sample_mean_curve = ArithmeticMeanCurve(sample_curves)
    MeanCurvePlotter._plot(a_mean_curve=sample_mean_curve)