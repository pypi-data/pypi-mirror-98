import examplecurves
from arithmeticmeancurve import FrozenStdExtrapolation, ArithmeticMeanCurve
import copy

_current_curves = examplecurves.Static.create("horizontallinear0")


def calculate_frozen_std_mean_curve():
    """
    >>> extrapolating_mean_curve = calculate_frozen_std_mean_curve()
    >>> from trashpanda import meld_along_columns
    >>> from pandas import DataFrame
    >>> from doctestprinter import print_pandas
    >>> mean_curve = DataFrame(extrapolating_mean_curve.mean_curve, columns=["mean"])
    >>> print_pandas(
    ...     meld_along_columns(extrapolating_mean_curve.family_of_curves, mean_curve),
    ...     formats="{:>.2f}#{:>.4f}"
    ... )
              y_0      y_1      y_2      y_3     y_4     mean
    x
    0.00   0.0000   0.0000   0.0000   0.0000  0.0000   0.0000
    0.24   2.3749   2.3788   2.3869   2.3675  2.4997   2.4016
    0.25   2.4882   2.4924   2.5009   2.4805  2.6190   2.5162
    0.26   2.4998   2.5039   2.5124   2.4920  2.6311   2.5278
    0.26   2.5047   2.5088   2.5174   2.4969  2.6362   2.5328
    0.26   2.5188   2.5229   2.5315   2.5110  2.6511   2.5471
    0.48   4.7498   4.7577   4.7739   4.7351  4.9993   4.8032
    0.51   4.9765   4.9847   5.0017   4.9611  5.2379   5.0324
    0.51   4.9995   5.0078   5.0249   4.9840  5.2622   5.0557
    0.51   5.0093   5.0176   5.0347   4.9938  5.2725   5.0656
    0.51   5.0375   5.0459   5.0631   5.0219  5.3022   5.0941
    0.73   7.1247   7.1365   7.1608   7.1026  7.4990   7.2047
    0.76   7.4647   7.4771   7.5026   7.4416  7.8569   7.5486
    0.77   7.4993   7.5117   7.5373   7.4761  7.8933   7.5835
    0.77   7.5140   7.5264   7.5521   7.4907  7.9087   7.5984
    0.77   7.5563   7.5688   7.5946   7.5329  7.9533   7.6412
    0.97   9.4996   9.5153   9.5478   9.4702  9.9987   9.6063
    1.01      nan      nan      nan      nan     nan  10.0160
    1.02   9.9529   9.9694  10.0034   9.9221     nan      nan
    1.02   9.9991  10.0156      nan   9.9681     nan      nan
    1.02  10.0186      nan      nan   9.9876     nan      nan
    1.03      nan      nan      nan  10.0439     nan      nan
    >>> round(extrapolating_mean_curve.statistics.end_x_mean, 4)
    1.0111
    >>> round(extrapolating_mean_curve.statistics.end_y_mean, 4)
    10.016
    >>> round(extrapolating_mean_curve.statistics.end_x_std, 4)
    0.0238
    >>> round(extrapolating_mean_curve.statistics.end_y_std, 4)
    0.0176
    """
    sample_curves = copy.copy(_current_curves)
    a_mean_curve = ArithmeticMeanCurve(sample_curves)
    return a_mean_curve


def extrapolate_end_cap():
    """

    >>> end_cap_mean_values = extrapolate_end_cap()
    >>> from doctestprinter import doctest_iter_print
    >>> doctest_iter_print(end_cap_mean_values, edits_item=lambda x: x.to_numpy())
    x = 1.0155758653529496:
      [ 9.95294354  9.96941122 10.00341993  9.92212445 10.45171057]
    x = 1.0202814839730938:
      [ 9.99905999 10.01560397 10.04581469  9.96809811 10.49671911]
    x = 1.022278673972714:
      [10.01863305 10.03197692 10.06443658  9.98761055 10.515341  ]
    x = 1.0280393839395214:
      [10.06840729 10.08412489 10.11658455 10.04389239 10.56748897]

    """
    sample_curves = copy.copy(_current_curves)
    a_mean_curve = ArithmeticMeanCurve(sample_curves)
    extrapolates = FrozenStdExtrapolation()
    extrapolates.prepare_extrapolation(a_mean_curve)

    end_cap = a_mean_curve.get_end_cap()
    extrapolations = {}
    for x_value, y_values in end_cap.iterrows():
        item_result = extrapolates(y_values)
        extrapolations["x = {}".format(x_value)] = item_result
    return extrapolations


