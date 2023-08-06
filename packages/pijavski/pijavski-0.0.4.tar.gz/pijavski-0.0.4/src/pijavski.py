from _pijavski import ffi, lib
import numpy as np


@ffi.def_extern()
def fun(x, f):
    """
    Sample test function to be optimised.
    """
    f[0] = (-1)*np.cos(x[0])+0.00001*(x[0]-100*3.1415)*(x[0]-100*3.1415)


def get_minimum(func=lib.fun, lip=2., xl=-50000., xu=90000., precision=1e-12, maxiter=300000):
    """
    Get the minimum of a given function using the Pijavski function.
    
    The function to optimise needs to be declared as a callback function for CFFI so that
    the Pijavski program can process it.
    
    :type func: _cffi_backend._CDataBase (<cdata> pointer-to-function object)
    :param func: Function with argumenst `x` and and `f` to be optimised using Pijavski. 
        It is a callback function that needs to be declared similar to a function in C/C++ 
        and using `@ffi.def_extern()` before the declaration. See below Basic Usage for how
        to declare this function.
    :type lip: float
    :param lip: Lipschitz constant.
    :type xl: float
    :param xl: Lower bound of the interval on which to optimise.
    :type xu: float
    :param xu: Upper bound of the interval on which to optimise.
    :type precision: float
    :param precision: Desired precision.
    :type maxiter: int
    :param maxiter: Maximum iterations.
    
    .. rubric:: Basic Usage

    >>> import pijavski
    >>> pijavski.get_minimum()
    0 314.1592651760589 -0.9999999991415484 8.584516431042744e-10 65533
    
    .. rubric:: _`Defining custom functions to optimise`
    
    - The function definition needs to be preceeded by `@ffi.def_extern()`.
    
    - The function name must be `fun` as this is how the callback function is defined in the
      CFFI builder.
      
    - When writing the function,  arguments `f` and `x` need to be declared as if they were 
      pointers using the bracket notation f[] and x[].
      
    - Use numpy math functions.
    
    Example:
    
    >>> # Simple declaration of f = -cos^2(x) as callback function.
    >>> import numpy as np
    >>> from pijavski import get_minimum, ffi, lib
    >>> @ffi.def_extern()
    ... def fun(f, x):
    ...     f[0] = (-1)*np.cos(x[0])**2
    >>> # Call get_minimum
    >>> get_minimum(func=lib.fun, xl=-100, xu=100)
    0 -1.0 4.6838846e-317 4.6838846e-317 1    
    """
    
    x0 = ffi.new("double *")
    f = ffi.new("double *")
    M = ffi.new("double *", lip)
    x1 = ffi.new("double *", xl)
    x2 = ffi.new("double *", xu)
    prec = ffi.new("double *", precision)
    maxit = ffi.new("int *", maxiter)
    
    res = lib.Pijavski(x0, f, func, M, x1, x2, prec, maxit)
    print(res, x0[0], f[0], prec[0], maxit[0])
