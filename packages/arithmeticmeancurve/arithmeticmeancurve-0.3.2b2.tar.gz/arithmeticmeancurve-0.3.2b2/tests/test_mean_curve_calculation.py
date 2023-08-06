import examplecurves
from arithmeticmeancurve import meld_set_of_curves_to_family
from arithmeticmeancurve import _calculate_mean_and_std_curve
from arithmeticmeancurve import ArithmeticMeanCurve


def test_mean_curve_calculation_without_end_cap():
    """
    >>> from doctestprinter import print_pandas
    >>> sample_mean, sample_std = test_mean_curve_calculation_without_end_cap()
    >>> print_pandas(sample_mean, formats="{:>.1f}#{:>.3f}")
    x
    0.0  0.000
    0.2  2.224
    0.2  2.386
    0.2  2.389
    0.3  2.457
    0.3  2.467
    0.5  4.448
    0.5  4.772
    0.5  4.778
    0.5  4.915
    0.5  4.935
    0.7  6.672
    0.7  7.158
    0.7  7.167
    0.8  7.372
    0.8  7.402
    0.9  8.896

    """
    sample_curves = examplecurves.Static.create("verticallinear0")
    sample_family = meld_set_of_curves_to_family(sample_curves)
    sample_family.interpolate(method="index", limit_area="inside", inplace=True)
    sample_family.dropna(inplace=True)

    a_mean_curve = ArithmeticMeanCurve(sample_family)
    mean_curve, mean_std = _calculate_mean_and_std_curve(a_mean_curve=a_mean_curve)
    return mean_curve, mean_std