def extrapolate_iterate_rows():
    """

    >>> histories = extrapolate_iterate_rows()
    >>> from doctestprinter import doctest_iter_print
    >>> for x_representation, item_history in histories.items():
    ...     print(x_representation)
    ...     doctest_iter_print(item_history, indent="  ")
    x = 1.0155758653529496
      [ 9.95294354  9.96941122 10.00341993  9.92212445  9.99868185]
      [ 9.95294354  9.96941122 10.00341993  9.92212445 10.36168563]
      [ 9.95294354  9.96941122 10.00341993  9.92212445 10.43428638]
      [ 9.95294354  9.96941122 10.00341993  9.92212445 10.44880653]
      [ 9.95294354  9.96941122 10.00341993  9.92212445 10.45171057]
    x = 1.0202814839730938
      [ 9.99905999 10.01560397 10.00080615  9.96809811 10.45171057]
      [ 9.99905999 10.01560397 10.02852077  9.96809811 10.47942519]
      [ 9.99905999 10.01560397 10.03960662  9.96809811 10.49051104]
      [ 9.99905999 10.01560397 10.04404096  9.96809811 10.49494538]
      [ 9.99905999 10.01560397 10.04581469  9.96809811 10.49671911]
    x = 1.022278673972714
      [10.01863305 10.01335504 10.04581469  9.98761055 10.49671911]
      [10.01863305 10.02143184 10.0538915   9.98761055 10.50479592]
      [10.01863305 10.02627793 10.05873758  9.98761055 10.509642  ]
      [10.01863305 10.02918558 10.06164523  9.98761055 10.51254965]
      [10.01863305 10.03093017 10.06338983  9.98761055 10.51429424]
      [10.01863305 10.03197692 10.06443658  9.98761055 10.515341  ]
    x = 1.0280393839395214
      [10.01625933 10.03197692 10.06443658 10.04389239 10.515341  ]
      [10.027669   10.0433866  10.07584626 10.04389239 10.52675068]
      [10.03679675 10.05251434 10.084974   10.04389239 10.53587842]
      [10.04409894 10.05981654 10.09227619 10.04389239 10.54318061]
      [10.04994069 10.06565829 10.09811795 10.04389239 10.54902237]
      [10.0546141  10.07033169 10.10279135 10.04389239 10.55369577]
      [10.05835282 10.07407042 10.10653007 10.04389239 10.55743449]
      [10.0613438  10.0770614  10.10952105 10.04389239 10.56042547]
      [10.06373658 10.07945418 10.11191383 10.04389239 10.56281825]
      [10.06565081 10.0813684  10.11382806 10.04389239 10.56473248]
      [10.06718219 10.08289979 10.11535944 10.04389239 10.56626386]
      [10.06840729 10.08412489 10.11658455 10.04389239 10.56748897]

    """
    sample_curves = copy.copy(_current_curves)
    a_mean_curve = ArithmeticMeanCurve(sample_curves)
    extrapolates = FrozenStdExtrapolation()
    extrapolates.prepare_extrapolation(a_mean_curve)

    end_cap = a_mean_curve.get_end_cap()
    histories = {}
    for x_value, y_values in end_cap.iterrows():
        iteration_history = [
            item.to_numpy() for item in extrapolates.iter_extrapolate_row(y_values)
        ]
        histories["x = {}".format(x_value)] = iteration_history
    return histories