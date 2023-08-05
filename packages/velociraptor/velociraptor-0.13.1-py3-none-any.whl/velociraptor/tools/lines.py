"""
Tools to generate various lines from datasets.
"""

import unyt
import numpy as np

from typing import List


def binned_mean_line(
    x: unyt.unyt_array,
    y: unyt.unyt_array,
    x_bins: unyt.unyt_array,
    minimum_in_bin: int = 3,
    return_additional: bool = False,
):
    """
    Gets a mean (y) line, binned in the x direction.

    Parameters
    ----------

    x: unyt.unyt_array
        Horizontal values, to be binned.

    y: unyt.unyt_array
        Vertical values, to have the mean calculated in the x-bins

    x_bins: unyt.unyt_array
        Horizontal bin edges. Must have the same units as x.

    minimum_in_bin: int, optional
        Minimum number of items in a bin to return that bin. If a bin has
        fewer values than this, it is excluded from the return values.
        Default: 3.

    return_additional: bool, optional
        Boolean. If true, makes the function return x and y data points that
        lie in the bins where the number of data points is smaller than
        minimum_in_bin, and any points that are higher than the highest bin
        edge. Default: false.


    Returns
    -------

    bin_centers: unyt.unyt_array
        The centers of the bins (taken to be the linear mean of the bin edges).

    means: unyt.unyt_array
        Vertical mean values within the bins.

    standard_deviation: unyt.unyt_array
        Standard deviation within the bins, to be shown as scatter.

    additional_x: unyt.unyt_array, optional
        x data points from the bins where the number of data points is smaller
        than minimum_in_bin

    additional_y: unyt.unyt_array, optional
        y data points from the bins where the number of data points is smaller
        than minimum_in_bin


    Notes
    -----

    The return types are such that you can pass this directly to `plt.errorbar`,
    as follows:

    .. code-block:: python

        plt.errorbar(
            *binned_mean_line(x, y, x_bins, 10)
        )

    """

    assert (
        x.units == x_bins.units
    ), "Please ensure that the x values and bins have the same units."

    hist = np.digitize(x, x_bins)

    means = []
    standard_deviations = []
    centers = []
    additional_x = []
    additional_y = []

    for bin in range(1, len(x_bins)):
        indicies_in_this_bin = hist == bin
        number_of_items_in_bin = indicies_in_this_bin.sum()

        if number_of_items_in_bin >= minimum_in_bin:
            y_values_in_this_bin = y[indicies_in_this_bin].value

            means.append(np.mean(y_values_in_this_bin))
            standard_deviations.append(np.std(y_values_in_this_bin))

            # Bin center is computed as the median of the X values of the data points
            # in the bin
            centers.append(np.median(x[indicies_in_this_bin].value))

        # If the number of data points in the bin is less than minimum_in_bin,
        # collect these data points if needed
        elif number_of_items_in_bin > 0 and return_additional:
            additional_x += list(x[indicies_in_this_bin].value)
            additional_y += list(y[indicies_in_this_bin].value)

    # Add any points that are larger:
    above_highest = hist == len(x_bins)
    additional_x += list(x[above_highest].value)
    additional_y += list(y[above_highest].value)

    means = unyt.unyt_array(means, units=y.units, name=y.name)
    standard_deviations = unyt.unyt_array(
        standard_deviations, units=y.units, name=f"{y.name} ($sigma$)"
    )
    centers = unyt.unyt_array(centers, units=x.units, name=x.name)
    additional_x = unyt.unyt_array(additional_x, units=x.units, name=x.name)
    additional_y = unyt.unyt_array(additional_y, units=y.units, name=y.name)

    if not return_additional:
        return centers, means, standard_deviations
    else:
        return centers, means, standard_deviations, additional_x, additional_y


def binned_median_line(
    x: unyt.unyt_array,
    y: unyt.unyt_array,
    x_bins: unyt.unyt_array,
    percentiles: List[int] = [16, 84],
    minimum_in_bin: int = 3,
    return_additional: bool = False,
):
    """
    Gets a median (y) line, binned in the x direction.

    Parameters
    ----------

    x: unyt.unyt_array
        Horizontal values, to be binned.

    y: unyt.unyt_array
        Vertical values, to have the median calculated in the x-bins

    x_bins: unyt.unyt_array
        Horizontal bin edges. Must have the same units as x.

    percentiles: List[int], optional
        Percentiles to return as the positive and negative errors. By
        default these are 16 and 84th percentiles.

    minimum_in_bin: int, optional
        Minimum number of items in a bin to return that bin. If a bin has
        fewer values than this, it is excluded from the return values.
        Default: 3.

    return_additional: bool, optional
        Boolean. If true, makes the function return x and y data points that
        lie in the bins where the number of data points is smaller than
        minimum_in_bin, and any points that are higher than the highest bin
        edge. Default: false.



    Returns
    -------

    bin_centers: unyt.unyt_array
        The centers of the bins (taken to be the linear mean of the bin edges).

    medians: unyt.unyt_array
        Vertical median values within the bins.

    deviations: unyt.unyt_array
        Deviation from median vertically using the ``percentiles`` defined above.
        This has shape 2xN.

    additional_x: unyt.unyt_array, optional
        x data points from the bins where the number of data points is smaller
        than minimum_in_bin

    additional_y: unyt.unyt_array, optional
        y data points from the bins where the number of data points is smaller
        than minimum_in_bin


    Notes
    -----

    The return types are such that you can pass this directly to `plt.errorbar`,
    as follows:

    .. code-block:: python

        plt.errorbar(
            *binned_median_line(x, y, x_bins, 10)
        )

    """

    assert (
        x.units == x_bins.units
    ), "Please ensure that the x values and bins have the same units."

    hist = np.digitize(x, x_bins)

    medians = []
    deviations = []
    centers = []
    additional_x = []
    additional_y = []

    for bin in range(1, len(x_bins)):
        indicies_in_this_bin = hist == bin
        number_of_items_in_bin = indicies_in_this_bin.sum()

        if number_of_items_in_bin >= minimum_in_bin:
            y_values_in_this_bin = y[indicies_in_this_bin].value

            medians.append(np.median(y_values_in_this_bin))
            deviations.append(np.percentile(y_values_in_this_bin, percentiles))

            # Bin center is computed as the median of the X values of the data points
            # in the bin
            centers.append(np.median(x[indicies_in_this_bin].value))

        # If the number of data points in the bin is less than minimum_in_bin,
        # collect these data points if needed
        elif number_of_items_in_bin > 0 and return_additional:
            additional_x += list(x[indicies_in_this_bin].value)
            additional_y += list(y[indicies_in_this_bin].value)

    # Add any points that are larger:
    above_highest = hist == len(x_bins)
    additional_x += list(x[above_highest].value)
    additional_y += list(y[above_highest].value)

    medians = unyt.unyt_array(medians, units=y.units, name=y.name)
    # Percentiles actually gives us the values - we want to be able to use
    # matplotlib's errorbar function
    deviations = unyt.unyt_array(
        abs(np.array(deviations).T - medians.value),
        units=y.units,
        name=f"{y.name} {percentiles} percentiles",
    )
    centers = unyt.unyt_array(centers, units=x.units, name=x.name)
    additional_x = unyt.unyt_array(additional_x, units=x.units, name=x.name)
    additional_y = unyt.unyt_array(additional_y, units=y.units, name=y.name)

    if not return_additional:
        return centers, medians, deviations
    else:
        return centers, medians, deviations, additional_x, additional_y
