__author__ = """David Scheliga"""
__email__ = "david.scheliga@gmx.de"
__version__ = "0.3.0b1"
__all__ = [
    "AMeanCurve",
    "ArithmeticMeanCurve",
    "calculate_std_circle",
    "extract_end_points",
    "Extrapolates",
    "convert_set_to_family_of_curves",
    "interpolate_family_of_curves",
    "FrozenStdExtrapolation",
    "meld_set_of_curves_to_family",
    "VisualIterationTester",
    "FamilyOfCurveStatistics",
]


import re
from abc import ABC, abstractmethod
from collections import namedtuple
from itertools import repeat
from typing import (
    Union,
    Iterable,
    List,
    Dict,
    Generator,
    Tuple,
    Optional,
    Callable,
    Iterator,
    Any,
    Mapping,
)

import matplotlib.pyplot as plt
import numpy
import pandas
from doctestprinter import prepare_pandas
from matplotlib import pyplot
from numpy import linalg
from pandas import DataFrame, Series, MultiIndex
from scipy import stats
from trashpanda import (
    cut_after,
    add_blank_rows,
    find_index_of_value_in_series,
    meld_along_columns,
)

Curves = Union[numpy.ndarray, DataFrame]
Curve = Union[numpy.ndarray, DataFrame]
AnArray = Union[numpy.ndarray, Iterable[Union[int, float]]]


SetOfCurves = List[DataFrame]
"""
A set of unique curves with separately x-values.
"""

RawFamilyOfCurves = DataFrame
"""
A family of unique curves with common x-values and only their original y-values.
"""

FamilyOfCurves = DataFrame
"""
A family of unique curves with common x-values and interpolated y-values. 
"""

ValidationResult = namedtuple("ValidationMessage", "correct error_message error_type")

_NON_MATCHING_COLUMN_COUNT_MESSAGE = (
    "Column-count of the provided curves doesn't match."
)
_NON_MONOTONIC_INCREASING_X = "x-values needs to be monotonic increasing."


DEFAULT_STD_CIRCLE_NAME = "std circle"

_MATCHES_NAME_WITH_NUMBER_POSTFIX = re.compile(r"(.*)(_[0-9]+)$")


def _get_column_basename(column_name: str) -> str:
    """
    Returns the basename of the column name removing trailing indexes
    indicated by the expression '_[0-9]+'

    Args:
        column_name(str):
            Column name with potential trailing indexes.

    Returns:
        str

    Examples:

        >>> # access to protected member for testing
        >>> # noinspection PyProtectedMember
        >>> from arithmeticmeancurve import _get_column_basename
        >>> _get_column_basename("column_1")
        'column'
        >>> _get_column_basename("column_12")
        'column'
        >>> _get_column_basename("column")
        'column'
        >>> _get_column_basename("column")
        'column'
        >>> _get_column_basename("a key_0")
        'a key'
        >>> _get_column_basename("a_0")
        'a'

    """
    matched_column_name = _MATCHES_NAME_WITH_NUMBER_POSTFIX.match(column_name)
    found_no_match_because_no_postfix = matched_column_name is None
    if found_no_match_because_no_postfix:
        return column_name
    return matched_column_name.group(1)


def _group_column_names_with_postfix_numbers(
    column_names_with_postfixes: List[str],
) -> Dict[str, List[str]]:
    """
    Sorts column names into groups.

    Args:
        column_names_with_postfixes(str):
            Column names which got a postfix by
            :func:`arithmeticmeancurve._number_column_name`.

    Returns:
        Dict[str, List[str]]:
            A mapping with the group base name as key and this groups column
            names.

    .. doctest::

        >>> # access to protected member for testing
        >>> # noinspection PyProtectedMember
        >>> from arithmeticmeancurve import _group_column_names_with_postfix_numbers
        >>> _group_column_names_with_postfix_numbers(
        ...     ["column_0", "z_0", "a key_0", "column_1", "z_1", "a key_1"]
        ... )
        {'column': ['column_0', 'column_1'], 'z': ['z_0', 'z_1'], 'a key': ['a key_0', 'a key_1']}
    """
    column_groups = {}
    for name_with_postfix in column_names_with_postfixes:
        base_name = _get_column_basename(name_with_postfix)
        if base_name not in column_groups:
            column_groups[base_name] = []
        column_groups[base_name].append(name_with_postfix)
    return column_groups


def _number_column_name(column_name: str, number: int) -> str:
    """
    Adds a postfix to a column.

    Args:
        column_name(st):
            Column name which gets the postfix.

        number(int):
            The number for the column.

    Returns:
        str
    """
    return "{}_{}".format(column_name, number)


def meld_set_of_curves_to_family(set_of_curves: SetOfCurves) -> RawFamilyOfCurves:
    """
    Merges a set into a family (of curves). Each curve within theresulting
    RawFamilyOfCurves will only contain its own y-values. All other values of
    the common x-values will be NaN.

    Args:
        set_of_curves(SetOfCurves):
            A set of unique curves, which doesn't share common x-values.

    Returns:
        RawFamilyOfCurves

    .. doctest::

        >>> from pathlib import Path
        >>> import pandas
        >>> import examplecurves
        >>> from doctestprinter import doctest_print
        >>> example_curves = examplecurves.Static.create(family_name="nonlinear0", cut_curves_at=3)
        >>> doctest_print(meld_set_of_curves_to_family(set_of_curves=example_curves))
                   y_0     y_1       y_2       y_3       y_4
        x
        0.000  0.00000  0.0000  0.000000  0.000000  0.000000
        0.090      NaN     NaN       NaN       NaN  1.796875
        0.096      NaN     NaN       NaN  1.796875       NaN
        0.100      NaN  1.5625       NaN       NaN       NaN
        0.111      NaN     NaN  1.607654       NaN       NaN
        0.115  1.40625     NaN       NaN       NaN       NaN
        0.180      NaN     NaN       NaN       NaN  3.450000
        0.192      NaN     NaN       NaN  3.450000       NaN
        0.200      NaN  3.0000       NaN       NaN       NaN
        0.222      NaN     NaN  3.085479       NaN       NaN
        0.230  2.70000     NaN       NaN       NaN       NaN
        >>> example_curves = examplecurves.Static.create(
        ...     family_name="nonlinear0",
        ...     cut_curves_at=3,
        ...     predefined_offset=1
        ... )
        >>> merged_family = meld_set_of_curves_to_family(set_of_curves=example_curves)
        >>> doctest_print(merged_family)
                   y_0     y_1       y_2       y_3       y_4
        x
        0.010      NaN     NaN       NaN  0.080000       NaN
        0.020      NaN     NaN       NaN       NaN  0.000000
        0.050      NaN     NaN  0.100000       NaN       NaN
        0.080  0.01000     NaN       NaN       NaN       NaN
        0.100      NaN  0.0500       NaN       NaN       NaN
        0.106      NaN     NaN       NaN  1.876875       NaN
        0.110      NaN     NaN       NaN       NaN  1.796875
        0.161      NaN     NaN  1.707654       NaN       NaN
        0.195  1.41625     NaN       NaN       NaN       NaN
        0.200      NaN  1.6125       NaN       NaN  3.450000
        0.202      NaN     NaN       NaN  3.530000       NaN
        0.272      NaN     NaN  3.185479       NaN       NaN
        0.300      NaN  3.0500       NaN       NaN       NaN
        0.310  2.71000     NaN       NaN       NaN       NaN

    """
    different_numbered_curves = []
    for index, curves in enumerate(set_of_curves):
        numbered_curves = curves.copy()
        numbered_curves.columns = [
            "{}_{}".format(column_name, index) for column_name in curves.columns
        ]
        different_numbered_curves.append(numbered_curves)

    first_left, second_right = different_numbered_curves[:2]
    all_in_one = meld_along_columns(
        first_left, second_right, copy_at_meld=False, keep="first"
    )
    for additional_curves in different_numbered_curves[2:]:
        all_in_one = meld_along_columns(
            all_in_one, additional_curves, copy_at_meld=False, keep="first"
        )

    return all_in_one


def interpolate_family_of_curves(
    raw_family_of_curves: RawFamilyOfCurves,
) -> FamilyOfCurves:
    """
    Perform default interpolation of a merged family of curves.

    Args:
        raw_family_of_curves(DataFrame):
            Family of curves containing NaN-Values.

    Returns:
        DataFrame

    Examples:

        >>> import examplecurves
        >>> from arithmeticmeancurve import (
        ...     meld_set_of_curves_to_family, interpolate_family_of_curves
        ... )
        >>> from doctestprinter import doctest_print
        >>> example_curves = examplecurves.Static.create(
        ...     family_name="nonlinear0",
        ...     cut_curves_at=3,
        ...     predefined_offset=1
        ... )
        >>> merged_family = meld_set_of_curves_to_family(set_of_curves=example_curves)
        >>> doctest_print(merged_family)
                   y_0     y_1       y_2       y_3       y_4
        x
        0.010      NaN     NaN       NaN  0.080000       NaN
        0.020      NaN     NaN       NaN       NaN  0.000000
        0.050      NaN     NaN  0.100000       NaN       NaN
        0.080  0.01000     NaN       NaN       NaN       NaN
        0.100      NaN  0.0500       NaN       NaN       NaN
        0.106      NaN     NaN       NaN  1.876875       NaN
        0.110      NaN     NaN       NaN       NaN  1.796875
        0.161      NaN     NaN  1.707654       NaN       NaN
        0.195  1.41625     NaN       NaN       NaN       NaN
        0.200      NaN  1.6125       NaN       NaN  3.450000
        0.202      NaN     NaN       NaN  3.530000       NaN
        0.272      NaN     NaN  3.185479       NaN       NaN
        0.300      NaN  3.0500       NaN       NaN       NaN
        0.310  2.71000     NaN       NaN       NaN       NaN
        >>> interpolated_family = interpolate_family_of_curves(
        ...     raw_family_of_curves=merged_family
        ... )
        >>> doctest_print(interpolated_family)
                    y_0       y_1       y_2       y_3       y_4
        x
        0.010       NaN       NaN       NaN  0.080000       NaN
        0.020       NaN       NaN       NaN  0.267174  0.000000
        0.050       NaN       NaN  0.100000  0.828698  0.598958
        0.080  0.010000       NaN  0.534501  1.390221  1.197917
        0.100  0.254565  0.050000  0.824168  1.764570  1.597222
        0.106  0.327935  0.143750  0.911069  1.876875  1.717014
        0.110  0.376848  0.206250  0.969002  1.945755  1.796875
        0.161  1.000489  1.003125  1.707654  2.823978  2.733646
        0.195  1.416250  1.534375  2.160321  3.409460  3.358160
        0.200  1.472500  1.612500  2.226890  3.495560  3.450000
        0.202  1.495000  1.641250  2.253517  3.530000       NaN
        0.272  2.282500  2.647500  3.185479       NaN       NaN
        0.300  2.597500  3.050000       NaN       NaN       NaN
        0.310  2.710000       NaN       NaN       NaN       NaN

    """
    return raw_family_of_curves.interpolate(method="index", limit_area="inside")


def convert_set_to_family_of_curves(set_of_curves: SetOfCurves) -> FamilyOfCurves:
    """
    Merges and interpolates a set into a family (of curves).

    Notes:
        The *family of curves* is the basis for a mean curve calculation.

    Args:
        set_of_curves(SetOfCurves):
            A set of unique curves, which doesn't share common x-values.

    Returns:
        DataFrame

    .. doctest::

        >>> import examplecurves
        >>> from arithmeticmeancurve import convert_set_to_family_of_curves
        >>> from doctestprinter import doctest_print
        >>> example_curves = examplecurves.Static.create(
        ...     family_name="nonlinear0",
        ...     cut_curves_at=3,
        ...     predefined_offset=1
        ... )
        >>> sample_family = convert_set_to_family_of_curves(example_curves)
        >>> doctest_print(sample_family)
                    y_0       y_1       y_2       y_3       y_4
        x
        0.010       NaN       NaN       NaN  0.080000       NaN
        0.020       NaN       NaN       NaN  0.267174  0.000000
        0.050       NaN       NaN  0.100000  0.828698  0.598958
        0.080  0.010000       NaN  0.534501  1.390221  1.197917
        0.100  0.254565  0.050000  0.824168  1.764570  1.597222
        0.106  0.327935  0.143750  0.911069  1.876875  1.717014
        0.110  0.376848  0.206250  0.969002  1.945755  1.796875
        0.161  1.000489  1.003125  1.707654  2.823978  2.733646
        0.195  1.416250  1.534375  2.160321  3.409460  3.358160
        0.200  1.472500  1.612500  2.226890  3.495560  3.450000
        0.202  1.495000  1.641250  2.253517  3.530000       NaN
        0.272  2.282500  2.647500  3.185479       NaN       NaN
        0.300  2.597500  3.050000       NaN       NaN       NaN
        0.310  2.710000       NaN       NaN       NaN       NaN


    """
    raw_family = meld_set_of_curves_to_family(set_of_curves=set_of_curves)
    return interpolate_family_of_curves(raw_family_of_curves=raw_family)


BlockSectionPositions = namedtuple(
    "BlockSectionPositions", "start_position end_position"
)


def _estimate_block_section_positions(
    curve_group_frame: DataFrame,
) -> BlockSectionPositions:
    """
    Estimates the positions of the middle value block.

    Returns:
        BlockSectionPositions

    .. doctest::

        >>> import examplecurves
        >>> # access to protected member for testing
        >>> # noinspection PyProtectedMember
        >>> from arithmeticmeancurve import (
        ...     _estimate_block_section_positions,
        ...     meld_set_of_curves_to_family
        ... )
        >>> sample_curves = examplecurves.Static.create(
        ...     family_name="nonlinear0",
        ...     curve_selection=[2, 3],
        ...     offsets=[0.11, 0.0]
        ... )
        >>> merged_curves = meld_set_of_curves_to_family(sample_curves)
        >>> group_frame = merged_curves.interpolate(method="index", limit_area="inside")
        >>> value_block_positions = _estimate_block_section_positions(group_frame)
        >>> value_block_positions
        BlockSectionPositions(start_position=2, end_position=18)

        Here is the resulting frame.

        >>> from doctestprinter import doctest_print
        >>> enumerated_frame = group_frame.copy()
        >>> enumerated_frame["number"] = list(range(len(enumerated_frame)))
        >>> doctest_print(enumerated_frame.iloc[:4])
                    y_0       y_1  number
        x
        0.000       NaN  0.000000       0
        0.096       NaN  1.796875       1
        0.110  0.000000  2.037956       2
        0.192  1.187636  3.450000       3
        >>> doctest_print(enumerated_frame.iloc[-4:])
                     y_0   y_1  number
        x
        0.960   8.986780  11.5      18
        0.998   9.226026   NaN      19
        1.109   9.795051   NaN      20
        1.220  10.234246   NaN      21

        Block slicing test.

        >>> value_block_start, value_block_end = value_block_positions
        >>> doctest_print(enumerated_frame.iloc[:value_block_start])
               y_0       y_1  number
        x
        0.000  NaN  0.000000       0
        0.096  NaN  1.796875       1
        >>> doctest_print(enumerated_frame.iloc[value_block_start:value_block_end+1])
                    y_0        y_1  number
        x
        0.110  0.000000   2.037956       2
        0.192  1.187636   3.450000       3
        0.221  1.607654   3.905957       4
        0.288  2.499674   4.959375       5
        0.332  3.085479   5.585286       6
        0.384  3.716973   6.325000       7
        0.443  4.433475   7.075944       8
        0.480  4.839531   7.546875       9
        0.554  5.651643   8.377930      10
        0.576  5.867350   8.625000      11
        0.665  6.739982   9.491243      12
        0.672  6.800429   9.559375      13
        0.768  7.629410  10.350000      14
        0.776  7.698492  10.403906      15
        0.864  8.355465  10.996875      16
        0.887  8.527174  11.117415      17
        0.960  8.986780  11.500000      18
        >>> doctest_print(enumerated_frame.iloc[value_block_end+1:])
                     y_0  y_1  number
        x
        0.998   9.226026  NaN      19
        1.109   9.795051  NaN      20
        1.220  10.234246  NaN      21

    """
    index_mask_of_middle_value_block = curve_group_frame.notna().all(axis=1)
    all_indexes = curve_group_frame.index.copy()
    all_indexes_count = len(all_indexes)
    numbered_indexes = Series(numpy.arange(all_indexes_count), index=all_indexes)

    indexes_of_mid_value_block = numbered_indexes.loc[index_mask_of_middle_value_block]
    integer_start_index_of_middle_value_block = indexes_of_mid_value_block.iloc[0]
    integer_end_index_of_middle_value_block = indexes_of_mid_value_block.iloc[-1]
    return BlockSectionPositions(
        start_position=integer_start_index_of_middle_value_block,
        end_position=integer_end_index_of_middle_value_block,
    )


class SectioningCurves(ABC):
    @abstractmethod
    def get_end_cap(self) -> DataFrame:
        """
        Returns the trailing section of the family of curves, at which the first
        Nan occurs.

        Returns:
            DataFrame
        """
        pass

    @abstractmethod
    def get_middle_value_block(self) -> DataFrame:
        pass

    @abstractmethod
    def get_last_full_row(self) -> DataFrame:
        pass


class AMeanCurve(SectioningCurves, ABC):
    @property
    @abstractmethod
    def statistics(self) -> "FamilyOfCurveStatistics":
        pass


