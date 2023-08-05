import numpy as _onp
import casadi as _cas
from aerosandbox.numpy.arithmetic import sum, abs
from aerosandbox.numpy.determine_type import is_casadi_type

def dot(a, b):
    """
    Dot product of two arrays.

    See syntax here: https://numpy.org/doc/stable/reference/generated/numpy.dot.html
    """
    if not is_casadi_type([a, b], recursive=True):
        return _onp.dot(a, b)

    else:
        return _cas.dot(a, b)

def cross(a, b, axisa=-1, axisb=-1, axisc=-1, axis=None):
    """
    Return the cross product of two (arrays of) vectors.

    See syntax here: https://numpy.org/doc/stable/reference/generated/numpy.cross.html
    """
    if not is_casadi_type([a, b], recursive=True):
        return _onp.cross(a, b, axisa=axisa, axisb=axisb, axisc=axisc, axis=axis)

    else:
        if axis is not None:
            if not (
                axis == -1 or
                axis == 0 or
                axis == 1
            ):
                raise ValueError("`axis` must be -1, 0, or 1.")
            axisa = axis
            axisb = axis
            axisc = axis


        if axisa == -1 or axisa == 1:
            if not is_casadi_type(a):
                a = _cas.DM(a)
            a = a.T
        elif axisa == 0:
            pass
        else:
            raise ValueError("`axisa` must be -1, 0, or 1.")

        if axisb == -1 or axisb == 1:
            if not is_casadi_type(b):
                b = _cas.DM(b)
            b = b.T
        elif axisb == 0:
            pass
        else:
            raise ValueError("`axisb` must be -1, 0, or 1.")

        # Compute the cross product, horizontally (along axis 1 of a 2D array)
        c = _cas.cross(a, b)

        if axisc == -1 or axisc == 1:
            c = c.T
        elif axisc == 0:
            pass
        else:
            raise ValueError("`axisc` must be -1, 0, or 1.")

        return c
