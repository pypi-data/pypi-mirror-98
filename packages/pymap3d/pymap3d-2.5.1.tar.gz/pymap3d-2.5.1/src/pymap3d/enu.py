""" transforms involving ENU East North Up """
from __future__ import annotations
import typing

try:
    from numpy import radians, sin, cos, hypot, arctan2 as atan2, degrees, pi, vectorize, ndarray
except ImportError:
    from math import radians, sin, cos, hypot, atan2, degrees, pi  # type: ignore

    vectorize = None
    ndarray = typing.Any  # type: ignore

from .ecef import geodetic2ecef, ecef2geodetic, enu2ecef, uvw2enu
from .ellipsoid import Ellipsoid

# py < 3.6 compatible
tau = 2 * pi

__all__ = ["enu2aer", "aer2enu", "enu2geodetic", "geodetic2enu"]


def enu2aer(
    e: float | ndarray, n: float | ndarray, u: float | ndarray, deg: bool = True
) -> tuple[float, float, float]:
    """
    ENU to Azimuth, Elevation, Range

    Parameters
    ----------

    e : float
        ENU East coordinate (meters)
    n : float
        ENU North coordinate (meters)
    u : float
        ENU Up coordinate (meters)
    deg : bool, optional
        degrees input/output  (False: radians in/out)

    Results
    -------

    azimuth : float
        azimuth to rarget
    elevation : float
        elevation to target
    srange : float
        slant range [meters]
    """

    if vectorize is not None:
        fun = vectorize(enu2aer_point)
        az, el, rng = fun(e, n, u, deg)
        return az[()], el[()], rng[()]
    else:
        return enu2aer_point(e, n, u, deg)


def enu2aer_point(
    e: float | ndarray, n: float | ndarray, u: float | ndarray, deg: bool = True
) -> tuple[float, float, float]:

    # 1 millimeter precision for singularity

    if abs(e) < 1e-3:
        e = 0.0
    if abs(n) < 1e-3:
        n = 0.0
    if abs(u) < 1e-3:
        u = 0.0

    r = hypot(e, n)
    slantRange = hypot(r, u)
    elev = atan2(u, r)
    az = atan2(e, n) % tau

    if deg:
        az = degrees(az)
        elev = degrees(elev)

    return az, elev, slantRange


def aer2enu(az: float, el: float, srange: float, deg: bool = True) -> tuple[float, float, float]:
    if vectorize is not None:
        fun = vectorize(aer2enu_point)
        e, n, u = fun(az, el, srange, deg)
        return e[()], n[()], u[()]
    else:
        return aer2enu_point(az, el, srange, deg)


def aer2enu_point(
    az: float, el: float, srange: float, deg: bool = True
) -> tuple[float, float, float]:
    """
    Azimuth, Elevation, Slant range to target to East, North, Up

    Parameters
    ----------
    azimuth : float
            azimuth clockwise from north (degrees)
    elevation : float
        elevation angle above horizon, neglecting aberrations (degrees)
    srange : float
        slant range [meters]
    deg : bool, optional
        degrees input/output  (False: radians in/out)

    Returns
    --------
    e : float
        East ENU coordinate (meters)
    n : float
        North ENU coordinate (meters)
    u : float
        Up ENU coordinate (meters)
    """
    if deg:
        el = radians(el)
        az = radians(az)

    if srange < 0:
        raise ValueError("Slant range  [0, Infinity)")

    r = srange * cos(el)

    return r * sin(az), r * cos(az), srange * sin(el)


def enu2geodetic(
    e: float,
    n: float,
    u: float,
    lat0: float,
    lon0: float,
    h0: float,
    ell: Ellipsoid = None,
    deg: bool = True,
) -> tuple[float | ndarray, float | ndarray, float | ndarray]:
    """
    East, North, Up to target to geodetic coordinates

    Parameters
    ----------
    e : float
        East ENU coordinate (meters)
    n : float
        North ENU coordinate (meters)
    u : float
        Up ENU coordinate (meters)
    lat0 : float
           Observer geodetic latitude
    lon0 : float
           Observer geodetic longitude
    h0 : float
         observer altitude above geodetic ellipsoid (meters)
    ell : Ellipsoid, optional
          reference ellipsoid
    deg : bool, optional
          degrees input/output  (False: radians in/out)


    Results
    -------
    lat : float
          geodetic latitude
    lon : float
          geodetic longitude
    alt : float
          altitude above ellipsoid  (meters)
    """

    x, y, z = enu2ecef(e, n, u, lat0, lon0, h0, ell, deg=deg)

    return ecef2geodetic(x, y, z, ell, deg=deg)


def geodetic2enu(
    lat: float,
    lon: float,
    h: float,
    lat0: float,
    lon0: float,
    h0: float,
    ell: Ellipsoid = None,
    deg: bool = True,
) -> tuple[float, float, float]:
    """
    Parameters
    ----------
    lat : float
          target geodetic latitude
    lon : float
          target geodetic longitude
    h : float
          target altitude above ellipsoid  (meters)
    lat0 : float
           Observer geodetic latitude
    lon0 : float
           Observer geodetic longitude
    h0 : float
         observer altitude above geodetic ellipsoid (meters)
    ell : Ellipsoid, optional
          reference ellipsoid
    deg : bool, optional
          degrees input/output  (False: radians in/out)


    Results
    -------
    e : float
        East ENU
    n : float
        North ENU
    u : float
        Up ENU
    """
    x1, y1, z1 = geodetic2ecef(lat, lon, h, ell, deg=deg)
    x2, y2, z2 = geodetic2ecef(lat0, lon0, h0, ell, deg=deg)

    return uvw2enu(x1 - x2, y1 - y2, z1 - z2, lat0, lon0, deg=deg)