class Extrapolates(Callable, ABC):
    @abstractmethod
    def prepare_extrapolation(self, a_mean_curve: AMeanCurve):
        """
        Prepares the extrapolation for the given mean curve.

        Args:
            a_mean_curve(AMeanCurve):
                A mean curve.

        """
        pass

    @property
    @abstractmethod
    def is_prepared(self) -> bool:
        """
        States if the instance is prepared for extrapolation.

        Returns:
            bool
        """
        pass  # pragma: no cover

    @abstractmethod
    def iter_extrapolate_row(
        self, values_at_x: Series
    ) -> Generator[Series, None, None]:
        """
        Extrapolates the y-values of all curves at an equal x-value.

        Yields:
            Series
        """
        pass  # pragma: no cover

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass  # pragma: no cover


class ExtrapolatingMeanCurve(Extrapolates):
    def __init__(self, method: Optional[Union[str, Extrapolates]] = None):
        if isinstance(method, Extrapolates):
            self._extrapolates = method
        elif method is None or isinstance(method, str):
            self._extrapolates = _get_extrapolation_method(method=method)
        else:
            raise TypeError(
                "Either provide an object that `Extrapolates` "
                "or the name of the extrapolating method. Got {} instead.".format(
                    type(method)
                )
            )

    @property
    def is_prepared(self) -> bool:
        return self._extrapolates.is_prepared

    def prepare_extrapolation(self, a_mean_curve: AMeanCurve):
        raise NotImplementedError(
            "This method should be overridden by a final implementation of AMeanCurve."
        )

    def iter_extrapolate_row(
        self, values_at_x: Series
    ) -> Generator[Series, None, None]:
        yield from self._extrapolates.iter_extrapolate_row(values_at_x=values_at_x)

    def __call__(self, *args, **kwargs):
        return self._extrapolates(*args, **kwargs)


FROZEN_STD_EXTRAPOLATION_STRING_TEMPLATE = """{class_name}
    Target standard deviation (std): {target_std}
    Curve's relative std positions:
        {relative_std_positions}
"""


def _extract_end_points_of_family(family_of_curves: FamilyOfCurves) -> numpy.ndarray:
    """
    Extracts the end points of a family of curves.

    Args:
        family_of_curves(DataFrame):
            A dataframe containing a family of curves.

    Returns:
        numpy.ndarray

    .. doctest::

        >>> import examplecurves
        >>> from doctestprinter import print_pandas
        >>> # access to protected member for testing
        >>> # noinspection PyProtectedMember
        >>> from arithmeticmeancurve import (
        ...     convert_set_to_family_of_curves, _extract_end_points_of_family
        ... )
        >>> example_curves = examplecurves.Static.create(
        ...     family_name="nonlinear0",
        ...     predefined_offset=1
        ... )
        >>> sample_family = convert_set_to_family_of_curves(example_curves)
        >>> print_pandas(sample_family.loc[0.9:], formats="{:>.3f}")
                 y_0     y_1     y_2     y_3     y_4
        x
        0.900  7.572   9.050   9.087  11.213  11.388
        0.920  7.680   9.163   9.213  11.318  11.500
        0.938  7.776   9.264   9.326  11.412     nan
        0.970  7.949   9.444   9.490  11.580     nan
        1.000  8.110   9.613   9.644     nan     nan
        1.000  8.110   9.613   9.644     nan     nan
        1.049  8.326   9.827   9.895     nan     nan
        1.100  8.550  10.050  10.097     nan     nan
        1.115  8.616     nan  10.156     nan     nan
        1.160  8.770     nan  10.334     nan     nan
        1.230  9.010     nan     nan     nan     nan
        >>> _extract_end_points_of_family(sample_family)
        array([[ 1.23      ,  9.01      ],
               [ 1.1       , 10.05      ],
               [ 1.16      , 10.33424587],
               [ 0.97      , 11.58      ],
               [ 0.92      , 11.5       ]])


    """
    end_points_of_curves = []

    for label, curve in family_of_curves.iteritems():
        value_indexes = curve.index[curve.isna() == False]
        value_curve = curve.loc[value_indexes]
        last_value_of_curve = value_curve.iloc[-1]
        last_x_value_of_curve = value_curve.index[-1]

        end_points_of_curves.append([last_x_value_of_curve, last_value_of_curve])
    return numpy.array(end_points_of_curves)


def _extract_end_points_of_set(set_of_curves: SetOfCurves) -> numpy.ndarray:
    """
    Extracts the end points of a set of curves.

    Args:
        set_of_curves(SetOfCurves):
            A sequence of DataFrames representing a family of curves.

    Returns:
        numpy.ndarray

    .. doctest::

        >>> import examplecurves
        >>> from doctestprinter import doctest_iter_print, prepare_pandas
        >>> # access to protected member for testing
        >>> # noinspection PyProtectedMember
        >>> from arithmeticmeancurve import (
        ...     convert_set_to_family_of_curves, _extract_end_points_of_set
        ... )
        >>> example_curves = examplecurves.Static.create(
        ...     family_name="nonlinear0",
        ...     predefined_offset=1
        ... )
        >>> def cut_prepare(frame):
        ...     return prepare_pandas(frame.iloc[-3:], formats="{:>5.2f}")
        >>> doctest_iter_print(example_curves, edits_item=cut_prepare)
                   y
        x
         1.00   8.11
         1.11   8.62
         1.23   9.01
                   y
        x
         0.90   9.05
         1.00   9.61
         1.10  10.05
                   y
        x
         0.94   9.33
         1.05   9.90
         1.16  10.33
                   y
        x
         0.78  10.43
         0.87  11.08
         0.97  11.58
                   y
        x
         0.74  10.35
         0.83  11.00
         0.92  11.50
        >>> _extract_end_points_of_set(example_curves)
        array([[ 1.23      ,  9.01      ],
               [ 1.1       , 10.05      ],
               [ 1.16      , 10.33424587],
               [ 0.97      , 11.58      ],
               [ 0.92      , 11.5       ]])


    """
    end_points_of_curves = []

    for curve in set_of_curves:
        value_indexes = curve.notna()
        value_curve = curve[value_indexes]
        last_value_of_curve = value_curve.iloc[-1][0]
        last_x_value_of_curve = value_curve.index[-1]

        end_points_of_curves.append([last_x_value_of_curve, last_value_of_curve])
    return numpy.array(end_points_of_curves)


def extract_end_points(
    set_or_family: Union[SetOfCurves, FamilyOfCurves]
) -> numpy.ndarray:
    """
    Extracts end point of either a set of curves of family of curves

    Args:
        set_or_family(Union[SetOfCurves, FamilyOfCurves]):
            The set of family of curves from which the end point should be retrieved.

    Returns:
        numpy.ndarray

    Examples:

        >>> # access to protected member for testing
        >>> # noinspection PyProtectedMember
        >>> import examplecurves
        >>> from doctestprinter import doctest_print
        >>> from arithmeticmeancurve import (
        ...     convert_set_to_family_of_curves, extract_end_points
        ... )
        >>> example_curves = examplecurves.Static.create(
        ...     family_name="nonlinear0",
        ...     predefined_offset=1
        ... )
        >>> sample_family = convert_set_to_family_of_curves(example_curves)
        >>> end_points = extract_end_points(example_curves)
        >>> doctest_print(end_points)
        [[ 1.23        9.01      ]
         [ 1.1        10.05      ]
         [ 1.16       10.33424587]
         [ 0.97       11.58      ]
         [ 0.92       11.5       ]]
        >>> end_points = extract_end_points(sample_family)
        >>> doctest_print(end_points)
        [[ 1.23        9.01      ]
         [ 1.1        10.05      ]
         [ 1.16       10.33424587]
         [ 0.97       11.58      ]
         [ 0.92       11.5       ]]
    """
    if isinstance(set_or_family, list):
        return _extract_end_points_of_set(set_of_curves=set_or_family)
    if isinstance(set_or_family, DataFrame):
        return _extract_end_points_of_family(family_of_curves=set_or_family)
    raise TypeError("{} is not supported.".format(type(set_or_family)))


class FrozenStdExtrapolation(Extrapolates):
    """
    >>> import examplecurves
    >>> from doctestprinter import print_pandas
    >>> from arithmeticmeancurve import ArithmeticMeanCurve, FrozenStdExtrapolation
    >>> sample_curves = examplecurves.Static.create(family_name="nonlinear0")
    >>> extrapolating_mean_curve = ArithmeticMeanCurve(sample_curves)
    >>> extrapolator = FrozenStdExtrapolation()
    >>> extrapolator.prepare_extrapolation(a_mean_curve=extrapolating_mean_curve)
    >>> extrapolator
    FrozenStdExtrapolation
        Target standard deviation (std): 1.443992337458438
        Curve's relative std positions:
            [-1.32494113 -0.23760247 -0.42801722  0.88639717  1.10416365]
    <BLANKLINE>
    >>> end_cap = extrapolating_mean_curve.get_end_cap()
    >>> print_pandas(end_cap, formats="{:>.3f}")
             y_0     y_1     y_2     y_3  y_4
    x
    0.920  8.100   9.650   9.390  11.290  nan
    0.960  8.276   9.825   9.595  11.500  nan
    0.999  8.448   9.996   9.795     nan  nan
    1.000  8.452  10.000   9.799     nan  nan
    1.035  8.606     nan   9.937     nan  nan
    1.110  8.863     nan  10.234     nan  nan
    1.150  9.000     nan     nan     nan  nan
    >>> # extrapolator is Callable
    >>> # noinspection PyTypeChecker
    >>> extrapolated_end_cap = end_cap.apply(extrapolator, axis=1)
    >>> print_pandas(extrapolated_end_cap, formats="{:>.3f}")
             y_0     y_1     y_2     y_3     y_4
    x
    0.920  8.100   9.650   9.390  11.290  11.600
    0.960  8.276   9.825   9.595  11.500  11.792
    0.999  8.448   9.996   9.795  11.650  11.965
    1.000  8.452  10.000   9.799  11.654  11.969
    1.035  8.606  10.193   9.937  11.816  12.130
    1.110  8.863  10.469  10.234  12.093  12.407
    1.150  9.000  10.566  10.291  12.189  12.503

    """

    MAXIMUM_ALLOWED_INTERPOLATIONS = 50
    TARGET_THRESHOLD = 0.0001

    def __init__(
        self,
        use_previous_iteration: bool = True,
        maximum_allowed_iterations: Optional[int] = None,
        target_threshold: Optional[float] = None,
    ):
        """
        Extrapolates with last standard deviation as target. The current default
        extrapolation method of the *ArithmeticMeanCurve*.

        Notes:
            By default the mean value curve is calculated until the
            relative deviation of the mean curve in regard of the previous
            iteration step's mean value is 0.01% (`figure 1`_). For more
            precise values the *target_threshold* can be lowered.

            For a faster calculation the previous row's result is used as
            the entry point for the next calculation. It can be disabled
            via the argument *use_previous_iteration*.

        Args:
            use_previous_iteration(bool):
                Default True; indicates if the results of the previous
                calculation are used as starting point within the next
                one.

            maximum_allowed_iterations(int):
                Default 50; maximum count of iterations of each row's
                extrapolation calculation.

            target_threshold(float):
                Default 0.0001 (or 0.01%); the relative deviation, which
                marks the iterations target. Lowering this value might
                need an increase of *maximum_allowed_iterations*.

        Examples:

            The default extrapolation is tweaked comparing `figure 1`_ with
            `figure 2`_.

            .. _figure 1:

            .. plot::

                from arithmeticmeancurve import VisualIterationTester as VIT
                import examplecurves
                from arithmeticmeancurve import FrozenStdExtrapolation
                sample_curves = examplecurves.Static.create(family_name="nonlinear0")

                VIT.plot_extrapolation_test(
                    curves=sample_curves, extrapolates=FrozenStdExtrapolation()
                )

            **Figure 1:** Extrapolation with default settings.
            Top diagram; iteration per extrapolated row (abscissa number).
            Bottom diagram; Original and extrapolated curves.

            .. _figure 2:

            .. plot::

                from arithmeticmeancurve import VisualIterationTester as VIT
                import examplecurves
                from arithmeticmeancurve import FrozenStdExtrapolation
                sample_curves = examplecurves.Static.create(family_name="nonlinear0")

                VIT.plot_extrapolation_test(
                    curves=sample_curves,
                    extrapolates=FrozenStdExtrapolation(use_previous_iteration=False)
                )

            **Figure 2:** Extrapolation with *use_previous_iteration* turned off.
            Top diagram; iteration per extrapolated row (abscissa number).
            Bottom diagram; Original and extrapolated curves.

        """
        self._use_last_mean_value = use_previous_iteration
        self._relative_std_positions = None
        self._target_extrapolation = None
        self._target_extrapolation_std = None
        self._maximum_allowed_interpolations = None
        self._target_threshold = None
        self._is_prepared: bool = False

        if maximum_allowed_iterations is None:
            maximum_allowed_iterations = self.MAXIMUM_ALLOWED_INTERPOLATIONS
        if target_threshold is None:
            target_threshold = self.TARGET_THRESHOLD
        self._init_arguments(
            maximum_allowed_iterations=maximum_allowed_iterations,
            target_threshold=target_threshold,
        )
        self._previous_iterations_mean_value = None

    def _init_arguments(self, maximum_allowed_iterations: int, target_threshold: float):
        try:
            maximum_allowed_iterations = int(maximum_allowed_iterations)
        except TypeError:
            raise TypeError(
                "maximum_allowed_interpolations is expected to be an integer."
            )
        if maximum_allowed_iterations < 1:
            raise ValueError("maximum_allowed_interpolations must be greater than 0")
        self._maximum_allowed_interpolations = maximum_allowed_iterations

        try:
            target_threshold = float(target_threshold)
        except TypeError:
            raise TypeError("target_threshold is expected to be a float.")
        self._target_threshold = target_threshold

    def __repr__(self):
        return FROZEN_STD_EXTRAPOLATION_STRING_TEMPLATE.format(
            class_name=self.__class__.__name__,
            target_std=self._target_extrapolation_std,
            relative_std_positions=self._relative_std_positions,
        )

    @property
    def is_prepared(self) -> bool:
        return self._is_prepared

    def prepare_extrapolation(self, a_mean_curve: SectioningCurves):
        last_value_row = a_mean_curve.get_last_full_row().iloc[0]
        last_middle_block_mean = last_value_row.mean()
        target_extrapolation_std = last_value_row.std()

        relative_std_positions = last_value_row.copy()
        relative_std_positions -= last_middle_block_mean
        relative_std_positions /= target_extrapolation_std

        self._relative_std_positions = relative_std_positions.to_numpy()
        self._target_extrapolation_std = target_extrapolation_std
        self._previous_iterations_mean_value = last_middle_block_mean
        self._is_prepared = True
        assert (
            self._relative_std_positions is not None
        ), "The 'relative_std_positions' cannot be None after preparation."

    def iter_extrapolate_row(
        self, values_at_x: Series
    ) -> Generator[Series, None, None]:
        """

        Args:
            values_at_x:

        Returns:

        .. doctest:

            >>> import examplecurves
            >>> from doctestprinter import doctest_print
            >>> from arithmeticmeancurve import (
            ...     ArithmeticMeanCurve, FrozenStdExtrapolation
            ... )
            >>> sample_curves = examplecurves.Static.create(family_name="nonlinear0")
            >>> extrapolating_mean_curve = ArithmeticMeanCurve(sample_curves)
            >>> extrapolator = FrozenStdExtrapolation()
            >>> extrapolator.prepare_extrapolation(a_mean_curve=extrapolating_mean_curve)
            >>> sample_values = extrapolating_mean_curve.get_end_cap().iloc[-3]
            >>> for iteration_index, values in enumerate(
            ...     extrapolator.iter_extrapolate_row(sample_values)
            ... ):
            ...     print(iteration_index, values.to_numpy())
            0 [ 8.60625     9.5625      9.93749225 11.18554688 11.5       ]
            1 [ 8.60625     9.81526168  9.93749225 11.43830855 11.75276168]
            2 [ 8.60625     9.96691868  9.93749225 11.58996556 11.90441868]
            3 [ 8.60625    10.05791289  9.93749225 11.68095976 11.99541289]
            4 [ 8.60625    10.11250941  9.93749225 11.73555628 12.05000941]
            5 [ 8.60625    10.14526732  9.93749225 11.7683142  12.08276732]
            6 [ 8.60625    10.16492207  9.93749225 11.78796895 12.10242207]
            7 [ 8.60625    10.17671492  9.93749225 11.79976179 12.11421492]
            8 [ 8.60625    10.18379063  9.93749225 11.8068375  12.12129063]
            9 [ 8.60625    10.18803605  9.93749225 11.81108293 12.12553605]
            10 [ 8.60625    10.19058331  9.93749225 11.81363018 12.12808331]
            11 [ 8.60625    10.19211166  9.93749225 11.81515854 12.12961166]

        """
        assert (
            not values_at_x.empty
        ), "An empty slice was given. Nothing to extrapolate."
        extrapolate_mask = values_at_x.isna()
        current_values = values_at_x

        if self._use_last_mean_value:
            last_mean_value = self._previous_iterations_mean_value
        else:
            last_mean_value = numpy.nanmean(current_values)

        for iteration in range(self._maximum_allowed_interpolations):
            extrapolated_values = (
                self._relative_std_positions[extrapolate_mask]
                * self._target_extrapolation_std
            )
            extrapolated_values += last_mean_value
            current_values = current_values.copy()
            current_values.loc[extrapolate_mask] = extrapolated_values
            iteration_mean_value = numpy.nanmean(current_values)

            mean_diff = abs(last_mean_value - iteration_mean_value) / last_mean_value
            if float(mean_diff) < self._target_threshold:
                yield current_values
                self._previous_iterations_mean_value = last_mean_value
                return None

            last_mean_value = iteration_mean_value
            yield current_values

    def __call__(self, current_values: Series, *args, **kwargs):
        assert (
            self._is_prepared and self._relative_std_positions is not None
        ), "A prepared extrapolation cannot have None 'self._relative_std_positions'."
        extrapolated_values = current_values
        for current_result in self.iter_extrapolate_row(values_at_x=current_values):
            extrapolated_values = current_result
        return extrapolated_values


