"""Misc utility functions that are not from SciPy, NumPy or scikit-image.

"""
import math

import numpy

if hasattr(math, 'prod'):
    prod = math.prod  # available in Python 3.8+ only
else:
    prod = numpy.prod


def _reshape_nd(arr, ndim, axis):
    """Promote a 1d array to ndim with size > 1 at the specified axis."""
    if arr.ndim != 1:
        raise ValueError("expected a 1d array")
    if axis < -ndim or axis > ndim - 1:
        raise ValueError("invalid axis")
    if ndim < 1:
        raise ValueError("ndim must be >= 1")
    axis = axis % ndim
    nd_shape = (1,) * axis + (arr.size,) + (1,) * (ndim - axis - 1)
    return arr.reshape(nd_shape)


def ndim(a):
    """
    Return the number of dimensions of an array.

    Parameters
    ----------
    a : array_like
        Input array.  If it is not already an ndarray, a conversion is
        attempted.

    Returns
    -------
    number_of_dimensions : int
        The number of dimensions in `a`.  Scalars are zero-dimensional.

    See Also
    --------
    ndarray.ndim : equivalent method
    shape : dimensions of array
    ndarray.shape : dimensions of array

    Examples
    --------
    >>> from cucim.numpy import ndim
    >>> ndim([[1,2,3],[4,5,6]])
    2
    >>> ndim(cupy.asarray([[1,2,3],[4,5,6]]))
    2
    >>> ndim(1)
    0

    """
    try:
        return a.ndim
    except AttributeError:
        return numpy.asarray(a).ndim


try:
    from cupy._util import _normalize_axis_index  # NOQA
    from cupy._util import _normalize_axis_indices

except ImportError:

    def _normalize_axis_index(axis, ndim):  # NOQA
        """
        Normalizes an axis index, ``axis``, such that is a valid positive
        index into the shape of array with ``ndim`` dimensions. Raises a
        ValueError with an appropriate message if this is not possible.

        Args:
            axis (int):
                The un-normalized index of the axis. Can be negative
            ndim (int):
                The number of dimensions of the array that ``axis`` should
                be normalized against

        Returns:
            int:
                The normalized axis index, such that
                `0 <= normalized_axis < ndim`
        """
        if axis < 0:
            axis += ndim
        if not (0 <= axis < ndim):
            raise numpy.AxisError("axis out of bounds")
        return axis

    def _normalize_axis_indices(axes, ndim):  # NOQA
        """Normalize axis indices.

        Args:
            axis (int, tuple of int or None):
                The un-normalized indices of the axis. Can be negative.
            ndim (int):
                The number of dimensions of the array that ``axis`` should
                be normalized against

        Returns:
            tuple of int:
                The tuple of normalized axis indices.
        """
        if axes is None:
            axes = tuple(range(ndim))
        elif not isinstance(axes, tuple):
            axes = (axes,)

        res = []
        for axis in axes:
            axis = _normalize_axis_index(axis, ndim)
            if axis in res:
                raise ValueError("Duplicate value in 'axis'")
            res.append(axis)

        return tuple(sorted(res))


try:
    from cupy.cuda._core import get_typename
except ImportError:
    # local copy of private code from CuPy
    _typenames_base = {
        numpy.dtype("float64"): "double",
        numpy.dtype("float32"): "float",
        numpy.dtype("float16"): "float16",
        numpy.dtype("complex128"): "complex<double>",
        numpy.dtype("complex64"): "complex<float>",
        numpy.dtype("int64"): "long long",
        numpy.dtype("int32"): "int",
        numpy.dtype("int16"): "short",
        numpy.dtype("int8"): "signed char",
        numpy.dtype("uint64"): "unsigned long long",
        numpy.dtype("uint32"): "unsigned int",
        numpy.dtype("uint16"): "unsigned short",
        numpy.dtype("uint8"): "unsigned char",
        numpy.dtype("bool"): "bool",
    }

    all_type_chars = "?bhilqBHILQefdFD"
    _typenames = {}
    for i in all_type_chars:
        d = numpy.dtype(i)
        t = d.type
        _typenames[t] = _typenames_base[d]

    def get_typename(dtype):
        if dtype is None:
            raise ValueError("dtype is None")
        if dtype not in _typenames:
            dtype = numpy.dtype(dtype).type
        return _typenames[dtype]


try:
    from cupy._util import PerformanceWarning
except ImportError:

    class PerformanceWarning(RuntimeWarning):
        """Warning that indicates possible performance issues."""
