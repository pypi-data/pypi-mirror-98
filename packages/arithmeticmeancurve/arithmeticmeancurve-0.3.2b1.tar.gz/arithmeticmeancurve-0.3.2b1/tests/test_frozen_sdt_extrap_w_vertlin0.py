"""
>>> import examplecurves
>>> from arithmeticmeancurve import ArithmeticMeanCurve, FrozenStdExtrapolation
>>> from doctestprinter import print_pandas
>>> a_mean_curve = examplecurves.Static.create("verticallinear0")
>>> sample_mean_curve = ArithmeticMeanCurve(a_mean_curve)
>>> print_pandas(sample_mean_curve.family_of_curves, formats="{:>.4}")
          y_0     y_1    y_2    y_3    y_4
x
0.0000  0.000   0.000  0.000  0.000  0.000
0.2267  2.292   2.256  2.281  2.215  2.076
0.2432  2.459   2.421  2.447  2.377  2.227
0.2435  2.462   2.424  2.450  2.380  2.230
0.2505  2.532   2.493  2.520  2.448  2.293
0.2516  2.543   2.503  2.531  2.458  2.303
0.4535  4.583   4.513  4.562  4.430  4.151
0.4865  4.917   4.841  4.894  4.753  4.454
0.4871  4.924   4.848  4.900  4.759  4.459
0.5010  5.065   4.986  5.041  4.895  4.587
0.5031  5.085   5.007  5.061  4.916  4.606
0.6802  6.875   6.769  6.843  6.646  6.227
0.7297  7.376   7.262  7.341  7.130  6.680
0.7306  7.385   7.271  7.350  7.139  6.689
0.7516  7.597   7.479  7.561  7.343  6.880
0.7547  7.628   7.510  7.592  7.373  6.909
0.9069  9.167   9.025  9.124  8.861  8.302
0.9730    nan   9.683  9.788  9.506  8.907
0.9742    nan   9.695  9.801    nan  8.918
1.0021    nan   9.973    nan    nan  9.174
1.0062    nan  10.014    nan    nan    nan
>>> sample_mean_curve.statistics
FamilyOfCurveStatistics
         end_x     end_y  min_x  min_y     max_x     max_y  start_x  start_y
mean  0.972476  9.532235    0.0    0.0  0.972476  9.532235      0.0      0.0
std   0.039746  0.376375    0.0    0.0  0.039746  0.376375      0.0      0.0
>>> extrapolates = FrozenStdExtrapolation()
>>> extrapolates.prepare_extrapolation(a_mean_curve=sample_mean_curve)
>>> extrapolates
FrozenStdExtrapolation
    Target standard deviation (std): 0.352041900152178
    Curve's relative std positions:
        [ 0.77005112  0.36806549  0.64719569 -0.09924049 -1.68607181]
<BLANKLINE>
"""
import examplecurves

from arithmeticmeancurve import (
    SetOfCurves,
    FrozenStdExtrapolation,
    convert_set_to_family_of_curves,
    FamilyOfCurveStatistics,
    _TargetValuesAreReachedCondition,
    ArithmeticMeanCurve,
)
from arithmeticmeancurve import ExtrapolationIterationTester as EIT
import copy


_current_curves = examplecurves.Static.create("verticallinear0")


def test_iterations():
    """
    >>> from doctestprinter import prepare_pandas, EditingItem, doctest_iter_print
    >>> import examplecurves
    >>> import pandas
    >>> from arithmeticmeancurve import FamilyOfCurveStatistics, convert_set_to_family_of_curves
    >>> iteration_records = test_iterations()
    >>> pandas.options.display.float_format = '{:.4f}'.format
    >>> edits_pandas = EditingItem(prepare_pandas, formats="{:<}{:>.2f}#{:>.4f}")
    >>> doctest_iter_print(iteration_records.to_frames(), edits_item=edits_pandas)
                           y_0     y_1     y_2     y_3     y_4
    sections
    start         0.97     nan  9.6779  9.7833  9.5015  8.9025
    extrapolated  0.97  9.8042     nan     nan     nan     nan
    iteration     0.97  9.1668  9.6779  9.7833  9.5015  8.9025
                  0.97  9.6775  9.6779  9.7833  9.5015  8.9025
                  0.97  9.7796  9.6779  9.7833  9.5015  8.9025
                  0.97  9.8001  9.6779  9.7833  9.5015  8.9025
                  0.97  9.8042  9.6779  9.7833  9.5015  8.9025

    """
    sample_curves = copy.copy(_current_curves)
    frozen_std_extrapolation = FrozenStdExtrapolation()
    iteration_records = EIT.record_iterations(
        set_of_curves=sample_curves, extrapolates=frozen_std_extrapolation
    )
    return iteration_records


def test_break_condition():
    """
    >>> import examplecurves
    >>> test_break_condition()
    [True]
    """
    sample_curves = copy.copy(_current_curves)
    sample_family = convert_set_to_family_of_curves(sample_curves)
    stats = FamilyOfCurveStatistics(family_of_curves=sample_family)

    a_mean_curve = ArithmeticMeanCurve(sample_curves)
    starting_end_mean_value = a_mean_curve.get_last_full_row().mean(axis=1).iloc[0]

    condition = _TargetValuesAreReachedCondition(
        stats.end_x_mean, stats.end_y_mean, starting_end_mean_value
    )

    frozen_std_extrapolation = FrozenStdExtrapolation()
    iteration_records = EIT.record_iterations(
        set_of_curves=sample_curves, extrapolates=frozen_std_extrapolation
    )
    extrapolation_results = iteration_records.get_extrapolation_result()
    condition_results = []
    for x_value, extrapolated_values in extrapolation_results.iterrows():
        condition_is_meet = condition.is_meet(x_value, extrapolated_values)
        condition_results.append(condition_is_meet)
    return condition_results