def _calculate_nominal_circular_arc_points(
    start_angle_in_rad: float, end_angle_in_rad: float, number_of_points: int
) -> numpy.ndarray:
    """
    Calculates point of a nominal circular arc.

    Args:
        start_angle_in_rad(float):
            Start angle at which the arcs begins.

        end_angle_in_rad:
            End angle at which the arcs ends.

        number_of_points:
            Number of calculated point of the nominal arc.

    Returns:
            numpy.ndarray

    .. doctest::

        >>> # access to protected member for testing
        >>> # noinspection PyProtectedMember
        >>> from arithmeticmeancurve import _calculate_nominal_circular_arc_points
        >>> import numpy
        >>> points = _calculate_nominal_circular_arc_points(
        ...     start_angle_in_rad=0.0,
        ...     end_angle_in_rad=2.0*numpy.pi,
        ...     number_of_points=9
        ... )
        >>> numpy.round(points, 3)
        array([[ 1.   ,  0.   ],
               [ 0.707,  0.707],
               [ 0.   ,  1.   ],
               [-0.707,  0.707],
               [-1.   ,  0.   ],
               [-0.707, -0.707],
               [-0.   , -1.   ],
               [ 0.707, -0.707],
               [ 1.   , -0.   ]])

    """
    full_circle_angles = numpy.linspace(
        start_angle_in_rad, end_angle_in_rad, num=number_of_points
    )

    x_point_values = numpy.cos(full_circle_angles)
    y_point_values = numpy.sin(full_circle_angles)
    return numpy.stack([x_point_values, y_point_values], axis=1)


def _calculate_end_point_mean_std(end_points: numpy.ndarray) -> dict:
    """
    Calculates the mean and standard deviation of points returning keyword
    arguments.

    Args:
        end_points(numpy.ndarray):
            The end point of a set or family of curves.

    Returns:
        dict

    .. doctest::

        >>> from arithmeticmeancurve import extract_end_points
        >>> import examplecurves
        >>> from doctestprinter import doctest_iter_print
        >>> sample_curves = examplecurves.Static.create(
        ...     family_name="nonlinear0",
        ...     predefined_offset=1
        ... )
        >>> ending_points = extract_end_points(set_or_family=sample_curves)
        >>> doctest_iter_print(
        ...     _calculate_end_point_mean_std(end_points=ending_points),
        ...     edits_item=lambda x: round(x, 3)
        ... )
        x_mean:
          1.076
        x_std:
          0.116
        y_mean:
          10.495
        y_std:
          0.961
    """
    x_values = end_points[:, 0]
    y_values = end_points[:, 1]

    return {
        "x_mean": numpy.mean(x_values),
        "x_std": numpy.std(x_values),
        "y_mean": numpy.mean(y_values),
        "y_std": numpy.std(y_values),
    }


class StatisticsOfPoints(object):
    def __init__(self, points: numpy.ndarray):
        self._x_mean = numpy.mean(points[:, 0])
        self._y_mean = numpy.mean(points[:, 1])
        self._x_std = numpy.std(points[:, 0])
        self._y_std = numpy.std(points[:, 1])
        x, y = points[:, 0], points[:, 1]
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        self._slope = slope
        self._intercept = intercept
        self._r_value = r_value
        self._p_value = p_value
        self._std_err = std_err

    @property
    def x_mean(self):
        return self._x_mean

    @property
    def y_mean(self):
        return self._y_mean

    @property
    def x_std(self):
        return self._x_std

    @property
    def y_std(self):
        return self._y_std

    @property
    def slope(self):
        return self._slope


def _calculate_std_bars(
    points_statistics: StatisticsOfPoints,
) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """

    Returns:

    """
    x_mean = points_statistics.x_mean
    x_std = points_statistics.x_std
    y_mean = points_statistics.y_mean
    y_std = points_statistics.y_std

    horizontal_bar = [
        [x_mean - x_std, y_mean],
        [x_mean, y_mean],
        [x_mean + x_std, y_mean],
    ]
    vertical_bar = [
        [x_mean, y_mean - y_std],
        [x_mean, y_mean],
        [x_mean, y_mean + y_std],
    ]

    return (
        numpy.array(horizontal_bar),
        numpy.array(vertical_bar),
    )


def _calculate_std_circle(
    points_statistics: StatisticsOfPoints,
) -> numpy.ndarray:
    number_of_points = 32

    nominal_circle = _calculate_nominal_circular_arc_points(
        start_angle_in_rad=0.0,
        end_angle_in_rad=2.0 * numpy.pi,
        number_of_points=number_of_points,
    )

    nominal_circle = numpy.append(nominal_circle, [nominal_circle[0].copy()], axis=0)

    circle_x_midpoint = points_statistics.x_mean
    circle_y_midpoint = points_statistics.y_mean
    circle_width = points_statistics.x_std
    circle_height = points_statistics.y_std

    std_circle = nominal_circle * [circle_width, circle_height]
    std_circle += numpy.array([circle_x_midpoint, circle_y_midpoint])

    return std_circle


def shear_points_vertical(
    points: numpy.ndarray, slope: float, center_point: Optional[numpy.ndarray] = None
) -> numpy.ndarray:
    """

    Args:
        points:
        slope:
        center_point:

    Returns:
        >>> import numpy
        >>> sample_points = numpy.array([[1.0, 1.0], [2.0, 1.0]])
        >>> shear_points_vertical(sample_points, -0.5)
        array([[1. , 0.5],
               [2. , 0. ]])
        >>> shear_points_vertical(sample_points, 0.5)
        array([[1. , 1.5],
               [2. , 2. ]])
        >>> shear_points_vertical(sample_points, 0.5, numpy.array([1.0, 1.0]))
        array([[1. , 1. ],
               [2. , 1.5]])
        >>> shear_points_vertical(sample_points, -0.5, numpy.array([1.0, 1.0]))
        array([[1. , 1. ],
               [2. , 0.5]])
    """
    shear_around_center = center_point is not None
    if shear_around_center:
        points_at_center = points - center_point
    else:
        points_at_center = points

    shear_vector = numpy.array([[1, slope], [0, 1]])
    sheared_points = points_at_center.dot(shear_vector)

    if shear_around_center:
        sheared_points += center_point
    return sheared_points


def calculate_std_circle(family_of_curves: FamilyOfCurves) -> Series:
    """

    Args:
        family_of_curves:

    Returns:

    .. doctest::

        >>> import examplecurves
        >>> from doctestprinter import print_pandas
        >>> from arithmeticmeancurve import (
        ...     meld_set_of_curves_to_family, calculate_std_circle
        ... )
        >>> sample_curves = examplecurves.Static.create(family_name="nonlinear0")
        >>> sample_family = meld_set_of_curves_to_family(sample_curves)
        >>> print_pandas(
        ...     calculate_std_circle(sample_family).iloc[::4], formats="{:>.3f}"
        ... )
        x      std circle
        1.117       9.613
        1.088      10.565
        1.019      11.442
        0.953      11.701
        0.931      11.179
        0.967      10.202
        1.038       9.377
        1.100       9.218

    """
    number_of_points = 32

    nomimal_circle = _calculate_nominal_circular_arc_points(
        start_angle_in_rad=0.0,
        end_angle_in_rad=2.0 * numpy.pi,
        number_of_points=number_of_points,
    )

    end_points = extract_end_points(set_or_family=family_of_curves)
    slope, *items = stats.linregress(end_points[:, 0], end_points[:, 1])

    end_point_statistics = _calculate_end_point_mean_std(end_points=end_points)
    circle_x_midpoint = end_point_statistics["x_mean"]
    circle_y_midpoint = end_point_statistics["y_mean"]
    circle_width = end_point_statistics["x_std"]
    circle_height = end_point_statistics["y_std"]

    std_circle = nomimal_circle * [circle_width, circle_height]

    y_shearing = numpy.array([slope, 0])
    sheared_scatter_circle_y = std_circle.dot(y_shearing)

    x_translations = numpy.full(len(std_circle), circle_x_midpoint)
    y_translations = sheared_scatter_circle_y + circle_y_midpoint

    translation_to_end_position = numpy.stack([x_translations, y_translations], axis=1)
    scatter_circle = std_circle + translation_to_end_position

    circle_x_points = scatter_circle[:, 0]
    circle_y_points = scatter_circle[:, 1]

    x_column_name = family_of_curves.index.name
    std_circle = Series(
        circle_y_points,
        index=pandas.Index(circle_x_points, name=x_column_name),
        name=DEFAULT_STD_CIRCLE_NAME,
    )

    return std_circle


_DEFAULT_KEY = "default"
_EXTRAPOLATION_METHODS = {
    _DEFAULT_KEY: FrozenStdExtrapolation,
    "frozen_std": FrozenStdExtrapolation,
}


class Bar(object):
    def __init__(self, points: numpy.ndarray):
        self._points: numpy.ndarray = points

    @property
    def points(self):
        return self._points

    def __getitem__(self, item):
        return self._points[item]

    def __iter__(self):
        yield self._points[:, 0]
        yield self._points[:, 1]

    def __len__(self):
        return 2


class StdBars(object):
    def __init__(self, points_statistics: StatisticsOfPoints, do_shear: bool = False):
        self._mid_point: numpy.ndarray = numpy.full(2, 0.0)
        self._horizontal_std_bar: numpy.ndarray = numpy.full(2, 0.0)
        self._vertical_std_bar: numpy.ndarray = numpy.full(2, 0.0)
        self._do_shear = do_shear
        self._calculate(points_statistics)

    def _calculate(self, points_statistics: StatisticsOfPoints):
        horizontal_bar, vertical_bar = _calculate_std_bars(
            points_statistics=points_statistics
        )
        mid_point = numpy.array((points_statistics.x_mean, points_statistics.y_mean))
        slope = points_statistics.slope
        if self._do_shear:
            horizontal_bar = shear_points_vertical(horizontal_bar, slope, mid_point)
            vertical_bar = shear_points_vertical(vertical_bar, slope, mid_point)

        self._horizontal_std_bar = Bar(horizontal_bar)
        self._vertical_std_bar = Bar(vertical_bar)
        self._mid_point = mid_point

    @property
    def horizontal(self) -> numpy.ndarray:
        return self._horizontal_std_bar

    @property
    def vertical(self) -> numpy.ndarray:
        return self._vertical_std_bar


class StdCircle(Iterable):
    def __init__(
        self,
        points_statistics: StatisticsOfPoints,
        do_shear: bool = False,
        index_name: Optional[str] = None,
    ):
        self._point_statistics: StatisticsOfPoints = points_statistics
        self._mid_point: numpy.ndarray = numpy.array(
            points_statistics.x_mean, points_statistics.y_mean
        )
        self._do_shear = do_shear
        self._points: Optional[numpy.ndarray] = None
        self._std_bars: StdBars = StdBars(
            points_statistics=points_statistics, do_shear=do_shear
        )
        if index_name is None:
            self._index_name = "x"
        else:
            self._index_name = index_name
        self._calculate()

    def _calculate(self):
        self._points = _calculate_std_circle(points_statistics=self._point_statistics)
        if self._do_shear:
            self._points = shear_points_vertical(
                self._points, self._point_statistics.slope, self._mid_point
            )

    @property
    def std_bars(self):
        return self._std_bars

    def __getitem__(self, item):
        return self._points[item]

    def __len__(self):
        return 2

    def __iter__(self):
        yield self._points[:, 0]
        yield self._points[:, 1]

    def to_series(self):
        x_values, y_values = self._points[:, 0], self._points[:, 1]
        return Series(
            y_values,
            index=pandas.Index(x_values, name=self._index_name),
            name=DEFAULT_STD_CIRCLE_NAME,
        )


class FamilyOfCurveStatistics(object):
    def __init__(self, family_of_curves: FamilyOfCurves):
        self._stats = self.get_curves_statistics(family_of_curves)

    def __repr__(self):
        return "{}\n{}".format(self.__class__.__name__, self._stats)

    def __round__(self, digits):
        return self._stats.round(digits)

    @staticmethod
    def get_curves_statistics(family_of_curves: FamilyOfCurves) -> DataFrame:
        """
        Calculates the mean and standard deviation of a family of curves start,
        end, min and max points.

        Returns:
            DataFrame

        Examples:
            >>> import examplecurves
            >>> from arithmeticmeancurve import (
            ...     FamilyOfCurveStatistics,
            ...     convert_set_to_family_of_curves
            ... )
            >>> from doctestprinter import print_pandas
            >>> sample_curves = examplecurves.Static.create(
            ...     family_name="nonlinear0",
            ...     predefined_offset=1
            ... )
            >>> example_family = convert_set_to_family_of_curves(sample_curves)
            >>> get_statistics_of_curves = FamilyOfCurveStatistics.get_curves_statistics
            >>> curve_statistics = get_statistics_of_curves(example_family)
            >>> print_pandas(curve_statistics, formats="{:>}#{:>.3f}")
                  end_x   end_y  min_x  min_y  max_x   max_y  start_x  start_y
            mean  1.076  10.495  0.052  0.048  1.076  10.495    0.052    0.048
             std  0.129   1.074  0.038  0.043  0.129   1.074    0.038    0.043
            >>> curve_statistics.loc["mean", "end_x"]
            1.076

        """
        values_of_curves = []
        for label, curve in family_of_curves.iteritems():
            # PEP 8: E712 doesn't work with pandas.
            # noinspection PyPep8
            value_indexes = curve.index[curve.isna() == False]
            value_curve = curve.loc[value_indexes]
            last_value_of_curve = value_curve.iloc[-1]
            last_x_value_of_curve = value_curve.index[-1]
            first_x_value_of_curve = value_curve.index[0]
            first_value_of_curve = value_curve.iloc[0]
            curve_index_of_maximum = value_curve.idxmax()
            maximum_value_of_curve = value_curve.loc[curve_index_of_maximum]
            curve_index_of_minimum = value_curve.idxmin()
            minimum_value_of_curve = value_curve.loc[curve_index_of_minimum]

            values_of_curves.append(
                {
                    "end_x": last_x_value_of_curve,
                    "end_y": last_value_of_curve,
                    "min_x": curve_index_of_minimum,
                    "min_y": minimum_value_of_curve,
                    "max_x": curve_index_of_maximum,
                    "max_y": maximum_value_of_curve,
                    "start_x": first_x_value_of_curve,
                    "start_y": first_value_of_curve,
                }
            )
        group_sample = DataFrame(values_of_curves)
        test = {
            "mean": group_sample.mean().to_dict(),
            "std": group_sample.std().to_dict(),
        }
        return DataFrame(test).transpose()

    @property
    def stats(self):
        return self._stats

    @property
    def end_x_mean(self):
        return self._stats.loc["mean", "end_x"]

    @property
    def end_x_std(self):
        return self._stats.loc["std", "end_x"]

    @property
    def end_y_mean(self):
        return self._stats.loc["mean", "end_y"]

    @property
    def end_y_std(self):
        return self._stats.loc["std", "end_y"]


def _get_extrapolation_method(method: Optional[str] = None) -> Extrapolates:
    if method is None:
        method = _DEFAULT_KEY
    try:
        extrapolator_class = _EXTRAPOLATION_METHODS[method]
    except KeyError:
        known_methods = "', '".join(_EXTRAPOLATION_METHODS)
        raise ValueError(
            "'{}' is not a valid method. "
            "Pick one of '{}'.".format(method, known_methods)
        )
    return extrapolator_class()


def _search_upwards(
    source_series: Series, search_value: float, start_index: int
) -> Optional[Tuple[int, int]]:
    """
    Searches the target value

    Args:
        source_series(Series):
            The values in which the search value should be located.

        search_value(float):
            Search value which should be in between to values.


    Returns:
        Optional[Tuple[int, int]]


    .. doctest::

        The second value is next to the search value but with neighbors not
        in between. The first half of the code lead to wrong positions.
        The scond half beginning at line with *_target_is_in_between* checks
        for values being in between.

        >>> indexes = [0.6022, 0.8025, 0.8027, 1.0017, 1.202, 1.2023]
        >>> values = [9.049, 9.182, 9.183, 10.116, 10.35, 10.3504]
        >>> from pandas import Series
        >>> sample_series = Series(values, index=indexes)
        >>> sample_search_value = 9.7076
        >>> _search_upwards(sample_series, sample_search_value, 0)
        (2, 3)
        >>> _search_upwards(sample_series, sample_search_value, 2)
        (2, 3)

    """
    max_right_position = len(source_series) - 1
    for left_position in range(start_index, max_right_position):
        right_position = left_position + 1
        left_value = source_series.iloc[left_position]
        right_value = source_series.iloc[right_position]
        if _target_is_in_between(left_value, search_value, right_value):
            return left_position, right_position
    return None


def _search_downwards(
    source_series: Series, search_value: float, start_index: int
) -> Optional[Tuple[int, int]]:
    """
    Searches the target value

    Args:
        source_series(Series):
            The values in which the search value should be located.

        search_value(float):
            Search value which should be in between to values.


    Returns:
        Optional[Tuple[int, int]]

    .. doctest::

        The second value is next to the search value but with neighbors not
        in between. The first half of the code lead to wrong positions.
        The scond half beginning at line with *_target_is_in_between* checks
        for values being in between.

        >>> indexes = [0.6022, 0.8025, 0.8027, 1.0017, 1.202, 1.2023]
        >>> values = [9.049, 9.182, 9.183, 10.116, 10.35, 10.3504]
        >>> from pandas import Series
        >>> sample_series = Series(values, index=indexes)
        >>> sample_search_value = 9.7076
        >>> _search_downwards(sample_series, sample_search_value, 3)
        (2, 3)
        >>> _search_downwards(sample_series, sample_search_value, 2)

    """
    max_index = len(source_series) - 1
    max_right_position = max_index - 1
    for right_position in range(start_index, 0, -1):
        left_position = right_position - 1
        left_value = source_series.iloc[left_position]
        right_value = source_series.iloc[right_position]
        if _target_is_in_between(left_value, search_value, right_value):
            return left_position, right_position
    return None


