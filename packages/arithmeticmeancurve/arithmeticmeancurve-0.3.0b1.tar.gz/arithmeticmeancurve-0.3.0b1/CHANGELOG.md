# Changelog
This changelog is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.3.0b1] - 2021-03-11 
### Added
- setup.cfg, .coveragerc, tox.ini, .travis.yml
- new test-file test_mean_curve_calculation.py
- Added new tests

### Changed
- Development status from *alpha* to *beta*
- README.md
- Code maintenance in arithmeticmeancurve.py
- Updated requirements.txt
- Changed setuptools layout from setup.py to setup.cfg
- Changed plain text GPLv3 to markdown version
- Maintained existing tests

### Removed
- dependency from *dicthandling*

## [0.2a9] - 2021-01-13
### Fixed
- Fixed doctests.

### Added
- Text and additional plots to the chapter *A look inside the extrapolation* within
  the documentation.

### Changed
- Executing `python -m arithmeticmeancurve` triggers a doctest.

## [0.2a8] - 2021-01-12
### Fixed
- Fixed of rare occurrence of mean curve being not cut correctly at the target
  arithmetic ending value.

### Added
- Possibility to set a predefined *Extrapolates*-Object as the extrapolation method
  within an *ArithmeticMeanCurve*.

## [0.2a7] - 2021-01-08
### Fixed
- Fixed rare occurrence of searched y-value leading to exception.

### Removed
- outsourced function to *meld_along_columns* of
  [trashpanda](https://gitlab.com/david.scheliga/trashpanda)

## [0.2a6] - 2021-01-07
### Fixed
- Package dependencies for pip installation.
- Duplicated indexes within curves lead to an exception raised by pandas.
  Now only first duplicates are kept.

## [0.2a5] - 2021-01-05
### Fixed
- Bug within documentation due to usage of removed version attribute.

### Added
- Section within documentation showing results of test cases. 
- Abstract class *Extrapolates* defining an extrapolation interface for testing.
- *MeanCurvePlotter* providing 3 plotting methods related to mean curves.
- *ExtrapolationIterationTester* to achieve deeper insight into iterations in
  combination with doctests.
- Arithmetic end point into default plot.

### Changed
- Reworked the arithmetic mean curve calculation.
- Enable testing within a deeper level of the curve extrapolation.
- *ArithmeticMeanCurve* forwards the extrapolation behavior.
- *FamilyOfCurveStatistics*.__repr__ prints a table of mean and standard
  deviation values.

### Fixed
- Bug in *_find_positions_in_between* which lead to wrong positions
  in case of *examplecurves.Static.create("VerticalLinear1")*.

### Removed
- Removed deprecated functions *_all_ndarrays_have_equal_column_count*, 
  *_all_dataframes_have_equal_column_count*, *_ndarray_has_monotonic_increasing_x*,
  *_dataframe_has_monotonic_increasing_x*, *_dataframes_are_valid_for_calculation*,
  *_ndarrays_are_valid_for_calculation*, *_input_curves_are_valid_for_calculation*
- Removed deprecated methods *FamilyOfCurveStatistics.extract_end_points_from_family*

## [0.1a1] - 2020-12-17
### Fixed
- Bug resulting in missing mean curve values, if the mean value of the ending abscissa
  values (x-values) was less then the *end cap or end section*.

### Changed
- Versioning via setuptools purely by git tags.
- *examplecurves>=0.2a1* are required.

## [0.1a0] - 2020-12-06
### Added
- Class *VisualIterationTester* for calculating and plotting the iterations
  during the extrapolation process of the mean curve calculation.

### Changed
- Outsourced *examplecurves* into an individual module at 
  http://gitlab.com/david.scheliga/examplecurves
- Fixed documentation in regard of the outsourced *examplecurves* module

### Removed
- Unintentional private method in arithmeticmeancurves.\_\_all\_\_
- Module *examplecurves* from setup.py.

## [0.0a1.post3] - 2020-12-03
### Added
- Basic usage to README.md and the sphinx documentation

### Fixed
- Minor wrong definitions within README.md
- Wrong compilation of basic_usage.rst at readthedocs.org

## [0.0a1] - 2020-12-02
- First code release of arithmeticmeancurve