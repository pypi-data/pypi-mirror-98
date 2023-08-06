"""
Issue with VerticalLinear0:
    The mean curve was not cut properly around a value of the arithmetic target point.

Cause:
    Y target value (y end mean) was outside the end cap. It is located in between the
    middle value block section and the end cap.

Solution(s):
    - The is_meet code of the break condition class was hardened.
    - The last middle block value line is concatenated to the extrapolated end cap to
      catch target values in between both.

>>> from arithmeticmeancurve import ArithmeticMeanCurve
>>> import examplecurves
>>> sample_curves = examplecurves.Static.create("VerticalLinear0")
>>> a_mean_curve = ArithmeticMeanCurve(sample_curves)
>>> a_mean_curve.calculate()
"""
import copy

import examplecurves
import pandas

from arithmeticmeancurve import (
    ArithmeticMeanCurve,
    _prepare_end_cap_for_extrapolation,
    _extrapolate_until_targets_are_included,
    _calculate_cutting_index_for_value,
)

_current_test_curves = examplecurves.Static.create("VerticalLinear0")


def test_find_cutting_index():
    """
    >>> import examplecurves
    >>> from doctestprinter import print_pandas
    >>> sample_curves = examplecurves.Static.create("VerticalLinear0")
    >>> end_mean_curve, target_end_y_value = test_find_cutting_index()
    >>> print_pandas(end_mean_curve, formats="{:>.3f}")
    x
    0.907  8.896
    0.972  9.534
    >>> round(target_end_y_value, 6)
    9.532235
    >>> index_for_target_y = _calculate_cutting_index_for_value(
    ...     series_to_cut=end_mean_curve,
    ...     cutting_y_value=target_end_y_value,
    ... )
    >>> round(index_for_target_y, 6)
    0.972307
    """
    sample_curves = copy.copy(_current_test_curves)
    a_mean_curve = ArithmeticMeanCurve(sample_curves)
    target_end_x_value = a_mean_curve.statistics.end_x_mean
    target_end_y_value = a_mean_curve.statistics.end_y_mean

    a_mean_curve.prepare_extrapolation()
    prepared_end_cap = _prepare_end_cap_for_extrapolation(a_mean_curve=a_mean_curve)

    last_full_value_row = a_mean_curve.get_last_full_row()
    last_value_row_mean_value = last_full_value_row.mean(axis=1)
    starting_x_mean_value = last_value_row_mean_value.iloc[0]

    extrapolated_end_cap = _extrapolate_until_targets_are_included(
        extrapolates=a_mean_curve,
        end_cap=prepared_end_cap,
        target_x_mean_value=target_end_x_value,
        target_y_mean_value=target_end_y_value,
        starting_last_mean_value=starting_x_mean_value,
    )
    extended_extrapolated_end_cap = pandas.concat(
        [last_full_value_row, extrapolated_end_cap])
    current_end_mean_curve = extended_extrapolated_end_cap.mean(axis=1)
    return current_end_mean_curve, target_end_y_value