def _find_positions_in_between(
    source_series: Series, search_value: float
) -> Optional[Tuple[int, int]]:
    """
    Finds two positions (integer indexes) for a *search value* within a
    sequence.

    Args:
        source_series(Series):
            The values in which the search value should be located.

        search_value(float):
            Search value which should be in between to values.

    Returns:
        Optional[Tuple[int, int]]

    Examples:

        >>> from pandas import Series, Index
        >>> from doctestprinter import print_pandas
        >>> sample_series = Series(
        ...     numpy.arange(3.0),
        ...     index=Index([0.1, 0.2, 0.3], name="x"),
        ...     name="y"
        ... )
        >>> print_pandas(sample_series)
        x    y
        0.1  0
        0.2  1
        0.3  2
        >>> _find_positions_in_between(sample_series, 0.0)
        (0, 1)
        >>> _find_positions_in_between(sample_series, 0.5)
        (0, 1)
        >>> _find_positions_in_between(sample_series, 1.0)
        (1, 2)
        >>> _find_positions_in_between(sample_series, 1.5)
        (1, 2)
        >>> _find_positions_in_between(sample_series, 2.0)
        (1, 2)
        >>> _find_positions_in_between(sample_series, 0.0)
        (0, 1)
        >>> _find_positions_in_between(sample_series, 0.5)
        (0, 1)
        >>> _find_positions_in_between(sample_series, 1.0)
        (1, 2)
        >>> _find_positions_in_between(sample_series, 1.5)
        (1, 2)
        >>> _find_positions_in_between(sample_series, 2.0)
        (1, 2)

        >>> str(_find_positions_in_between(Series(dtype=float), 2.0))
        'None'

    .. doctest::

        The second value is next to the search value but with neighbors not
        in between. The first half of the code lead to wrong positions.
        The scond half beginning at line with *_target_is_in_between* checks
        for values being in between.

        >>> indexes = [0.998143, 1.014351, 1.014519, 1.014543, 1.014996, 1.033422]
        >>> values = [9.979952, 10.142040, 10.141824, 10.141548, 10.141944, 10.315983]
        >>> from pandas import Series
        >>> sample_series = Series(values, index=indexes)
        >>> sample_search_value = 10.147148
        >>> _find_positions_in_between(sample_series, sample_search_value)
        (4, 5)

    .. doctest::

        The second value is next to the search value but with neighbors not
        in between. The first half of the code lead to wrong positions.
        The scond half beginning at line with *_target_is_in_between* checks
        for values being in between.

        >>> indexes = [0.6022, 0.8025, 0.8027, 1.0017, 1.202, 1.2023]
        >>> values = [9.049, 9.182, 9.183, 10.116, 10.35, 10.3504]
        >>> from pandas import Series
        >>> sample_series = Series(values, index=indexes)
        >>> sample_search_value = 9.7076
        >>> _find_positions_in_between(sample_series, sample_search_value)
        (2, 3)

    .. doctest::
        >>> indexes = [0.99814, 1.01435, 1.01452, 1.01454, 1.015, 1.03342]
        >>> values = [9.97995, 10.1423, 10.14135, 10.14009, 10.13908, 10.31668]
        >>> from pandas import Series
        >>> sample_series = Series(values, index=indexes)
        >>> sample_search_value = 10.1471482
        >>> _find_positions_in_between(sample_series, sample_search_value)
        (4, 5)

    """
    if source_series.empty:
        return None
    not_enough_values_for_search_between = len(source_series) < 2
    if not_enough_values_for_search_between:
        return None

    deltas_to_search_value = source_series.sub(search_value)
    absolute_deltas_to_search_value = deltas_to_search_value.abs()
    nearest_index_to_search_value = absolute_deltas_to_search_value.idxmin()
    left_position = source_series.index.get_loc(nearest_index_to_search_value)

    last_possible_position = len(source_series) - 1
    if left_position == last_possible_position:
        right_position = left_position
        left_position -= 1
    else:
        right_position = left_position + 1

    left_value = source_series.iloc[left_position]
    right_value = source_series.iloc[right_position]

    if _target_is_in_between(left_value, search_value, right_value):
        return left_position, right_position

    positions_of_left_selection = _search_downwards(
        source_series=source_series,
        search_value=search_value,
        start_index=right_position,
    )
    if positions_of_left_selection is not None:
        return positions_of_left_selection

    positions_of_right_selection = _search_upwards(
        source_series=source_series,
        search_value=search_value,
        start_index=left_position,
    )
    if positions_of_right_selection is not None:
        return positions_of_right_selection

    return None


def _calculate_cutting_index_for_value(
    series_to_cut: Series, cutting_y_value: float
) -> float:
    """
    Calculates the necessary index for cutting at a target y-value.

    Notes:
         Supports only float type indexes.

    Args:
        series_to_cut(Series):
            The sequence of values which should be cut.

        cutting_y_value(cutting values):
            The y-value for which x-index is searched.

    Returns:
        float

    Examples:

        >>> from pandas import Series, Index
        >>> from doctestprinter import print_pandas
        >>> sample_series = Series(
        ...     numpy.arange(3.0),
        ...     index=Index([0.1, 0.2, 0.3], name="x"),
        ...     name="y"
        ... )
        >>> print_pandas(sample_series)
        x    y
        0.1  0
        0.2  1
        0.3  2
        >>> _calculate_cutting_index_for_value(sample_series, 0.0)
        0.1
        >>> _calculate_cutting_index_for_value(sample_series, 0.4)
        0.14
        >>> _calculate_cutting_index_for_value(sample_series, 1.0)
        0.2

    """
    selection_section = series_to_cut
    direct_value_within_series = cutting_y_value in selection_section.values
    if direct_value_within_series:
        cutting_index = series_to_cut[series_to_cut == cutting_y_value].index.values
        first_occurred_index = cutting_index[0]
        return first_occurred_index

    positions = _find_positions_in_between(
        source_series=series_to_cut,
        search_value=cutting_y_value,
    )
    if positions is None:
        raise ValueError(
            "Could not find a valid y-value {} withing the target series '{}'. "
            "Either the value is not within the Series or the code is broken."
            "".format(cutting_y_value, series_to_cut.name)
        )
    left_position, right_position = positions

    left_x_value = series_to_cut.index[left_position]
    left_y_value = series_to_cut.iloc[left_position]
    right_x_value = series_to_cut.index[right_position]
    right_y_value = series_to_cut.iloc[right_position]
    x_as_y_values = numpy.array([left_x_value, right_x_value])
    y_as_x_values = numpy.array([left_y_value, right_y_value])
    target_index = numpy.interp([cutting_y_value], y_as_x_values, x_as_y_values)[0]
    return target_index


def _get_slope(x0: float, y0: float, x1: float, y1: float) -> float:
    """
    Gets the splope of 2 points.

    Args:
        x0(float):
            x-value of first point.

        y0(float):
            y-value of first point.

        x1(float):
            x-value of second point.

        y1(float):
            y-value of second point.

    Returns:
        float

    .. doctest::

        >>> _get_slope(0, 1, 0, 2)
        inf
        >>> _get_slope(0, 1, 0, 0)
        -inf
        >>> _get_slope(0, 0, 1, 1)
        1.0

    """
    dx = x1 - x0
    dy = y1 - y0
    try:
        return dy / dx
    except ZeroDivisionError:
        if dy < 0.0:
            return -numpy.inf
        return numpy.inf


def _target_is_in_between(left_value, mid_value, right_value):
    """

    Args:
        right_value:
        mid_value:
        left_value:

    Returns:

    .. doctest::

        >>> _target_is_in_between(2.0, 2.5, 3.0)
        True
        >>> _target_is_in_between(2.0, 2.0, 3.0)
        True
        >>> _target_is_in_between(2.0, 3.0, 3.0)
        True
        >>> _target_is_in_between(2.0, 1.0, 3.0)
        False
        >>> _target_is_in_between(2.0, 4.0, 3.0)
        False
        >>> _target_is_in_between(-2.0, -2.5, -3.0)
        True
        >>> _target_is_in_between(-2.0, -2.0, -3.0)
        True
        >>> _target_is_in_between(-2.0, -3.0, -3.0)
        True
        >>> _target_is_in_between(-2.0, -1.0, -3.0)
        False
        >>> _target_is_in_between(-2.0, -4.0, -3.0)
        False

        >>> _target_is_in_between(None, 2.5, 3.0)
        False
        >>> _target_is_in_between(2.0, 2.5, None)
        False
        >>> from numpy import NaN
        >>> _target_is_in_between(NaN, 2.5, 3.0)
        False
        >>> _target_is_in_between(2.0, 2.5, NaN)
        False
        >>> _target_is_in_between(2.0, 2.5, 2.0)
        False
    """
    if right_value is None or right_value is numpy.NaN:
        return False
    if left_value is None or left_value is numpy.NaN:
        return False
    slope = _get_slope(x0=0.0, y0=left_value, x1=1.0, y1=right_value)
    intercept = left_value
    if slope == 0:
        return False
    try:
        target_x = (mid_value - intercept) / slope
    except ZeroDivisionError:
        return False
    is_between_left_and_right = 0.0 <= target_x <= 1.0
    return is_between_left_and_right


Point2D = Union[numpy.ndarray, Tuple[float, float]]


def _get_mean_points_near_to_target(
    end_mean_curve: Series, target_point: Tuple[float, float]
) -> Tuple[Point2D, Point2D]:
    """

    Args:
        end_mean_curve:
        target_point:

    Returns:
        Tuple[Point2D, Point2D]

    .. doctest::

        >>> from pandas import Series, Index
        >>> horizontallinear0_target = (0.972496, 9.991761)
        >>> horizontallinear0_sample_curve = Series(
        ...     [9.868422, 9.963931, 9.985395, 9.991761],
        ...     index=Index([0.960002, 0.969662, 0.972496, 0.973147], name="x")
        ... )
        >>> _get_mean_points_near_to_target(
        ...     end_mean_curve=horizontallinear0_sample_curve,
        ...     target_point=horizontallinear0_target
        ... )
        (array([0.972496, 9.985395]), array([0.973147, 9.991761]))

    """
    target_x, target_y = target_point
    point_meet_target_x = numpy.array([target_x, end_mean_curve.loc[target_x]])
    nearest_index_to_y = find_index_of_value_in_series(end_mean_curve, target_y)
    point_meet_target_y = numpy.array(
        [nearest_index_to_y, end_mean_curve.loc[nearest_index_to_y]]
    )
    return point_meet_target_x, point_meet_target_y


def _get_target_distances(
    end_mean_curve: Series, target_point: Tuple[float, float]
) -> Tuple[float, float]:
    """

    Args:
        end_mean_curve:
        target_point:

    Returns:

    .. doctest::

        >>> from pandas import Series, Index
        >>> import numpy as np
        >>> horizontallinear0_target = (0.972496, 9.991761)
        >>> horizontallinear0_sample_curve = Series(
        ...     [9.868422, 9.963931, 9.985395, 9.991761],
        ...     index=Index([0.960002, 0.969662, 0.972496, 0.973147], name="x")
        ... )
        >>> sample_distances = _get_target_distances(
        ...     end_mean_curve=horizontallinear0_sample_curve,
        ...     target_point=horizontallinear0_target
        ... )
        >>> np.round(sample_distances, 6)
        array([0.006366, 0.000651])

    """
    point_meet_target_x, point_meet_target_y = _get_mean_points_near_to_target(
        end_mean_curve=end_mean_curve, target_point=target_point
    )
    target_point = numpy.array(target_point)

    target_vector_x = target_point - point_meet_target_x
    target_vector_y = target_point - point_meet_target_y

    target_x_distance = linalg.norm(target_vector_x)
    target_y_distance = linalg.norm(target_vector_y)
    return target_x_distance, target_y_distance


def _get_cutting_index_at_shortest_distance(
    end_mean_curve: Series, target_point: Tuple[float, float]
) -> float:
    """
    Searches the point with the shortest distance towards the target point.
    The points in question are within the the ending mean curve of an
    extrapolated end cap. The first point in question contains the target
    x-value and the second point the target y-value.

    Args:
        end_mean_curve(Series):
            Mean curve of the extrapolated end cap.

        target_point:
            Target point for the extrapolation of the family of curves.

    Returns:
        float

    .. doctest::

        >>> # protected member access for purely for testing
        >>> # noinspection PyProtectedMember
        >>> from arithmeticmeancurve import _get_cutting_index_at_shortest_distance
        >>> from pandas import Series
        >>> sample_target = (1.0, 1.0)
        >>> _get_cutting_index_at_shortest_distance(
        ...     end_mean_curve=Series([0.9, 1.0], index=[1.0, 1.2]),
        ...     target_point=sample_target
        ... )
        1.0
        >>> _get_cutting_index_at_shortest_distance(
        ...     end_mean_curve=Series([0.9, 1.0], index=[1.0, 1.1]),
        ...     target_point=sample_target
        ... )
        1.0
        >>> _get_cutting_index_at_shortest_distance(
        ...     end_mean_curve=Series([0.9, 1.0], index=[1.0, 1.05]),
        ...     target_point=sample_target
        ... )
        1.05

    .. doctest::

        >>> from pandas import Series, Index
        >>> horizontallinear0_target = (0.972496, 9.991761)
        >>> horizontallinear0_sample_curve = Series(
        ...     [9.868422, 9.963931, 9.985395, 9.991761],
        ...     index=Index([0.960002, 0.969662, 0.972496, 0.973147], name="x")
        ... )
        >>> _get_cutting_index_at_shortest_distance(
        ...     end_mean_curve=horizontallinear0_sample_curve,
        ...     target_point=horizontallinear0_target
        ... )
        0.973147

    """
    target_x_distance, target_y_distance = _get_target_distances(
        end_mean_curve=end_mean_curve, target_point=target_point
    )
    if target_x_distance < target_y_distance:
        return target_point[0]
    return end_mean_curve.index[-1]


class _ExtrapolationBreakCondition(ABC):
    @abstractmethod
    def is_meet(self, x_value: float, extrapolated_values: Series) -> True:
        pass


class _TargetValuesAreReachedCondition(_ExtrapolationBreakCondition):
    """

    .. testsetup::
        >>> from pandas import DataFrame
        >>> from doctestprinter import print_pandas
        >>> # protected member access for purely for testing
        >>> # noinspection PyProtectedMember
        >>> from arithmeticmeancurve import _TargetValuesAreReachedCondition
        >>> def test_returned_indexes(sample_frame, condition) -> List[float]:
        ...     indexes = []
        ...     for index, values in sample_frame.iterrows():
        ...         indexes.append(index)
        ...         if condition.is_meet(index, values):
        ...             return indexes
        ...     return indexes

    .. doctest::

        >>> first_quadrant_sample = DataFrame(
        ...     [[1, 3], [3, 5], [5, 7], [7, 9]],
        ...     columns=["y-1", "y-2"],
        ...     index = [0.1, 0.2, 0.3, 0.4]
        ... )
        >>> print_pandas(first_quadrant_sample.mean(axis=1), formats="{:>.1f}")
        0.1  2.0
        0.2  4.0
        0.3  6.0
        0.4  8.0
        >>> x_before_y = _TargetValuesAreReachedCondition(0.2, 5, 1.0)
        >>> test_returned_indexes(first_quadrant_sample, x_before_y)
        [0.1, 0.2, 0.3]

        >>> y_before_x = _TargetValuesAreReachedCondition(0.3, 3, 1.0)
        >>> test_returned_indexes(first_quadrant_sample, y_before_x)
        [0.1, 0.2, 0.3]

    .. doctest::

        >>> fourth_quadrant_sample = DataFrame(
        ...     [[-1, -3], [-3, -5], [-5, -7], [-7, -9]],
        ...     columns=["y-1", "y-2"],
        ...     index = [0.1, 0.2, 0.3, 0.4]
        ... )
        >>> print_pandas(fourth_quadrant_sample.mean(axis=1), formats="{:>.1f}")
        0.1  -2.0
        0.2  -4.0
        0.3  -6.0
        0.4  -8.0
        >>> x_before_y = _TargetValuesAreReachedCondition(0.2, -5, -1)
        >>> test_returned_indexes(fourth_quadrant_sample, x_before_y)
        [0.1, 0.2, 0.3]

        >>> y_before_x = _TargetValuesAreReachedCondition(0.3, -3, -1)
        >>> test_returned_indexes(fourth_quadrant_sample, y_before_x)
        [0.1, 0.2, 0.3]

    .. doctest::

        >>> second_quadrant_sample = DataFrame(
        ...     [[1, 3], [3, 5], [5, 7], [7, 9]],
        ...     columns=["y-1", "y-2"],
        ...     index = [-0.1, -0.2, -0.3, -0.4]
        ... )
        >>> print_pandas(second_quadrant_sample.mean(axis=1), formats="{:>.1f}")
        -0.1  2.0
        -0.2  4.0
        -0.3  6.0
        -0.4  8.0

        >>> x_before_y = _TargetValuesAreReachedCondition(-0.2, 5, 1)
        >>> test_returned_indexes(second_quadrant_sample, x_before_y)
        [-0.1, -0.2, -0.3]

        >>> y_before_x = _TargetValuesAreReachedCondition(-0.3, 3, 1)
        >>> test_returned_indexes(second_quadrant_sample, y_before_x)
        [-0.1, -0.2, -0.3]


    .. doctest::

        >>> third_quadrant_sample = DataFrame(
        ...     [[-1, -3], [-3, -5], [-5, -7], [-7, -9]],
        ...     columns=["y-1", "y-2"],
        ...     index = [-0.1, -0.2, -0.3, -0.4]
        ... )
        >>> print_pandas(third_quadrant_sample.mean(axis=1), formats="{:>.1f}")
        -0.1  -2.0
        -0.2  -4.0
        -0.3  -6.0
        -0.4  -8.0

        >>> x_before_y = _TargetValuesAreReachedCondition(-0.2, -5, -1)
        >>> test_returned_indexes(third_quadrant_sample, x_before_y)
        [-0.1, -0.2, -0.3]

        >>> y_before_x = _TargetValuesAreReachedCondition(-0.3, -3, -1)
        >>> test_returned_indexes(third_quadrant_sample, y_before_x)
        [-0.1, -0.2, -0.3]

    """

    def __init__(
        self,
        target_x_value: float,
        target_y_value: float,
        starting_last_mean_value: float,
    ):
        self._target_x_value = target_x_value
        self._x_target_was_meet = False
        self._y_target_was_meet = False
        self._target_y_value = target_y_value
        self._last_mean_value = starting_last_mean_value

    def is_meet(self, x_value: float, extrapolated_values: Series) -> True:
        assert isinstance(
            x_value, float
        ), "x_value must be a float, got `{}` instead.".format(type(x_value))
        assert isinstance(
            extrapolated_values, Series
        ), "extrapolated_values must be type of `pandas.Series`, got `{}` instead.".format(
            type(extrapolated_values)
        )
        if not self._y_target_was_meet:
            current_mean_value = extrapolated_values.mean()
            y_target_is_meet = _target_is_in_between(
                left_value=self._last_mean_value,
                mid_value=self._target_y_value,
                right_value=current_mean_value,
            )
            self._y_target_was_meet = y_target_is_meet

        if not self._x_target_was_meet:
            self._x_target_was_meet = x_value == self._target_x_value
        self._last_mean_value = extrapolated_values.mean()
        targets_are_meet = self._x_target_was_meet and self._y_target_was_meet
        return targets_are_meet


