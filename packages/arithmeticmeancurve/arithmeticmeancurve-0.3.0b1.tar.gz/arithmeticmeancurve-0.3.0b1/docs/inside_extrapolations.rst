*******************************
A look inside the extrapolation
*******************************

Frozen standard deviation extrapolation
=======================================

The *frozen standard deviation extrapolation* supports 3 parameters.
*use_previous_iteration*, *target_threshold* and *maximum_allowed_iterations*

maximum_allowed_iterations
--------------------------

Defines the maximum allowed iterations for each row of values. Default is 50.

target_threshold
----------------

The parameter *target_threshold* (default 0.0001) defines the stopping condition for the
iterative extrapolation. It is the relative deviation of the current arithmetic mean
value towards the previous calculated mean value during the extrapolation.

The *target_threshold* has direct impact on the performed iterations
(see `figure 1`_ and `figure 2`_). *target_threshold* is accompanied with
*maximum_allowed_iterations* as it might be necessary to increase
*maximum_allowed_iterations* for small *target_threshold*.

.. _figure 1:

.. plot::

    import examplecurves
    from arithmeticmeancurve import (
        ArithmeticMeanCurve, FrozenStdExtrapolation, VisualIterationTester
    )

    sample_curves = examplecurves.Static.create(family_name="horizontallinear1")
    extrapolates = FrozenStdExtrapolation(target_threshold=0.001)
    VisualIterationTester.plot_extrapolation_test(
        curves=sample_curves,
        extrapolates=extrapolates
    )

**Figure 1**: Iteration using *FrozenStdExtrapolation* with a *target threshold* of 0.001.


.. _figure 2:

.. plot::

    import examplecurves
    from arithmeticmeancurve import (
        ArithmeticMeanCurve, FrozenStdExtrapolation, VisualIterationTester
    )

    sample_curves = examplecurves.Static.create(family_name="horizontallinear1")
    extrapolates = FrozenStdExtrapolation(target_threshold=0.0001)
    VisualIterationTester.plot_extrapolation_test(
        curves=sample_curves,
        extrapolates=extrapolates
    )

**Figure 2**: Iteration using *FrozenStdExtrapolation* with a *target threshold* of 0.0001.


use_previous_iteration
----------------------

By default *FrozenStdExtrapolation* uses the previous iteration result as the starting
point for the next one to speed up the calculation.

.. plot::

    import examplecurves
    from arithmeticmeancurve import (
        ArithmeticMeanCurve, FrozenStdExtrapolation, VisualIterationTester
    )

    sample_curves = examplecurves.Static.create(family_name="nonlinear0")
    extrapolates = FrozenStdExtrapolation(use_previous_iteration=False)
    VisualIterationTester.plot_extrapolation_test(
        curves=sample_curves,
        extrapolates=extrapolates
    )

**Figure 3**: Iteration with *use_previous_iteration* disabled.


.. plot::

    import examplecurves
    from arithmeticmeancurve import (
        ArithmeticMeanCurve, FrozenStdExtrapolation, VisualIterationTester
    )

    sample_curves = examplecurves.Static.create(family_name="nonlinear0")
    extrapolates = FrozenStdExtrapolation(use_previous_iteration=True)
    VisualIterationTester.plot_extrapolation_test(
        curves=sample_curves,
        extrapolates=extrapolates
    )

**Figure 3**: Default extrapolation using previous iteration results and a target
threshold of 0.0001.