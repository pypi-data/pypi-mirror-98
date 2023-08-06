# -----------------------------------------------------------------------------
# Description:    Plot interpolations.
# Repository:     https://gitlab.com/quantify-os/quantify-core
# Copyright (C) Qblox BV & Orange Quantum Systems Holding BV (2020-2021)
# -----------------------------------------------------------------------------
import logging
import numpy as np
from typing_extensions import Literal
from scipy import interpolate


def areas(ip):
    p = ip.tri.points[ip.tri.vertices]
    q = p[:, :-1, :] - p[:, -1, None, :]
    areas = abs(q[:, 0, 0] * q[:, 1, 1] - q[:, 0, 1] * q[:, 1, 0]) / 2
    return areas


def scale(points, xy_mean, xy_scale):
    points = np.asarray(points, dtype=float)
    return (points - xy_mean) / xy_scale


def unscale(points, xy_mean, xy_scale):
    points = np.asarray(points, dtype=float)
    return points * xy_scale + xy_mean


def interpolate_heatmap(
    x,
    y,
    z,
    n: int = None,
    interp_method: Literal["linear", "nearest", "deg"] = "linear",
):
    """
    The output of this method can directly be used for plt.imshow(z_grid, extent=extent, aspect='auto')
    where the extent is determined by the min and max of the x_grid and y_grid.

    The output can also be used as input for ax.pcolormesh(x, y, Z,**kw)

    Parameters
    ----------
    x : :class:`numpy.ndarray`
        x data points
    y : :class:`numpy.ndarray`
        y data points
    z : :class:`numpy.ndarray`
        z data points
    n
        number of points for each dimension on the interpolated grid if set to None will auto determine amount of
        points needed
    interp_method
        determines what interpolation method is used.
    Returns
    -------
    x_grid : :class:`numpy.ndarray`
        N*1 array of x-values of the interpolated grid
    y_grid : :class:`numpy.ndarray`
        N*1 array of x-values of the interpolated grid
    z_grid : :class:`numpy.ndarray`
        N*N array of z-values that form a grid.
    """

    points = list(zip(x, y))
    lbrt = np.min(points, axis=0), np.max(points, axis=0)
    lbrt = lbrt[0][0], lbrt[0][1], lbrt[1][0], lbrt[1][1]

    xy_mean = np.mean([lbrt[0], lbrt[2]]), np.mean([lbrt[1], lbrt[3]])
    xy_scale = np.ptp([lbrt[0], lbrt[2]]), np.ptp([lbrt[1], lbrt[3]])

    # interpolation needs to happen on a rescaled grid, this is somewhat akin
    # to an assumption in the interpolation that the scale of the experiment
    # is chosen sensibly. N.B. even if interp_method == "nearest" the linear
    # interpolation is used to determine the amount of grid points.
    ip = interpolate.LinearNDInterpolator(
        scale(points, xy_mean=xy_mean, xy_scale=xy_scale), z
    )

    if n is None:
        # Calculate how many grid points are needed.
        # factor from A=√3/4 * a² (equilateral triangle)
        # N.B. a factor 4 was added as there were to few points for uniform grid otherwise.
        all_areas = areas(ip)
        area_min = all_areas[all_areas > 0.0].min()
        n = int(0.658 / np.sqrt(area_min)) * 4
        n = max(n, 10)
        if n > 500:
            logging.debug("n: {} larger than 500".format(n))
            n = 500

    x_lin = y_lin = np.linspace(-0.5, 0.5, n)

    if interp_method == "linear":
        z_grid = ip(x_lin[:, None], y_lin[None, :]).squeeze()
    elif interp_method == "nearest":
        ip = interpolate.NearestNDInterpolator(
            scale(points, xy_mean=xy_mean, xy_scale=xy_scale), z
        )
        z_grid = ip(x_lin[:, None], y_lin[None, :]).squeeze()
    elif interp_method == "deg":
        # Circular interpolation in deg units
        phases = np.deg2rad(z)
        newdata_cos = np.cos(phases)
        newdata_sin = np.sin(phases)

        ip_cos = interpolate.LinearNDInterpolator(
            scale(points, xy_mean=xy_mean, xy_scale=xy_scale), newdata_cos
        )
        newdata_cos = ip_cos(x_lin[:, None], y_lin[None, :]).squeeze()

        ip_sin = interpolate.LinearNDInterpolator(
            scale(points, xy_mean=xy_mean, xy_scale=xy_scale), newdata_sin
        )
        newdata_sin = ip_sin(x_lin[:, None], y_lin[None, :]).squeeze()

        z_grid = (np.rad2deg(np.arctan2(newdata_sin, newdata_cos)) % 360).squeeze()
    else:
        raise ValueError("interp_method must be one of {'linear', 'nearest', 'deg'}")

    # x and y grid points need to be rescaled from the linearly chosen points
    points_grid = unscale(list(zip(x_lin, y_lin)), xy_mean=xy_mean, xy_scale=xy_scale)
    x_grid = points_grid[:, 0]
    y_grid = points_grid[:, 1]

    return x_grid, y_grid, z_grid.T