def _extrapolate_until_targets_are_included(
    extrapolates: Extrapolates,
    end_cap: DataFrame,
    target_x_mean_value: float,
    target_y_mean_value: float,
    starting_last_mean_value: float,
) -> DataFrame:
    """
    Extrapolate until the x and y target are included.

    Args:
        extrapolates(Extrapolates):
            The extraplation method.

        end_cap(DataFrame):
            The end cap of the family of curves which should be extrapolated.

        target_x_mean_value:
            The x value which might be represented within the mean curve.

        target_y_mean_value:
            The y value which might be represented within the mean curve.

        starting_last_mean_value:
            The prior mean value before the end cap starts.

    Returns:
        DataFrame

    .. doctest::

        >>> import examplecurves
        >>> # protected member access for purely for testing
        >>> # noinspection PyProtectedMember
        >>> from arithmeticmeancurve import (
        ...     ArithmeticMeanCurve,
        ...     _preprocess_end_cap_for_extrapolation,
        ...     _extrapolate_until_targets_are_included
        ... )
        >>> from doctestprinter import doctest_print
        >>> sample_curves = examplecurves.Static.create("nonlinear0")
        >>> sample_mean_curve = ArithmeticMeanCurve(sample_curves)
        >>> target_x = sample_mean_curve.statistics.end_x_mean
        >>> target_x
        1.024
        >>> target_y = sample_mean_curve.statistics.end_y_mean
        >>> round(target_y, 6)
        10.446849
        >>> starting_mean_value = sample_mean_curve.get_last_full_row().mean(axis=1).iloc[0]
        >>> prepared_end_cap = _prepare_end_cap_for_extrapolation(sample_mean_curve)
        >>> sample_mean_curve.prepare_extrapolation()
        >>> extrapolated_end_cap = _extrapolate_until_targets_are_included(
        ...     extrapolates=sample_mean_curve,
        ...     end_cap=prepared_end_cap,
        ...     target_x_mean_value=target_x,
        ...     target_y_mean_value=target_y,
        ...     starting_last_mean_value=starting_mean_value
        ... )
        >>> doctest_print(extrapolated_end_cap.round(3))
                 y_0     y_1    y_2     y_3     y_4
        x
        0.920  8.100   9.650  9.390  11.290  11.600
        0.960  8.276   9.825  9.595  11.500  11.792
        0.999  8.448   9.996  9.795  11.650  11.965
        1.000  8.452  10.000  9.799  11.654  11.969
        1.024  8.558  10.146  9.894  11.770  12.084
    """
    break_condition = _TargetValuesAreReachedCondition(
        target_x_value=target_x_mean_value,
        target_y_value=target_y_mean_value,
        starting_last_mean_value=starting_last_mean_value,
    )
    extrapolations = []
    for x_value, y_values in end_cap.iterrows():
        extrapolated_values = extrapolates(y_values)
        extrapolations.append(extrapolated_values)
        if break_condition.is_meet(
            x_value=x_value, extrapolated_values=extrapolated_values
        ):
            break
    additional_end_cap = DataFrame(extrapolations)
    additional_end_cap.index.name = end_cap.index.name
    return additional_end_cap


def _preprocess_end_cap_for_extrapolation(
    end_cap: DataFrame,
    last_middle_block_row: DataFrame,
    mandatory_x_values: List[float],
) -> DataFrame:
    """
    Creates an ending cap for calculation of the extrapolated part of the mean curve.
    Since the ordinate value of the mean curve are the extrapolation result, the
    first potential mean curves ending is an abscissa value (x-value). By default
    this value is the arithmetic mean of the family of curves ending points, the
    mean curve carries.

    Args:
        end_cap(DataFrame):
            The ending cap of family of curves, in which values needs to be
            extrapolated.

        last_middle_block_row(DataFrame):
            The last row of the family of curves before the ending cap, which
            has all values defined.

        mandatory_x_values(List[float]):
            Mandatory x-valeus which should definitelly be contained within
            prepared end cap.

    Returns:
        DataFrame

    .. doctest::

        horizontallinear0 has a target_x_value, which is lower then the first
        end cap index.

        >>> import examplecurves
        >>> # protected member access for purely for testing
        >>> # noinspection PyProtectedMember
        >>> from arithmeticmeancurve import (
        ...     ArithmeticMeanCurve,
        ...     _preprocess_end_cap_for_extrapolation
        ... )
        >>> from doctestprinter import doctest_print
        >>> sample_curves = examplecurves.Static.create("horizontallinear0")
        >>> sample_mean_curve = ArithmeticMeanCurve(sample_curves)
        >>> target_x_value = sample_mean_curve.statistics.end_x_mean
        >>> target_x_value
        1.0110986280155145
        >>> unprepared_end_cap = sample_mean_curve.get_end_cap()
        >>> last_full_value_row = sample_mean_curve.get_last_full_row()
        >>> doctest_print(unprepared_end_cap)
                        y_0        y_1       y_2        y_3  y_4
        x
        1.015576   9.952944   9.969411  10.00342   9.922124  NaN
        1.020281   9.999060  10.015604       NaN   9.968098  NaN
        1.022279  10.018633        NaN       NaN   9.987611  NaN
        1.028039        NaN        NaN       NaN  10.043892  NaN
        >>> sample_end_cap = _preprocess_end_cap_for_extrapolation(
        ...     end_cap=unprepared_end_cap,
        ...     last_middle_block_row=last_full_value_row,
        ...     mandatory_x_values=[target_x_value]
        ... )
        >>> doctest_print(sample_end_cap)
                        y_0        y_1        y_2        y_3  y_4
        x
        1.011099   9.909065   9.925460   9.959319   9.878382  NaN
        1.015576   9.952944   9.969411  10.003420   9.922124  NaN
        1.020281   9.999060  10.015604        NaN   9.968098  NaN
        1.022279  10.018633        NaN        NaN   9.987611  NaN
        1.028039        NaN        NaN        NaN  10.043892  NaN

    .. doctest::

        >>> import examplecurves
        >>> # protected member access for purely for testing
        >>> # noinspection PyProtectedMember
        >>> from arithmeticmeancurve import (
        ...     ArithmeticMeanCurve,
        ...     _preprocess_end_cap_for_extrapolation
        ... )
        >>> from doctestprinter import doctest_print
        >>> sample_curves = examplecurves.Static.create("nonlinear0")
        >>> sample_mean_curve = ArithmeticMeanCurve(sample_curves)
        >>> target_x_value = sample_mean_curve.statistics.end_x_mean
        >>> target_x_value
        1.024
        >>> unprepared_end_cap = sample_mean_curve.get_end_cap()
        >>> last_full_value_row = sample_mean_curve.get_last_full_row()
        >>> doctest_print(unprepared_end_cap)
                    y_0        y_1        y_2        y_3  y_4
        x
        0.920  8.100000   9.650000   9.390069  11.290365  NaN
        0.960  8.276087   9.825000   9.595123  11.500000  NaN
        0.999  8.447772   9.995625   9.795051        NaN  NaN
        1.000  8.452174  10.000000   9.799007        NaN  NaN
        1.035  8.606250        NaN   9.937492        NaN  NaN
        1.110  8.863043        NaN  10.234246        NaN  NaN
        1.150  9.000000        NaN        NaN        NaN  NaN
        >>> sample_end_cap = _preprocess_end_cap_for_extrapolation(
        ...     end_cap=unprepared_end_cap,
        ...     last_middle_block_row=last_full_value_row,
        ...     mandatory_x_values=[target_x_value]
        ... )
        >>> doctest_print(sample_end_cap)
                    y_0        y_1        y_2        y_3  y_4
        x
        0.920  8.100000   9.650000   9.390069  11.290365  NaN
        0.960  8.276087   9.825000   9.595123  11.500000  NaN
        0.999  8.447772   9.995625   9.795051        NaN  NaN
        1.000  8.452174  10.000000   9.799007        NaN  NaN
        1.024  8.557826        NaN   9.893968        NaN  NaN
        1.035  8.606250        NaN   9.937492        NaN  NaN
        1.110  8.863043        NaN  10.234246        NaN  NaN
        1.150  9.000000        NaN        NaN        NaN  NaN

    """
    # Creating the end cap for calculation of the extrapolated part of the
    # mean curve.
    assert isinstance(mandatory_x_values, list), "`mandatory_x_values` must be a list."

    sorted_mandatory_x_values = list(sorted(mandatory_x_values))
    combined_rows = pandas.concat((last_middle_block_row, end_cap))
    combined_rows = add_blank_rows(
        source=combined_rows, indexes_to_add=sorted_mandatory_x_values
    )
    combined_rows.interpolate(method="index", limit_area="inside", inplace=True)
    prepared_end_cap = combined_rows.iloc[1:]
    return prepared_end_cap


def _prepare_end_cap_for_extrapolation(a_mean_curve: AMeanCurve):
    """
    Creates an ending cap for calculation of the extrapolated part of the mean curve.
    Since the ordinate value of the mean curve are the extrapolation result, the
    first potential mean curves ending is an abscissa value (x-value). By default
    this value is the arithmetic mean of the family of curves ending points, the
    mean curve carries.

    Args:
        a_mean_curve(AMeanCurve):
            #ToDo Change expression 'AMeanCurve' since it is misleading.

    Returns:
        DataFrame

    .. doctest::

        horizontallinear0 has a target_x_value, which is lower then the first
        end cap index.

        >>> import examplecurves
        >>> # protected member access for purely for testing
        >>> # noinspection PyProtectedMember
        >>> from arithmeticmeancurve import (
        ...     ArithmeticMeanCurve,
        ...     _preprocess_end_cap_for_extrapolation
        ... )
        >>> from doctestprinter import doctest_print
        >>> sample_curves = examplecurves.Static.create("horizontallinear0")
        >>> sample_mean_curve = ArithmeticMeanCurve(sample_curves)
        >>> target_x_value = sample_mean_curve.statistics.end_x_mean
        >>> target_x_value
        1.0110986280155145
        >>> doctest_print(sample_mean_curve.get_end_cap())
                        y_0        y_1       y_2        y_3  y_4
        x
        1.015576   9.952944   9.969411  10.00342   9.922124  NaN
        1.020281   9.999060  10.015604       NaN   9.968098  NaN
        1.022279  10.018633        NaN       NaN   9.987611  NaN
        1.028039        NaN        NaN       NaN  10.043892  NaN
        >>> sample_end_cap = _prepare_end_cap_for_extrapolation(sample_mean_curve)
        >>> doctest_print(sample_end_cap)
                        y_0        y_1        y_2        y_3  y_4
        x
        1.011099   9.909065   9.925460   9.959319   9.878382  NaN
        1.015576   9.952944   9.969411  10.003420   9.922124  NaN
        1.020281   9.999060  10.015604        NaN   9.968098  NaN
        1.022279  10.018633        NaN        NaN   9.987611  NaN
        1.028039        NaN        NaN        NaN  10.043892  NaN

    .. doctest::

        >>> import examplecurves
        >>> # protected member access for purely for testing
        >>> # noinspection PyProtectedMember
        >>> from arithmeticmeancurve import (
        ...     ArithmeticMeanCurve,
        ...     _preprocess_end_cap_for_extrapolation
        ... )
        >>> from doctestprinter import doctest_print
        >>> sample_curves = examplecurves.Static.create("nonlinear0")
        >>> sample_mean_curve = ArithmeticMeanCurve(sample_curves)
        >>> target_x_value = sample_mean_curve.statistics.end_x_mean
        >>> target_x_value
        1.024
        >>> doctest_print(sample_mean_curve.get_end_cap())
                    y_0        y_1        y_2        y_3  y_4
        x
        0.920  8.100000   9.650000   9.390069  11.290365  NaN
        0.960  8.276087   9.825000   9.595123  11.500000  NaN
        0.999  8.447772   9.995625   9.795051        NaN  NaN
        1.000  8.452174  10.000000   9.799007        NaN  NaN
        1.035  8.606250        NaN   9.937492        NaN  NaN
        1.110  8.863043        NaN  10.234246        NaN  NaN
        1.150  9.000000        NaN        NaN        NaN  NaN
        >>> sample_end_cap = _prepare_end_cap_for_extrapolation(sample_mean_curve)
        >>> doctest_print(sample_end_cap)
                    y_0        y_1        y_2        y_3  y_4
        x
        0.920  8.100000   9.650000   9.390069  11.290365  NaN
        0.960  8.276087   9.825000   9.595123  11.500000  NaN
        0.999  8.447772   9.995625   9.795051        NaN  NaN
        1.000  8.452174  10.000000   9.799007        NaN  NaN
        1.024  8.557826        NaN   9.893968        NaN  NaN
        1.035  8.606250        NaN   9.937492        NaN  NaN
        1.110  8.863043        NaN  10.234246        NaN  NaN
        1.150  9.000000        NaN        NaN        NaN  NaN

    """
    full_end_cap = a_mean_curve.get_end_cap()
    last_full_row = a_mean_curve.get_last_full_row()
    required_x_values = [a_mean_curve.statistics.end_x_mean]

    return _preprocess_end_cap_for_extrapolation(
        end_cap=full_end_cap,
        last_middle_block_row=last_full_row,
        mandatory_x_values=required_x_values,
    )


def _calculate_mean_and_std_curve(
    a_mean_curve: "ArithmeticMeanCurve",
) -> Tuple[Series, Series]:
    """
    Calculates the actual mean curve and standard deviation curve.

    Args:
        a_mean_curve:

    Returns:
        Tuple[Series, Series]:
            Arithmetic mean and standard deviation curve

    .. doctest::

        >>> import examplecurves
        >>> # protected member access for purely for testing
        >>> # noinspection PyProtectedMember
        >>> from arithmeticmeancurve import (
        ...     ArithmeticMeanCurve,
        ...     _calculate_mean_and_std_curve
        ... )
        >>> from doctestprinter import doctest_print
        >>> sample_curves = examplecurves.Static.create("nonlinear0")
        >>> sample_mean_curve = ArithmeticMeanCurve(sample_curves)
        >>> sample_mean, sample_std = _calculate_mean_and_std_curve(
        ...     a_mean_curve=sample_mean_curve
        ... )
        >>> round(sample_mean_curve.statistics.end_x_mean, 3)
        1.024
        >>> round(sample_mean_curve.statistics.end_y_mean, 3)
        10.447
        >>> doctest_print(sample_mean.iloc[-3:].round(3))
        x
        1.00000    10.375
        1.01496    10.447
        1.02400    10.490
        dtype: float64
        >>> doctest_print(sample_std.iloc[-3:].round(3))
        x
        1.00000    1.445
        1.01496    1.447
        1.02400    1.448
        dtype: float64

    .. doctest::

        >>> import examplecurves
        >>> # protected member access for purely for testing
        >>> # noinspection PyProtectedMember
        >>> from arithmeticmeancurve import (
        ...     ArithmeticMeanCurve,
        ...     _calculate_mean_and_std_curve
        ... )
        >>> from doctestprinter import doctest_print
        >>> sample_curves = examplecurves.Static.create("horizontallinear1")
        >>> sample_mean_curve = ArithmeticMeanCurve(sample_curves)
        >>> sample_mean, sample_std = _calculate_mean_and_std_curve(
        ...     a_mean_curve=sample_mean_curve
        ... )
        >>> round(sample_mean_curve.statistics.end_x_mean, 3)
        0.972
        >>> round(sample_mean_curve.statistics.end_y_mean, 3)
        9.992
        >>> doctest_print(sample_mean.iloc[-3:].round(3))
        x
        0.969662    9.964
        0.972496    9.985
        0.973147    9.992
        dtype: float64
        >>> doctest_print(sample_std.iloc[-3:].round(3))
        x
        0.969662    0.277
        0.972496    0.274
        0.973147    0.274
        dtype: float64
    """
    if a_mean_curve.has_no_end_cap:
        mid_block_values = a_mean_curve.get_middle_value_block()
        mean_curve = mid_block_values.mean(axis=1)
        std_curve = mid_block_values.std(axis=1)
        return mean_curve, std_curve

    target_end_x_value = a_mean_curve.statistics.end_x_mean
    target_end_y_value = a_mean_curve.statistics.end_y_mean
    target_point = (target_end_x_value, target_end_y_value)

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
    index_for_target_y = _calculate_cutting_index_for_value(
        series_to_cut=current_end_mean_curve,
        cutting_y_value=target_end_y_value,
    )

    target_y_intersects_before_target_x = index_for_target_y < target_end_x_value
    if target_y_intersects_before_target_x:
        extrapolated_end_cap_with_targets = add_blank_rows(
            source=extrapolated_end_cap, indexes_to_add=[index_for_target_y]
        )
        extrapolated_end_cap_with_targets.interpolate(
            method="index", limit_area="inside", inplace=True
        )
    else:
        extrapolated_end_cap_with_targets = cut_after(
            source_to_cut=extrapolated_end_cap,
            cutting_index=index_for_target_y,
        )

    end_mean_curve_with_targets = extrapolated_end_cap_with_targets.mean(axis=1)
    cutting_index_at_shortest_distance = _get_cutting_index_at_shortest_distance(
        end_mean_curve=end_mean_curve_with_targets,
        target_point=target_point,
    )
    final_end_cap = cut_after(
        source_to_cut=extrapolated_end_cap_with_targets,
        cutting_index=cutting_index_at_shortest_distance,
    )
    final_end_cap = final_end_cap.iloc[1:]

    middle_value_block = a_mean_curve.get_middle_value_block()
    all_curves_extrapolated = pandas.concat([middle_value_block, final_end_cap])

    mean_curve = all_curves_extrapolated.mean(axis=1)
    std_curve = all_curves_extrapolated.std(axis=1)

    return mean_curve, std_curve


