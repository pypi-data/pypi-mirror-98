"""
Issue with VerticalLinear1:
    The mean curve was not cut properly around a value of the arithmetic target point.

Cause:
    The second value of the extrapolated end mean curve is nearest to the targetvalue
    when searched with *_find_positions_in_between*. But the target value is not
    in between its neighbors. The first half of *_find_positions_in_between*
    lead to wrong positions. Therefore the second half of this method.

Solution:
    Edited *_find_positions_in_between*

>>> from doctestprinter import print_pandas
>>> from arithmeticmeancurve import ArithmeticMeanCurve
>>> import examplecurves
>>> a_mean_curve = examplecurves.Static.create("VerticalLinear1")
>>> a_mean_curve = ArithmeticMeanCurve(a_mean_curve)

Test a running calculation.

>>> a_mean_curve.calculate()

Show the results.
>>> print_pandas(a_mean_curve.statistics.stats, formats="{:>}#{:>.4f}")
       end_x    end_y   min_x   min_y   max_x    max_y  start_x  start_y
mean  1.0150  10.1471  0.0000  0.0000  1.0150  10.1471   0.0000   0.0000
 std  0.0125   0.2252  0.0000  0.0000  0.0125   0.2252   0.0000   0.0000
>>> print_pandas(a_mean_curve.mean_curve, formats="{:>.4f}")
x
0.0000   0.0000
0.2495   2.4950
0.2536   2.5355
0.2536   2.5359
0.2536   2.5360
0.2584   2.5832
0.4991   4.9900
0.5072   5.0710
0.5073   5.0718
0.5073   5.0720
0.5167   5.1663
0.7486   7.4850
0.7608   7.6065
0.7609   7.6078
0.7609   7.6079
0.7751   7.7495
0.9981   9.9800
1.0145  10.1418
1.0145  10.1415
1.0150  10.1419
1.0155  10.1471

"""
import copy

import examplecurves
import pandas

from arithmeticmeancurve import (
    ArithmeticMeanCurve,
    _prepare_end_cap_for_extrapolation,
    _extrapolate_until_targets_are_included,
    _calculate_cutting_index_for_value,
    FrozenStdExtrapolation,
    _calculate_mean_and_std_curve,
)


_current_test_curves = examplecurves.Static.create("verticallinear1")


def test_find_cutting_index():
    """
    Debug incorrect cutting index calculation.

    >>> from arithmeticmeancurve import _find_positions_in_between
    >>> import examplecurves
    >>> from doctestprinter import print_pandas
    >>> end_mean_curve, target_end_y_value = test_find_cutting_index()
    >>> round(target_end_y_value, 6)
    10.147148
    >>> print_pandas(end_mean_curve, formats="{:>.4f}")
    x
    0.9981   9.9800
    1.0144  10.1420
    1.0145  10.1418
    1.0145  10.1415
    1.0150  10.1419
    1.0334  10.3160
    >>> _find_positions_in_between(
    ...     source_series=end_mean_curve, search_value=target_end_y_value,
    ... )
    (4, 5)
    >>> index_for_target_y = _calculate_cutting_index_for_value(
    ...     series_to_cut=end_mean_curve,
    ...     cutting_y_value=target_end_y_value,
    ... )
    >>> round(index_for_target_y, 6)
    1.015547
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
        [last_full_value_row, extrapolated_end_cap]
    )
    current_end_mean_curve = extended_extrapolated_end_cap.mean(axis=1)
    return current_end_mean_curve, target_end_y_value


def test_find_cutting_index_2():
    """
    Debug incorrect cutting index calculation if FrozenStdExtrapolation is
    run with use_previous_iteration=False.

    >>> from arithmeticmeancurve import _find_positions_in_between
    >>> import examplecurves
    >>> from doctestprinter import print_pandas
    >>> end_mean_curve, target_end_y_value = test_find_cutting_index_2()
    >>> round(target_end_y_value, 6)
    10.147148
    >>> print_pandas(end_mean_curve, formats="{:>.4f}")
    x
    0.9981   9.9800
    1.0144  10.1423
    1.0145  10.1414
    1.0145  10.1401
    1.0150  10.1391
    1.0334  10.3167
    >>> _find_positions_in_between(
    ...     source_series=end_mean_curve, search_value=target_end_y_value,
    ... )
    (4, 5)
    >>> index_for_target_y = _calculate_cutting_index_for_value(
    ...     series_to_cut=end_mean_curve,
    ...     cutting_y_value=target_end_y_value,
    ... )
    >>> round(index_for_target_y, 6)
    1.015833
    """
    sample_curves = copy.copy(_current_test_curves)
    extrapolates = FrozenStdExtrapolation(
        use_previous_iteration=False, target_threshold=0.0001
    )
    a_mean_curve = ArithmeticMeanCurve(sample_curves, method=extrapolates)
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
        [last_full_value_row, extrapolated_end_cap]
    )
    current_end_mean_curve = extended_extrapolated_end_cap.mean(axis=1)
    return current_end_mean_curve, target_end_y_value


def test_calculate_cutting_index_for_value():
    """
    _calculate_cutting_index_for_value leads to a wrong cutting index,
    if FrozenStdExtrapolation is run with use_previous_iteration=False.

    >>> from arithmeticmeancurve import _find_positions_in_between
    >>> import examplecurves
    >>> from doctestprinter import doctest_print
    >>> indexes, values, target_end_y_value = test_calculate_cutting_index_for_value()
    >>> target_end_y_value
    10.147148237071187
    >>> indexes
    [0.99814, 1.01435, 1.01452, 1.01454, 1.015, 1.03342]
    >>> values
    [9.97995, 10.1423, 10.14135, 10.14009, 10.13908, 10.31668]
    >>> from pandas import Series
    >>> sample_series = Series(values, index=indexes)
    >>> sample_search_value = target_end_y_value
    >>> _find_positions_in_between(sample_series, sample_search_value)
    (4, 5)
    """
    end_mean_curve, target_end_y_value = test_find_cutting_index_2()
    indexes = [round(x_i, 5) for x_i in end_mean_curve.index]
    return indexes, end_mean_curve.round(5).to_list(), target_end_y_value


def test_do_not_use_previous_iteration_mean_curve():
    """
    >>> import examplecurves
    >>> from doctestprinter import print_pandas
    >>> mean_curve, std_curve = test_do_not_use_previous_iteration_mean_curve()
    >>> print_pandas(mean_curve, formats="{:>.4f}" )
    x
    0.0000   0.0000
    0.2495   2.4950
    0.2536   2.5355
    0.2536   2.5359
    0.2536   2.5360
    0.2584   2.5832
    0.4991   4.9900
    0.5072   5.0710
    0.5073   5.0718
    0.5073   5.0720
    0.5167   5.1663
    0.7486   7.4850
    0.7608   7.6065
    0.7609   7.6078
    0.7609   7.6079
    0.7751   7.7495
    0.9981   9.9800
    1.0145  10.1414
    1.0145  10.1401
    1.0150  10.1391
    1.0158  10.1471
    """
    sample_curves = copy.copy(_current_test_curves)
    extrapolates = FrozenStdExtrapolation(
        use_previous_iteration=False, target_threshold=0.0001
    )
    a_mean_curve = ArithmeticMeanCurve(sample_curves, method=extrapolates)
    return _calculate_mean_and_std_curve(a_mean_curve)