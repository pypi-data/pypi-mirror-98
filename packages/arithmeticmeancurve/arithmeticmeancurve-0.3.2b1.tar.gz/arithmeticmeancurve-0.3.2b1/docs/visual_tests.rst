***************************
Tests on Families of Curves
***************************

Except *NonLinear0* all families of curves shown below were chosen as they triggered
logical bugs within the code of prior releases.

NonLinear0
==========

This family of curve is an exemplary family of curve which was created as the first
test case for the first alpha release. The curves end points are **not** generated
using a standard deviation.

No offsets
----------

.. plot::

    test_family_name = "NonLinear0"
    import examplecurves
    from arithmeticmeancurve import MeanCurvePlotter
    sample_curves = examplecurves.Static.create(family_name=test_family_name)
    MeanCurvePlotter.test_plot(
        sample_curves,
        upper_title="Family of curves {}".format(test_family_name),
        lower_title="Focus on end points. X, Y distances may be distorted."
    )

Offsets 0
---------

.. plot::

    test_family_name = "NonLinear0"
    import examplecurves
    from arithmeticmeancurve import MeanCurvePlotter
    sample_curves = examplecurves.Static.create(
        family_name=test_family_name, predefined_offset=0
    )
    MeanCurvePlotter.test_plot(
        sample_curves,
        upper_title="Family of curves {}".format(test_family_name),
        lower_title="Focus on end points. X, Y distances may be distorted."
    )

Offsets 1
---------

.. plot::

    test_family_name = "NonLinear0"
    import examplecurves
    from arithmeticmeancurve import MeanCurvePlotter
    sample_curves = examplecurves.Static.create(
        family_name=test_family_name, predefined_offset=1
    )
    MeanCurvePlotter.test_plot(
        sample_curves,
        upper_title="Family of curves {}".format(test_family_name),
        lower_title="Focus on end points. X, Y distances may be distorted."
    )


HorizontalLinear
================