class ArithmeticMeanCurve(ExtrapolatingMeanCurve, AMeanCurve):
    def __init__(
        self, curves: Union[SetOfCurves, FamilyOfCurves], method: Optional[str] = None
    ):
        """
        Represents a family of curves.

        Args:
            curves(Union[SetOfCurves, FamilyOfCurves]):
                A '*set of unique curves*' with seperated x-values or a
                'family of curves' with common x-values.

            method(str):
                Default 'frozen_std'; extrapolation method to use.

        Examples:
            >>> import examplecurves
            >>> from doctestprinter import doctest_print, doctest_iter_print
            >>> sample_curves = examplecurves.Static.create(family_name="nonlinear0")
            >>> doctest_iter_print(sample_curves, edits_item=lambda x: x.iloc[:3])
                         y
            x
            0.000  0.00000
            0.115  1.40625
            0.230  2.70000
                      y
            x
            0.0  0.0000
            0.1  1.5625
            0.2  3.0000
                          y
            x
            0.000  0.000000
            0.111  1.607654
            0.222  3.085479
                          y
            x
            0.000  0.000000
            0.096  1.796875
            0.192  3.450000
                         y
            x
            0.00  0.000000
            0.09  1.796875
            0.18  3.450000
            >>> from arithmeticmeancurve import ArithmeticMeanCurve
            >>> extrapolating_mean_curve = ArithmeticMeanCurve(curves=sample_curves)
            >>> doctest_print(extrapolating_mean_curve.family_of_curves.loc[:0.2])
                        y_0       y_1       y_2       y_3       y_4
            x
            0.000  0.000000  0.000000  0.000000  0.000000  0.000000
            0.090  1.100543  1.406250  1.303503  1.684570  1.796875
            0.096  1.173913  1.500000  1.390403  1.796875  1.907083
            0.100  1.222826  1.562500  1.448337  1.865755  1.980556
            0.111  1.357337  1.720625  1.607654  2.055176  2.182604
            0.115  1.406250  1.778125  1.660909  2.124056  2.256076
            0.180  2.137500  2.712500  2.526302  3.243359  3.450000
            0.192  2.272500  2.885000  2.686067  3.450000  3.651250
            0.200  2.362500  3.000000  2.792577  3.575781  3.785417


            .. plot:: ./pyplots/example_10_full.py

            **Figure**: Extrapolated mean curve with scatter curve.

        """
        super().__init__(method=method)
        self.curves = None
        self._family_of_curves = None
        # Will be initialized by _initialize
        # noinspection PyTypeChecker
        self._mid_value_block_positions: BlockSectionPositions = None
        self._numbered_index = None
        self._mean_curve = None
        self._std_curve = None
        self._std_scatter_curve = None
        self._curves_end_points = None
        self._statistics = None
        self._std_circle = None
        self._initialize(curves=curves)
        self._is_calculated = False

    @property
    def has_no_end_cap(self):
        last_row_position = len(self._family_of_curves) - 1
        last_row_position_of_full_row = self._mid_value_block_positions.end_position
        return last_row_position == last_row_position_of_full_row

    def _calculate_mean_curve_if_needed(self):
        if not self._is_calculated:
            self.calculate()

    def _calculate_std_circle_if_needed(self):
        if self._std_circle is None:
            self._calculate_std_circle()

    def _initialize(self, curves: Union[List[Curves], DataFrame]):
        if isinstance(curves, DataFrame):
            self._family_of_curves = curves
        else:
            merged_frame = meld_set_of_curves_to_family(curves)
            self._family_of_curves = merged_frame.interpolate(
                method="index", limit_area="inside"
            )
        self._mid_value_block_positions = _estimate_block_section_positions(
            curve_group_frame=self._family_of_curves
        )
        self._numbered_index = DataFrame(
            numpy.arange(len(self._family_of_curves)),
            index=self._family_of_curves.index.copy(),
        )
        self._statistics = FamilyOfCurveStatistics(
            family_of_curves=self._family_of_curves
        )

    @property
    def statistics(self) -> FamilyOfCurveStatistics:
        """
        Provides statistics of the family of curves. Contains mean and standard
        deviation for starting, minimum, maximum and ending of the family of curves.

        Returns:
            FamilyOfCurveStatistics
        """
        return self._statistics

    @property
    def std_bars(self) -> StdBars:
        """
        Standard deviation bars.

        Returns:
            StdBars
        """
        self._calculate_std_circle_if_needed()
        return self._std_circle.std_bars

    @property
    def std_circle(self) -> StdCircle:
        """
        Represents the standard deviation as a circle.

        Returns:
            StdCircle

        Examples:

            The task of the standard deviation circle is to depict the x-y
            relation of the family of curves end points (figure 1). Its purpose
            is to give a quick visual impression of the family of curves deviation,
            within in a plot of multiple mean curves. Plotting all family of curves
            in such cases might visually overburden the figure. Std circles are
            best used accompanied with scatter curves.

            .. plot::

                import numpy
                import examplecurves
                from arithmeticmeancurve import extract_end_points, ArithmeticMeanCurve

                sample_curves = examplecurves.Static.create(
                    family_name="nonlinear0", predefined_offset=1,
                )
                extrapolating_mean_curve = ArithmeticMeanCurve(curves=sample_curves)
                end_points = extract_end_points(extrapolating_mean_curve.family_of_curves)
                x_values, y_values = end_points[:, 0], end_points[:, 1]

                import matplotlib.pyplot as plt

                # Setup figure
                fig = plt.figure(figsize=(9, 5), dpi=96)
                gspec = fig.add_gridspec(1, 1)
                axis = fig.add_subplot(gspec[0, 0])
                axis.set_title("extrapolated arithmetic mean curve")

                axis.plot(
                    *extrapolating_mean_curve.std_bars.horizontal,
                    "-|",
                    markersize=20,
                    label="Horizontal standard deviation",
                )
                axis.plot(
                    *extrapolating_mean_curve.std_bars.vertical,
                    "-_",
                    markersize=20,
                    label="Vertical standard deviation",
                )
                axis.plot(
                    x_values,
                    y_values,
                    "ok",
                    markersize=8,
                    label="end points of family of curves",
                )
                axis.plot(extrapolating_mean_curve.std_circle, "--k", label="Standard deviation circle")
                axis.plot(extrapolating_mean_curve.family_of_curves)
                # Finishing touch
                axis.set_xlim(0.9, 1.4)
                axis.set_ylim(8.5, 12.0)

                # Finishing touch
                axis.legend()
                plt.show()

            **Figure 1** Standard deviation circle.

            .. _figure 2:

            .. plot::

                import numpy
                import examplecurves
                from arithmeticmeancurve import extract_end_points, ArithmeticMeanCurve

                sample_curves = examplecurves.Static.create(
                    family_name="nonlinear0", predefined_offset=1,
                )
                extrapolating_mean_curve = ArithmeticMeanCurve(curves=sample_curves)
                end_points = extract_end_points(extrapolating_mean_curve.family_of_curves)
                x_values, y_values = end_points[:, 0], end_points[:, 1]

                import matplotlib.pyplot as plt

                # Setup figure
                fig = plt.figure(figsize=(9, 5), dpi=96)
                gspec = fig.add_gridspec(1, 1)
                axis = fig.add_subplot(gspec[0, 0])
                axis.set_title("extrapolated arithmetic mean curve")

                axis.plot(
                    x_values,
                    y_values,
                    "ok",
                    markersize=8,
                    label="end points of family of curves",
                )
                axis.plot(extrapolating_mean_curve.std_circle, "--k", label="Standard deviation circle")
                axis.boxplot(x_values, positions=[numpy.mean(y_values)], vert=False, manage_ticks=False)
                axis.boxplot(y_values, positions=[numpy.mean(x_values)], manage_ticks=False)
                # Finishing touch
                axis.set_xlim(0.9, 1.4)
                axis.set_ylim(8.5, 12.0)

                # Finishing touch
                axis.legend()
                plt.show()

            **Figure 2** Standard deviation circle versus box plots.

        """
        self._calculate_std_circle_if_needed()
        return self._std_circle.to_series()

    @property
    def mean_curve_end_point(self) -> numpy:
        return numpy.array([self._mean_curve.index[-1], self._mean_curve.iloc[-1]])

    @property
    def value_block_end_position(self) -> int:
        """

        Returns:

        """
        return self._mid_value_block_positions.end_position

    @property
    def family_of_curves(self) -> DataFrame:
        """
        The curves within a DataFrame interpolated.

        Returns:
            DataFrame

        Examples:
            >>> from pandas import DataFrame
            >>> import numpy
            >>> from arithmeticmeancurve import ArithmeticMeanCurve
            >>> curve_1 = DataFrame(
            ...     [1, 2, 3], index=[0.1, 0.2, 0.3], columns=["y"]
            ... )
            >>> curve_2 = DataFrame(
            ...     [1, 2, 3], index=[0.11, 0.19, 0.31], columns=["y"]
            ... )
            >>> curve_3 = DataFrame(
            ...     [1, 2, 3], index=[0.1, 0.21, 0.30], columns=["y"]
            ... )

            All single curves are being mapped onto a common index. Empty
            values are interpolated, within the curves inner boundaries.

            >>> extrapolating_mean_curve = ArithmeticMeanCurve([curve_1, curve_2, curve_3])
            >>> extrapolating_mean_curve.family_of_curves
                  y_0       y_1       y_2
            0.10  1.0       NaN  1.000000
            0.11  1.1  1.000000  1.090909
            0.19  1.9  2.000000  1.818182
            0.20  2.0  2.083333  1.909091
            0.21  2.1  2.166667  2.000000
            0.30  3.0  2.916667  3.000000
            0.31  NaN  3.000000       NaN


        **Comparision in between 'set of curves' and 'family of curves'**

            *Top figure*; the ingoing 'set of curves' is a set of
            unique curves with seperated absisa values (x-values).

            *Bottom figure*; the 'family of curves' share common abisa values
            (x-values). This is an necessary step towards the mean value curve
            calculation.


            .. plot::

               import examplecurves
               from arithmeticmeancurve import ArithmeticMeanCurve

               sample_curves = examplecurves.Static.create(
                   family_name="nonlinear0",
                   predefined_offset=1,
               )
               extrapolating_mean_curve = ArithmeticMeanCurve(sample_curves)
               family_of_curves = extrapolating_mean_curve.family_of_curves

               import matplotlib.pyplot as plt

               fig = plt.figure(figsize=(8, 10), dpi=96)
               gspec = fig.add_gridspec(2, 1)
               top_axis = fig.add_subplot(gspec[0, :])
               top_axis.set_title("Ingoing 'set of curves' (List[DataFrame])")
               for index, curve in enumerate(sample_curves):
                   current_label = "Sample curve {}".format(index)
                   top_axis.plot(curve, marker="o", markersize=3, label=current_label)

               bottom_axis = fig.add_subplot(gspec[1, :])
               bottom_axis.set_title("Curves with common index. (DataFrame)")
               for index, (label, curve) in enumerate(family_of_curves.iteritems()):
                   current_label = "Sample curve {}".format(index)
                   bottom_axis.plot(curve, marker="o", markersize=3, label=current_label)

               fig.tight_layout()
               plt.show()


        """
        return self._family_of_curves

    @property
    def mean_curve(self) -> DataFrame:
        """
        Arithmetic mean curve of the sample curves.

        Returns:
            DataFrame

        Examples:

            .. plot::

               import examplecurves
               from arithmeticmeancurve import ArithmeticMeanCurve

               sample_curves = examplecurves.Static.create(
                   family_name="nonlinear0",
                   predefined_offset=1,
               )
               a_mean_curve = ArithmeticMeanCurve(sample_curves)

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

        """
        self._calculate_mean_curve_if_needed()
        return self._mean_curve

    @property
    def std_curve(self):
        self._calculate_mean_curve_if_needed()
        return self._std_curve

    @property
    def scatter_curve(self):
        """
        Scatter curve representing the standard deviation.

        Returns:

        Arithmetic mean curve of the sample curves.

        Returns:
            DataFrame

        Examples:

            .. plot::

               import examplecurves
               from arithmeticmeancurve import ArithmeticMeanCurve

               sample_curves = examplecurves.Static.create(
                   family_name="nonlinear0",
                   predefined_offset=1,
               )
               extrapolating_mean_curve = ArithmeticMeanCurve(sample_curves)
               mean_curve = extrapolating_mean_curve.calculate_mean_curve()
               scatter_curve = extrapolating_mean_curve.calculate_scatter_curve()
               import matplotlib.pyplot as plt

               fig = plt.figure(figsize=(8, 5), dpi=96)
               gspec = fig.add_gridspec(1, 3)
               axis = fig.add_subplot(gspec[:, :2])
               for index, curve in enumerate(sample_curves):
                   current_label = "Sample curve {}".format(index)
                   axis.plot(curve, marker="o", markersize=3, label=current_label)

               axis.plot(scatter_curve, ":k", label="Scatter curve")

               axis.legend(bbox_to_anchor=(1.05, 1.02), loc='upper left')
               plt.show()

        """
        self._calculate_mean_curve_if_needed()
        return self._std_scatter_curve

    def prepare_extrapolation(self):
        # ToDo: The ArithmeticMeanCurve must be restructured into mixins.
        # This method should be placed within a super class.
        self._extrapolates.prepare_extrapolation(a_mean_curve=self)

    def calculate_scatter_curve(self) -> Series:
        mean_curve = self._mean_curve
        std_curve = self._std_curve
        upper_bound_curve = mean_curve + std_curve
        lower_bound_curve = mean_curve - std_curve
        upper_bound_curve = upper_bound_curve.reindex(upper_bound_curve.index[::-1])

        end_points = extract_end_points(self._family_of_curves)
        smallest_x = numpy.amin(end_points, axis=0)[0]

        upper_bound_curve = cut_after(
            source_to_cut=upper_bound_curve, cutting_index=smallest_x
        )
        lower_bound_curve = cut_after(
            source_to_cut=lower_bound_curve, cutting_index=smallest_x
        )

        blank_line = DataFrame([numpy.nan], index=pandas.Index([smallest_x]))

        scatter_curve = pandas.concat(
            (lower_bound_curve, blank_line, upper_bound_curve)
        )
        self._std_scatter_curve = scatter_curve
        return scatter_curve

    def calculate_mean_curve(self):
        mean_curve, std_curve = _calculate_mean_and_std_curve(a_mean_curve=self)
        self._mean_curve = mean_curve
        self._std_curve = std_curve

    def _calculate_std_circle(self):
        end_points = extract_end_points(self._family_of_curves)
        points_statistics = StatisticsOfPoints(end_points)
        self._std_circle = StdCircle(points_statistics, do_shear=False)

    def calculate(self):
        self.calculate_mean_curve()
        self.calculate_scatter_curve()
        self._calculate_std_circle()
        self._is_calculated = True

    def get_position_of_index(self, index: float) -> int:
        return self._numbered_index.loc[index]

    def get_middle_value_block(self):
        start_position, end_position = self._mid_value_block_positions
        return self._family_of_curves.iloc[start_position : end_position + 1].copy()

    def get_last_full_row(self) -> DataFrame:
        start_position, end_position = self._mid_value_block_positions
        return self._family_of_curves.iloc[end_position : end_position + 1].copy()

    def get_end_cap(self):
        start_position_of_end_cap = self._mid_value_block_positions.end_position + 1
        return self._family_of_curves.iloc[start_position_of_end_cap:].copy()

    def get_end_cap_after_x_mean(self):
        full_end_cap = self.get_end_cap()
        cut_end_cap = cut_after(
            source_to_cut=full_end_cap, cutting_index=self.statistics.end_x_mean
        )
        start_without_x_mean = slice(1, None, None)
        return cut_end_cap.iloc[start_without_x_mean].copy()


class FigureParameters(Mapping):
    """"""

    def __init__(
        self, figsize: Tuple[float, float], dpi: float = 96, tight_layout: bool = True
    ):
        self._figure_arguments = {
            "figsize": figsize,
            "dpi": dpi,
            "tight_layout": tight_layout,
        }

    def __getitem__(self, key) -> Any:
        return self._figure_arguments[key]

    def __len__(self) -> int:
        return len(self._figure_arguments)

    def __iter__(self) -> Iterator:
        return iter(self._figure_arguments)


_DEFAULT_ITERATION_RECORD_FORMAT = "{:<}{:>.2f}#{:>8.4f}"


class _IterationRecord(object):
    """
    >>> from pandas import Series, DataFrame, Index
    >>> import numpy
    >>> from doctestprinter import doctest_print, print_pandas
    >>> sample_start = Series(
    ...     [1.0, 1.5, numpy.nan], name=0.1, index=Index(["y0", "y1", "y2"], name="x")
    ... )
    >>> sample_iterations = DataFrame(
    ...     [[1.0, 1.5, 1.9], [1.0, 1.5, 2.0]],
    ...     columns=["y0", "y1", "y2"],
    ...     index=[1, 2]
    ... )
    >>> sample_record = _IterationRecord(
    ...     sample_start, sample_iterations
    ... )
    >>> doctest_print(sample_record.str_for_doctest())
                              y0        y1        y2
    sections      x
    start         0.10    1.0000    1.5000       nan
    extrapolated  0.10       nan       nan    2.0000
    iteration     0.10    1.0000    1.5000    1.9000
                  0.10    1.0000    1.5000    2.0000
    >>> print_pandas(sample_record.start_values)
         y0   y1   y2
    x
    0.1   1  1.5  nan
    >>> print_pandas(sample_record.iteration_history)
         y0   y1   y2
    x
    0.1   1  1.5  1.9
    0.1   1  1.5  2.0
    >>> print_pandas(sample_record.extrapolation_result)
         y0   y1  y2
    x
    0.1   1  1.5   2
    >>> print_pandas(sample_record.extrapolated_values)
          y0   y1  y2
    x
    0.1  nan  nan   2
    >>> reindex_sample = sample_record.reindex(iteration_number=2, common_divider=10)
    >>> print_pandas(reindex_sample, formats="{:<}{:>.1f}#{:>.1f}")
                        y0   y1   y2
    sections      x
    start         0.1  1.0  1.5  nan
    extrapolated  0.1  nan  nan  2.0
    iteration     2.1  1.0  1.5  1.9
                  2.2  1.0  1.5  2.0
    >>> reindex_sample_history = sample_record.get_reindex_history(
    ...     iteration_number=2, common_divider=10
    ... )
    >>> print_pandas(reindex_sample_history)
         y0   y1   y2
    2.1   1  1.5  1.9
    2.2   1  1.5  2.0
    """

    def __init__(
        self,
        start_values: Series,
        iteration_history: DataFrame,
    ):
        assert isinstance(
            start_values, Series
        ), "start_values must be of type `pandas.Series` got {} instead".format(
            type(start_values)
        )
        assert isinstance(
            iteration_history, DataFrame
        ), "iteration_history must be of type `pandas.DataFrame` got {} instead".format(
            type(iteration_history)
        )
        iteration_count = len(iteration_history)
        extrapolation_result = iteration_history.iloc[-1].copy()
        extrapolation_result.loc[start_values.notna()] = numpy.NaN
        record = pandas.concat(
            [
                start_values.to_frame().transpose(),
                extrapolation_result.to_frame().transpose(),
                iteration_history,
            ]
        )
        record.index = self.create_multi_index(
            index_section_name=start_values.index.name,
            index_value=start_values.name,
            iteration_count=iteration_count,
        )
        self._record = record

    @property
    def start_values(self) -> Series:
        return self._record.loc["start"]

    @property
    def iteration_history(self) -> DataFrame:
        return self._record.loc["iteration"]

    @property
    def extrapolation_result(self) -> Series:
        return self._record.loc["iteration"].iloc[-1:]

    @property
    def extrapolated_values(self) -> Series:
        return self._record.loc["extrapolated"]

    @property
    def empty(self):
        return self._record.empty

    @property
    def iteration_count(self):
        return len(self.iteration_history)

    def to_frame(self):
        return self._record.copy(deep=True)

    def get_reindex_history(self, iteration_number: int, common_divider: int):
        iteration_indexes = self.create_iteration_indexes(
            iteration_count=self.iteration_count,
            iteration_number=iteration_number,
            common_divider=common_divider,
        )
        reindex_history = self.iteration_history.copy()
        reindex_history.index = iteration_indexes
        return reindex_history

    @staticmethod
    def create_iteration_indexes(
        iteration_count: int, iteration_number: int = 0, common_divider: int = 1
    ):
        """

        Args:
            iteration_count:
            iteration_number:
            common_divider:

        Returns:

        Examples:
            >>> _IterationRecord.create_iteration_indexes(
            ...     iteration_count=3, iteration_number=2, common_divider=10
            ... )
            array([2.1, 2.2, 2.3])
        """
        try:
            common_divider = int(common_divider)
        except TypeError:
            raise TypeError("common_divider must be convertible to an integer.")
        assert (
            common_divider % 10 == 0 or common_divider == 1
        ), "common_divider must be 1 or a multiple of 10, got '{}' instead.".format(
            common_divider
        )
        history_index = numpy.arange(1, iteration_count + 1) / common_divider
        history_index += iteration_number
        return history_index

    @staticmethod
    def create_multi_index(
        index_section_name: str, index_value: float, iteration_count: int
    ):
        """

        Args:
            index_section_name:
            index_value:
            iteration_count:

        Returns:

        Examples:
            >>> sample_history_indexes = _IterationRecord.create_iteration_indexes(
            ...     iteration_count=3, iteration_number=2, common_divider=10
            ... )
            >>> _IterationRecord.create_multi_index("x", 0.1, 3)
            MultiIndex([(       'start', 0.1),
                        ('extrapolated', 0.1),
                        (   'iteration', 0.1),
                        (   'iteration', 0.1),
                        (   'iteration', 0.1)],
                       names=['sections', 'x'])
        """
        iteration_history_indexes = list(
            zip(
                repeat("iteration", iteration_count),
                repeat(index_value, iteration_count),
            )
        )
        indexes = [
            ("start", index_value),
            ("extrapolated", index_value),
        ] + iteration_history_indexes
        return MultiIndex.from_tuples(indexes, names=("sections", index_section_name))

    @classmethod
    def create_iteration_multi_index(
        cls,
        index_section_name: str,
        index_value: float,
        iteration_count: int,
        iteration_number: int,
        common_divider: Union[int, float],
    ):
        """

        Args:
            index_section_name:
            index_value:
            iteration_count:
            iteration_number:
            common_divider:

        Returns:

        Examples:
            >>> sample_history_indexes = _IterationRecord.create_iteration_indexes(
            ...     iteration_count=3, iteration_number=2, common_divider=10
            ... )
            >>> _IterationRecord.create_iteration_multi_index(
            ...     index_section_name="x",
            ...     index_value=0.1,
            ...     iteration_count=3,
            ...     iteration_number=2,
            ...     common_divider=10
            ... )
            MultiIndex([(       'start', 0.1),
                        ('extrapolated', 0.1),
                        (   'iteration', 2.1),
                        (   'iteration', 2.2),
                        (   'iteration', 2.3)],
                       names=['sections', 'x'])
        """
        iteration_numbers = cls.create_iteration_indexes(
            iteration_count=iteration_count,
            iteration_number=iteration_number,
            common_divider=common_divider,
        )
        head_indexes = [
            ("start", index_value),
            ("extrapolated", index_value),
        ]
        iteration_indexes = list(
            zip(repeat("iteration", iteration_count), iteration_numbers)
        )
        indexes = head_indexes + iteration_indexes
        return MultiIndex.from_tuples(indexes, names=("sections", index_section_name))

    def reindex(
        self, iteration_number: int, common_divider: Union[int, float]
    ) -> DataFrame:
        index_value = self._record.loc["start"].index[0]
        new_multi_index = self.create_iteration_multi_index(
            index_section_name=self.start_values.index.name,
            index_value=index_value,
            iteration_count=self.iteration_count,
            iteration_number=iteration_number,
            common_divider=common_divider,
        )
        requested_frame = self._record.copy()
        requested_frame.index = new_multi_index
        return requested_frame

    def __round__(self, n=None):
        return self.round(digits=n)

    def round(self, digits: int = 3) -> DataFrame:
        return self._record.round(digits)

    def __repr__(self):
        return str(self._record)

    def str_for_doctest(self, formats: Optional[str] = None):
        representation = prepare_pandas(
            self._record, formats=_DEFAULT_ITERATION_RECORD_FORMAT
        )
        return representation


class _IterationRecords(object):
    """
    >>> import examplecurves
    >>> # protected member access for purely for testing
    >>> # noinspection PyProtectedMember
    >>> from arithmeticmeancurve import (
    ...     FrozenStdExtrapolation,
    ...     ExtrapolationIterationTester
    ... )
    >>> from doctestprinter import print_pandas, doctest_iter_print
    >>> sample_curves = examplecurves.Static.create("nonlinear0")
    >>> frozen_std_extrapolation = FrozenStdExtrapolation()
    >>> test_method = ExtrapolationIterationTester.record_iterations
    >>> iteration_records = test_method(
    ...     set_of_curves=sample_curves, extrapolates=frozen_std_extrapolation
    ... )
    >>> print_pandas(iteration_records.get_start_values(), formats="{:>.3f}")
             y_0     y_1    y_2     y_3  y_4
    0.920  8.100   9.650  9.390  11.290  nan
    0.960  8.276   9.825  9.595  11.500  nan
    0.999  8.448   9.996  9.795     nan  nan
    1.000  8.452  10.000  9.799     nan  nan
    1.024  8.558     nan  9.894     nan  nan
    >>> print_pandas(iteration_records.get_extrapolation_result(), formats="{:>.3f}")
             y_0     y_1    y_2     y_3     y_4
    0.920  8.100   9.650  9.390  11.290  11.600
    0.960  8.276   9.825  9.595  11.500  11.792
    0.999  8.448   9.996  9.795  11.650  11.965
    1.000  8.452  10.000  9.799  11.654  11.969
    1.024  8.558  10.146  9.894  11.770  12.084

    """

    def __init__(self):
        self._records: List[_IterationRecord] = []
        self.printer_format = "{:>.2f}#{:>.4f}"

    def append(self, raw_iteration_record: _IterationRecord):
        self._records.append(raw_iteration_record)

    def get_common_divider(self) -> int:
        """
        Detects the minimum common divider for all records.

        Returns:
            int
        """
        max_iteration_count = 0
        for record in self._records:
            if max_iteration_count < record.iteration_count:
                max_iteration_count = record.iteration_count
        return self.calculate_common_divider(max_iteration_count=max_iteration_count)

    @staticmethod
    def calculate_common_divider(max_iteration_count: int) -> int:
        """

        Args:
            max_iteration_count:

        Returns:

        Examples:
            >>> _IterationRecords.calculate_common_divider(4)
            10
            >>> _IterationRecords.calculate_common_divider(99)
            100
            >>> _IterationRecords.calculate_common_divider(100)
            110

        """
        common_iteration_divider = 10
        for common_iteration_divider in map(lambda x: 10 * x, range(1, 100)):
            if max_iteration_count < common_iteration_divider:
                break
        return common_iteration_divider

    def get_complete_history(self) -> DataFrame:
        common_divider = self.get_common_divider()
        histories = []
        for index, record in enumerate(self._records):
            iteration_number = index + 1
            reindex_history = record.get_reindex_history(
                iteration_number=iteration_number, common_divider=common_divider
            )
            histories.append(reindex_history)
        complete_history = pandas.concat(histories)
        return complete_history

    def get_extrapolation(self) -> DataFrame:
        extrapolations = [record.extrapolated_values for record in self]
        extrapolation = pandas.concat(extrapolations)
        return extrapolation

    def get_start_values(self) -> DataFrame:
        start_values = [record.start_values for record in self]
        unchanged_values = pandas.concat(start_values)
        return unchanged_values

    def get_extrapolation_result(self) -> DataFrame:
        results = [record.extrapolation_result for record in self]
        extrapolation_result = pandas.concat(results)
        return extrapolation_result

    def to_frames(self) -> List[DataFrame]:
        requested_frames = []
        for record in self._records:
            frame = record.to_frame()
            requested_frames.append(frame)
        return requested_frames

    def __repr__(self):
        common_divider = self.get_common_divider()
        prepared_records = [
            str(
                record.reindex(
                    iteration_number=index + 1, common_divider=common_divider
                )
            )
            for index, record in enumerate(self)
        ]
        return "\n".join(prepared_records)

    def __getitem__(self, position):
        return self._records[position]

    def __iter__(self) -> Iterator[_IterationRecord]:
        return iter(self._records)

    def __next__(self) -> _IterationRecord:
        return next(self._records)

    def __len__(self) -> int:
        return len(self._records)

    def str_for_doctest(self, formats: Optional[str] = None):
        common_divider = self.get_common_divider()
        prepared_records = []
        for index, record in enumerate(self):
            record.reindex(iteration_number=index + 1, common_divider=common_divider)
            representation = record.str_for_doctest(formats=formats)
            prepared_records.append(representation)
        return "\n".join(prepared_records)


class ExtrapolationIterationTester(object):
    @staticmethod
    def record_iterations(
        set_of_curves: SetOfCurves, extrapolates: Extrapolates
    ) -> _IterationRecords:
        """

        Args:
            set_of_curves:
            extrapolates:

        Returns:

        .. doctest::

            >>> import examplecurves
            >>> # protected member access for purely for testing
            >>> # noinspection PyProtectedMember
            >>> from arithmeticmeancurve import (
            ...     FrozenStdExtrapolation,
            ...     ExtrapolationIterationTester
            ... )
            >>> from doctestprinter import doctest_print, doctest_iter_print
            >>> sample_curves = examplecurves.Static.create("nonlinear0")
            >>> frozen_std_extrapolation = FrozenStdExtrapolation()
            >>> test_method = ExtrapolationIterationTester.record_iterations
            >>> recorded_iterations = test_method(
            ...     set_of_curves=sample_curves, extrapolates=frozen_std_extrapolation
            ... )
            >>> doctest_print(recorded_iterations.str_for_doctest())
                                     y_0       y_1       y_2       y_3       y_4
            sections
            start         0.92    8.1000    9.6500    9.3901   11.2904       nan
            extrapolated  0.92       nan       nan       nan       nan   11.5998
            iteration     0.92    8.1000    9.6500    9.3901   11.2904   11.5000
                          0.92    8.1000    9.6500    9.3901   11.2904   11.5805
                          0.92    8.1000    9.6500    9.3901   11.2904   11.5966
                          0.92    8.1000    9.6500    9.3901   11.2904   11.5998
                                     y_0       y_1       y_2       y_3       y_4
            sections
            start         0.96    8.2761    9.8250    9.5951   11.5000       nan
            extrapolated  0.96       nan       nan       nan       nan   11.7917
            iteration     0.96    8.2761    9.8250    9.5951   11.5000   11.5998
                          0.96    8.2761    9.8250    9.5951   11.5000   11.7536
                          0.96    8.2761    9.8250    9.5951   11.5000   11.7844
                          0.96    8.2761    9.8250    9.5951   11.5000   11.7905
                          0.96    8.2761    9.8250    9.5951   11.5000   11.7917
                                     y_0       y_1       y_2       y_3       y_4
            sections
            start         1.00    8.4478    9.9956    9.7951       nan       nan
            extrapolated  1.00       nan       nan       nan   11.6502   11.9646
            iteration     1.00    8.4478    9.9956    9.7951   11.4773   11.7917
                          1.00    8.4478    9.9956    9.7951   11.5814   11.8959
                          1.00    8.4478    9.9956    9.7951   11.6231   11.9376
                          1.00    8.4478    9.9956    9.7951   11.6398   11.9542
                          1.00    8.4478    9.9956    9.7951   11.6464   11.9609
                          1.00    8.4478    9.9956    9.7951   11.6491   11.9636
                          1.00    8.4478    9.9956    9.7951   11.6502   11.9646
                                     y_0       y_1       y_2       y_3       y_4
            sections
            start         1.00    8.4522   10.0000    9.7990       nan       nan
            extrapolated  1.00       nan       nan       nan   11.6543   11.9688
            iteration     1.00    8.4522   10.0000    9.7990   11.6502   11.9646
                          1.00    8.4522   10.0000    9.7990   11.6531   11.9676
                          1.00    8.4522   10.0000    9.7990   11.6543   11.9688
                                     y_0       y_1       y_2       y_3       y_4
            sections
            start         1.02    8.5578       nan    9.8940       nan       nan
            extrapolated  1.02       nan   10.1465       nan   11.7695   12.0840
            iteration     1.02    8.5578   10.0313    9.8940   11.6543   11.9688
                          1.02    8.5578   10.0781    9.8940   11.7012   12.0156
                          1.02    8.5578   10.1063    9.8940   11.7293   12.0438
                          1.02    8.5578   10.1231    9.8940   11.7462   12.0606
                          1.02    8.5578   10.1332    9.8940   11.7563   12.0707
                          1.02    8.5578   10.1393    9.8940   11.7624   12.0768
                          1.02    8.5578   10.1430    9.8940   11.7660   12.0805
                          1.02    8.5578   10.1452    9.8940   11.7682   12.0827
                          1.02    8.5578   10.1465    9.8940   11.7695   12.0840

        """
        a_mean_curve = ArithmeticMeanCurve(set_of_curves)
        extrapolates.prepare_extrapolation(a_mean_curve=a_mean_curve)
        prepared_end_cap = _prepare_end_cap_for_extrapolation(a_mean_curve=a_mean_curve)
        target_x_value = a_mean_curve.statistics.end_x_mean
        target_y_value = a_mean_curve.statistics.end_y_mean
        starting_last_mean_value = a_mean_curve.get_last_full_row().mean(axis=1).iloc[0]
        break_condition = _TargetValuesAreReachedCondition(
            target_x_value=target_x_value,
            target_y_value=target_y_value,
            starting_last_mean_value=starting_last_mean_value,
        )

        iteration_records = _IterationRecords()
        for x_value, current_values in prepared_end_cap.iterrows():
            raw_interpolation_history = list(
                extrapolates.iter_extrapolate_row(values_at_x=current_values)
            )
            interpolation_history = DataFrame(raw_interpolation_history)
            iteration_records.append(
                _IterationRecord(
                    start_values=current_values,
                    iteration_history=interpolation_history,
                )
            )
            extrapolated_values = interpolation_history.iloc[-1]
            if break_condition.is_meet(
                x_value=x_value,
                extrapolated_values=extrapolated_values,
            ):
                break
        return iteration_records