End points of all families of curves within the group of *horizontal linear*
bases on a simple strength failure criterion. Slope (Young's modulus) and y-values
(strength) are randomly generated using a standard deviation. The x-values are
calculated on basis of the generated values.

The calculation leads to horizontally aligned end points, which gives this
group its name.

Variation 0
-----------

.. plot::

    test_family_name = "HorizontalLinear0"
    import examplecurves
    from arithmeticmeancurve import MeanCurvePlotter
    sample_curves = examplecurves.Static.create(family_name=test_family_name)
    MeanCurvePlotter.test_plot(
        sample_curves,
        upper_title="Family of curves {}".format(test_family_name),
        lower_title="Focus on end points. X, Y distances may be distorted."
    )


Variation 1
-----------

.. plot::

    test_family_name = "HorizontalLinear1"
    import examplecurves
    from arithmeticmeancurve import MeanCurvePlotter
    sample_curves = examplecurves.Static.create(family_name=test_family_name)
    MeanCurvePlotter.test_plot(
        sample_curves,
        upper_title="Family of curves {}".format(test_family_name),
        lower_title="Focus on end points. X, Y distances may be distorted."
    )


Variation 2
-----------

.. plot::

    test_family_name = "HorizontalLinear2"
    import examplecurves
    from arithmeticmeancurve import MeanCurvePlotter
    sample_curves = examplecurves.Static.create(family_name=test_family_name)
    MeanCurvePlotter.test_plot(
        sample_curves,
        upper_title="Family of curves {}".format(test_family_name),
        lower_title="Focus on end points. X, Y distances may be distorted."
    )


Variation 3
-----------

.. plot::

    test_family_name = "HorizontalLinear3"
    import examplecurves
    from arithmeticmeancurve import MeanCurvePlotter
    sample_curves = examplecurves.Static.create(family_name=test_family_name)
    MeanCurvePlotter.test_plot(
        sample_curves,
        upper_title="Family of curves {}".format(test_family_name),
        lower_title="Focus on end points. X, Y distances may be distorted."
    )

DiagonalLinear
==============

End points of all families of curves within the group of *diagonal linear*
bases on a simple energy failure criterion. Slope (Young's modulus) and area
beneath the x-y curve (energy) are randomly generated using a standard deviation.
The x-values and y-values are calculated on basis of the generated values.

The calculation leads to diagonally aligned end points, which gives this
group its name.

Variation 0
-----------

.. plot::

    test_family_name = "DiagonalLinear0"
    import examplecurves
    from arithmeticmeancurve import MeanCurvePlotter
    sample_curves = examplecurves.Static.create(family_name=test_family_name)
    MeanCurvePlotter.test_plot(
        sample_curves,
        upper_title="Family of curves {}".format(test_family_name),
        lower_title="Focus on end points. X, Y distances may be distorted."
    )


Variation 1
-----------

.. plot::

    test_family_name = "DiagonalLinear1"
    import examplecurves
    from arithmeticmeancurve import MeanCurvePlotter
    sample_curves = examplecurves.Static.create(family_name=test_family_name)
    MeanCurvePlotter.test_plot(
        sample_curves,
        upper_title="Family of curves {}".format(test_family_name),
        lower_title="Focus on end points. X, Y distances may be distorted."
    )


Variation 2
-----------

.. plot::

    test_family_name = "DiagonalLinear2"
    import examplecurves
    from arithmeticmeancurve import MeanCurvePlotter
    sample_curves = examplecurves.Static.create(family_name=test_family_name)
    MeanCurvePlotter.test_plot(
        sample_curves,
        upper_title="Family of curves {}".format(test_family_name),
        lower_title="Focus on end points. X, Y distances may be distorted."
    )


Variation 3
-----------

.. plot::

    test_family_name = "DiagonalLinear3"
    import examplecurves
    from arithmeticmeancurve import MeanCurvePlotter
    sample_curves = examplecurves.Static.create(family_name=test_family_name)
    MeanCurvePlotter.test_plot(
        sample_curves,
        upper_title="Family of curves {}".format(test_family_name),
        lower_title="Focus on end points. X, Y distances may be distorted."
    )

VerticalLinear
==============

End points of all families of curves within the group of *vertical linear*
bases on a simple strain failure criterion. Slope (Young's modulus) and x-values
(strain) are randomly generated using a standard deviation.
The y-values are calculated on basis of the generated values.

The calculation leads to vertically aligned end points, which gives this
group its name.

Variation 0
-----------

The arithmetic y-mean value of the ending points is located in between the last
full value row and the ending part of the family of curves, which needs extrapolation.

.. plot::

    test_family_name = "VerticalLinear0"
    import examplecurves
    from arithmeticmeancurve import MeanCurvePlotter
    sample_curves = examplecurves.Static.create(family_name=test_family_name)
    MeanCurvePlotter.test_plot(
        sample_curves,
        upper_title="Family of curves {}".format(test_family_name),
        lower_title="Focus on end points. X, Y distances may be distorted."
    )


Variation 1
-----------

.. plot::

    test_family_name = "VerticalLinear1"
    import examplecurves
    from arithmeticmeancurve import MeanCurvePlotter
    sample_curves = examplecurves.Static.create(family_name=test_family_name)
    MeanCurvePlotter.test_plot(
        sample_curves,
        upper_title="Family of curves {}".format(test_family_name),
        lower_title="Focus on end points. X, Y distances may be distorted."
    )


Variation 2
-----------

.. plot::

    test_family_name = "VerticalLinear2"
    import examplecurves
    from arithmeticmeancurve import MeanCurvePlotter
    sample_curves = examplecurves.Static.create(family_name=test_family_name)
    MeanCurvePlotter.test_plot(
        sample_curves,
        upper_title="Family of curves {}".format(test_family_name),
        lower_title="Focus on end points. X, Y distances may be distorted."
    )


Variation 3
-----------

.. plot::

    test_family_name = "VerticalLinear3"
    import examplecurves
    from arithmeticmeancurve import MeanCurvePlotter
    sample_curves = examplecurves.Static.create(family_name=test_family_name)
    MeanCurvePlotter.test_plot(
        sample_curves,
        upper_title="Family of curves {}".format(test_family_name),
        lower_title="Focus on end points. X, Y distances may be distorted."
    )