class MeanCurvePlotter(object):
    @staticmethod
    def get_axis_limits(
        end_points: numpy.ndarray, x_padding: float = 0.1, y_padding: float = 0.1
    ) -> dict:
        """
        Returns the outer boundaries of a list of points for plotting.

        Args:
            end_points(numpy.ndarray):
                End point for which to calculate the boundaries.

            y_padding(float):
                Padding along the ordinate.

            x_padding(float):
                Padding along the abscissa.

        Returns:
            dict:
                A dictionary with xlim containing keyword arguments for
                matplotlib.pyplot.axis.set_xlim and analogue ylim.

        Examples:

            >>> sample_end_points = numpy.array(
            ...     [
            ...         [0.98,  9.96],
            ...         [1.01,  9.94],
            ...         [0.94,  9.99],
            ...         [1.03, 10.00],
            ...         [1.01,  9.95],
            ...     ]
            ... )
            >>> from doctestprinter import doctest_iter_print, round_collections
            >>> raw_axis_limits = MeanCurvePlotter.get_axis_limits(
            ...     end_points=sample_end_points, x_padding=0, y_padding=0
            ... )
            >>> doctest_iter_print(raw_axis_limits, edits_item=round_collections)
            xlim:
              {'left': 0.94, 'right': 1.03}
            ylim:
              {'bottom': 9.94, 'top': 10.0}
            >>> padded_axis_limits = MeanCurvePlotter.get_axis_limits(
            ...     end_points=sample_end_points
            ... )
            >>> doctest_iter_print(padded_axis_limits, edits_item=round_collections)
            xlim:
              {'left': 0.931, 'right': 1.039}
            ylim:
              {'bottom': 9.934, 'top': 10.006}

        """
        min_x, min_y = numpy.amin(end_points, axis=0)
        max_x, max_y = numpy.amax(end_points, axis=0)

        x_span = max_x - min_x
        y_span = max_y - min_y

        x_padding = x_padding * x_span
        y_padding = y_padding * y_span

        return {
            "xlim": {"left": min_x - x_padding, "right": max_x + x_padding},
            "ylim": {"bottom": min_y - y_padding, "top": max_y + y_padding},
        }

    @staticmethod
    def plot_mean_curve_end_region(
        axis: pyplot.axis,
        a_mean_curve: ArithmeticMeanCurve,
        sample_curve_color: str = "lightskyblue",
        title: str = None,
    ):
        """
        Plots into the end region of the family of curves and their mean curve.

        Args:
            axis:
            a_mean_curve:
            sample_curve_color:
            title:

        Returns:

        """
        curves_end_point = extract_end_points(a_mean_curve.family_of_curves)
        end_points = numpy.concatenate(
            (curves_end_point, [a_mean_curve.mean_curve_end_point])
        )
        end_x = a_mean_curve.statistics.end_x_mean
        end_y = a_mean_curve.statistics.end_y_mean
        if title is not None:
            axis.set_title(title)
        axis.plot(a_mean_curve.family_of_curves, "-o", color=sample_curve_color)
        axis.plot(a_mean_curve.mean_curve, "-ok")
        axis.plot(end_x, end_y, "rP")
        axis.plot(a_mean_curve.scatter_curve, "--ok")
        axis.plot(a_mean_curve.std_circle, "--r")
        axis_limits = MeanCurvePlotter.get_axis_limits(end_points=end_points)
        axis.set_ylim(**axis_limits["ylim"])
        axis.set_xlim(**axis_limits["xlim"])

    @staticmethod
    def plot(
        a_mean_curve: ArithmeticMeanCurve, title: str = None, with_marker: bool = True
    ):
        import matplotlib.pyplot as plt

        fig = plt.figure(figsize=(8, 5), dpi=96)
        gspec = fig.add_gridspec(1, 3)
        axis = fig.add_subplot(gspec[:, :2])

        MeanCurvePlotter.plot_default(
            axis=axis, a_mean_curve=a_mean_curve, title=title, with_marker=with_marker
        )

        axis.legend(bbox_to_anchor=(1.05, 1.02), loc="upper left")
        plt.show()
        plt.close(fig)

    @staticmethod
    def plot_default(
        axis: pyplot.axis,
        a_mean_curve: ArithmeticMeanCurve,
        title: str = None,
        with_marker: bool = True,
    ):
        """
        Plots into the end region of the family of curves and their mean curve.

        Args:
            axis:
            a_mean_curve:
            title:

        Returns:

        """
        if title is not None:
            axis.set_title(title)
        family_of_curves = a_mean_curve.family_of_curves
        end_x = a_mean_curve.statistics.end_x_mean
        end_y = a_mean_curve.statistics.end_y_mean

        if with_marker:
            curve_plot_kwargs = {"marker": "o", "makersize": 3}
            mean_curve_plot_kwargs = {"marker": "o", "markersize": 5}
        else:
            curve_plot_kwargs = {}
            mean_curve_plot_kwargs = {}

        for index, (label, curve) in enumerate(family_of_curves.iteritems()):
            current_label = "sample curve {}".format(index)
            axis.plot(curve, label=current_label, **curve_plot_kwargs)
        axis.plot(
            a_mean_curve.mean_curve,
            "--k",
            label="arithmetic mean curve",
            **mean_curve_plot_kwargs
        )
        axis.plot(end_x, end_y, "rP")
        axis.plot(a_mean_curve.std_circle, ":r", label="std circle")
        axis.plot(a_mean_curve.scatter_curve, ":k", label="scatter curve")

    @staticmethod
    def test_plot(
        sample_curves: SetOfCurves,
        upper_title: Optional[str] = None,
        lower_title: Optional[str] = None,
    ):
        a_mean_curve = ArithmeticMeanCurve(sample_curves)

        # Setup figure
        fig = plt.figure(figsize=(8, 10), dpi=96)
        gspec = fig.add_gridspec(2, 1)

        upper_axis = fig.add_subplot(gspec[0, :])
        MeanCurvePlotter.plot_default(
            axis=upper_axis, a_mean_curve=a_mean_curve, title=upper_title
        )

        lower_axis = fig.add_subplot(gspec[1, :])
        MeanCurvePlotter.plot_mean_curve_end_region(
            axis=lower_axis, a_mean_curve=a_mean_curve, title=lower_title
        )

        # Finishing touch
        plt.tight_layout()
        plt.show()

    @staticmethod
    def test_plot_mean_curve(
        a_mean_curve: AMeanCurve,
        upper_title: Optional[str] = None,
        lower_title: Optional[str] = None,
    ):
        # Setup figure
        fig = plt.figure(figsize=(8, 10), dpi=96)
        gspec = fig.add_gridspec(2, 1)

        upper_axis = fig.add_subplot(gspec[0, :])
        MeanCurvePlotter.plot_default(
            axis=upper_axis, a_mean_curve=a_mean_curve, title=upper_title
        )

        lower_axis = fig.add_subplot(gspec[1, :])
        MeanCurvePlotter.plot_mean_curve_end_region(
            axis=lower_axis, a_mean_curve=a_mean_curve, title=lower_title
        )

        # Finishing touch
        plt.tight_layout()
        plt.show()


class VisualIterationTester(object):
    @staticmethod
    def calculate_extrapolation_iteration_history(
        curves: SetOfCurves, extrapolates: Extrapolates
    ) -> Tuple[DataFrame, DataFrame]:
        """
        Calculates the history of the extrapolation's iterations of a mean curve.

        Args:
            curves(SetOfCurves):
                The set of curves for which a mean curve should be calculated,
                what triggers an extrapolation process.

            extrapolates(Extrapolates):
                The callable entity, which extrapolates the curves for
                calculating a mean curve.

        Returns:
            Tuple[DataFrame, DataFrame]:
                The *history of iterations per step* and the
                *extrapolated curve points*.

        .. doctest::

            >>> import examplecurves
            >>> from doctestprinter import doctest_print
            >>> from arithmeticmeancurve import VisualIterationTester as VIT
            >>> from arithmeticmeancurve import FrozenStdExtrapolation
            >>> example_curves = examplecurves.Static.create(
            ...     family_name="nonlinear0",
            ...     cut_curves_at=3,
            ...     predefined_offset=1
            ... )
            >>>
            >>> history, extrapolated = VIT.calculate_extrapolation_iteration_history(
            ...     example_curves, FrozenStdExtrapolation()
            ... )
            >>> history
                    y_0      y_1       y_2       y_3       y_4
            1.1  1.4950  1.64125  2.253517  3.530000  3.450000
            1.2  1.4950  1.64125  2.253517  3.530000  3.472464
            1.3  1.4950  1.64125  2.253517  3.530000  3.476956
            1.4  1.4950  1.64125  2.253517  3.530000  3.477855
            2.1  2.1115  2.42900  2.983110  3.523415  3.477855
            2.2  2.1115  2.42900  2.983110  3.949046  3.903486
            2.3  2.1115  2.42900  2.983110  4.119298  4.073738
            2.4  2.1115  2.42900  2.983110  4.187399  4.141839
            2.5  2.1115  2.42900  2.983110  4.214640  4.169080
            2.6  2.1115  2.42900  2.983110  4.225536  4.179976
            2.7  2.1115  2.42900  2.983110  4.229894  4.184334
            2.8  2.1115  2.42900  2.983110  4.231638  4.186078
            2.9  2.1115  2.42900  2.983110  4.232335  4.186775
            >>> extrapolated
                    y_0  y_1  y_2       y_3       y_4
            0.2020  NaN  NaN  NaN       NaN  3.477855
            0.2568  NaN  NaN  NaN  4.232335  4.186775

            >>> example_curves = examplecurves.Static.create(
            ...     family_name="horizontallinear0",
            ... )
            >>>
            >>> history, extrapolated = VIT.calculate_extrapolation_iteration_history(
            ...     example_curves, FrozenStdExtrapolation()
            ... )
            >>> history
                      y_0       y_1        y_2       y_3        y_4
            1.1  9.909065  9.925460   9.959319  9.878382   9.998682
            1.2  9.909065  9.925460   9.959319  9.878382  10.326551
            1.3  9.909065  9.925460   9.959319  9.878382  10.392125
            1.4  9.909065  9.925460   9.959319  9.878382  10.405240
            1.5  9.909065  9.925460   9.959319  9.878382  10.407863
            2.1  9.952944  9.969411  10.003420  9.922124  10.407863
            2.2  9.952944  9.969411  10.003420  9.922124  10.443522
            2.3  9.952944  9.969411  10.003420  9.922124  10.450654
            2.4  9.952944  9.969411  10.003420  9.922124  10.452080
            >>> extrapolated
                      y_0  y_1  y_2  y_3        y_4
            1.011099  NaN  NaN  NaN  NaN  10.407863
            1.015576  NaN  NaN  NaN  NaN  10.452080

        """
        a_mean_curve = ArithmeticMeanCurve(curves=curves)
        extrapolates.prepare_extrapolation(a_mean_curve=a_mean_curve)
        prepared_end_cap = _prepare_end_cap_for_extrapolation(a_mean_curve=a_mean_curve)
        target_x_value = a_mean_curve.statistics.end_x_mean
        target_y_value = a_mean_curve.statistics.end_y_mean
        starting_last_mean_value = a_mean_curve.get_last_full_row().mean(axis=1).iloc[0]
        break_condition = _TargetValuesAreReachedCondition(
            target_x_value=target_x_value,
            target_y_value=target_y_value,
            starting_last_mean_value=starting_last_mean_value,
        )

        all_steps_of_iterations = []
        extrapolation_results = []
        max_number_of_iterations = 0
        for x_value, current_values in prepared_end_cap.iterrows():
            steps_of_iteration = list(
                extrapolates.iter_extrapolate_row(values_at_x=current_values)
            )

            mask_of_existing_values = current_values.notna()
            extrapolation_result = steps_of_iteration[-1].copy()
            break_at_the_end = break_condition.is_meet(
                x_value=x_value, extrapolated_values=extrapolation_result
            )
            extrapolation_result.loc[mask_of_existing_values] = numpy.nan
            extrapolation_results.append(extrapolation_result)

            iteration_steps_as_frame = DataFrame(steps_of_iteration)
            all_steps_of_iterations.append(iteration_steps_as_frame)
            max_number_of_iterations = len(iteration_steps_as_frame)
            if break_at_the_end:
                break

        common_iteration_divider = 10
        for common_iteration_divider in map(lambda x: 10 * x, range(1, 100)):
            if max_number_of_iterations < common_iteration_divider:
                break

        for row_index, iteration_steps in enumerate(all_steps_of_iterations):
            current_iteration_count = len(iteration_steps)
            new_index = (
                numpy.arange(1, current_iteration_count + 1) / common_iteration_divider
            )
            new_index += row_index + 1
            old_index_name = iteration_steps.index.name
            iteration_steps.index = pandas.Index(new_index, name=old_index_name)

        iteration_history = pandas.concat(all_steps_of_iterations)
        extrapolated_curves = pandas.concat(extrapolation_results, axis=1).transpose()
        return iteration_history, extrapolated_curves

    @classmethod
    def plot_extrapolation_test(cls, curves: SetOfCurves, extrapolates: Extrapolates):
        iteration_records = ExtrapolationIterationTester.record_iterations(
            set_of_curves=curves, extrapolates=extrapolates
        )
        iteration_history = iteration_records.get_complete_history()
        extrapolated_curves = iteration_records.get_extrapolation()
        original_values = iteration_records.get_start_values()
        complete_values = iteration_records.get_extrapolation_result()
        iteration_mean_curve = iteration_history.mean(axis=1)
        complete_mean_curve = complete_values.mean(axis=1)

        family_of_curves = convert_set_to_family_of_curves(curves)
        statistics = FamilyOfCurveStatistics(family_of_curves=family_of_curves)
        a_mean_point = [statistics.end_x_mean, statistics.end_y_mean]

        import matplotlib.pyplot as plt
        from matplotlib import cm

        tab10_cm = cm.get_cmap("tab20")
        color_pairs = list(
            map(lambda i: (tab10_cm(i * 2), tab10_cm((i * 2) + 1)), range(100))
        )

        # Setup figure
        fig = plt.figure(figsize=(10.2, 10), dpi=96)
        gspec = fig.add_gridspec(2, 6)
        iteration_axis = fig.add_subplot(gspec[0, :5])
        iteration_axis.set_title(
            "Iteration results of row to necessary to extrapolate."
        )
        iteration_axis.set_xlabel("Row number of values to interpolate.")
        iteration_axis.set_ylabel("Original and extrapolated y-values")
        # Plot
        original_for_history = original_values.copy()
        original_for_history.index = pandas.Index(
            numpy.arange(1, len(original_values) + 1)
        )
        for index, (label, original_curve) in enumerate(
            original_for_history.iteritems()
        ):
            iteration_axis.plot(
                original_curve,
                "P",
                color=color_pairs[index][1],
                markersize=7,
                label="original {}".format(index),
            )

        for index, (label, iterated_values) in enumerate(iteration_history.iteritems()):
            iteration_axis.plot(
                iterated_values,
                "o",
                color=color_pairs[index][0],
                markersize=3,
                label="extrapolated {}".format(index),
            )
        iteration_axis.plot(iteration_mean_curve, "ks", markersize=5, label="mean")
        iteration_axis.grid(b=True, which="major", axis="x")

        result_axis = fig.add_subplot(gspec[1, :5])
        result_axis.set_title("Original and extrapolated curves.")
        result_axis.set_xlabel("x-values")
        result_axis.set_ylabel("Original and extrapolated y-values")
        result_axis.plot(*a_mean_point, "r+", markersize=20, label="arith. end point")
        for index, (label, curve) in enumerate(original_values.iteritems()):
            current_label = "original {}".format(index)
            color = color_pairs[index][1]
            result_axis.plot(
                curve, marker="o", color=color, markersize=3, label=current_label
            )

        for index, (label, curve) in enumerate(extrapolated_curves.iteritems()):
            current_label = "extraploated {}".format(index)
            color = color_pairs[index][0]
            result_axis.plot(
                curve, ":P", color=color, markersize=5, label=current_label
            )

        result_axis.plot(complete_mean_curve, "--ks", markersize=5, label="mean")

        # Finishing touch
        iteration_axis.legend(loc="upper left", bbox_to_anchor=(1.02, 1.02))
        result_axis.legend(loc="upper left", bbox_to_anchor=(1.02, 1.02))
        plt.show()


if __name__ == "__main__":
    import doctest

    doctest.testmod()