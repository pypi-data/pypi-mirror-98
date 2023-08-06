# Pijavski

This is an example of how to use CFFI to call a Pijavski function written in C++ that optimises a test function and returns the minimum.


## Installation

To install simply type:

```
$ pip install pijavski
```


## Usage

To test, open a python console and import the package. The function `pijavski.get_minimum`, with arguments *lip*, *xl*, *xu*, *precision* and *maxiter*, prints `res`, `x0`, `f`, `prec`, `maxit` as result.

```
>>> import pijavski
>>> pijavski.get_minimum()
0 -5323.428786928975 1.2546522006214123e-09 3.5218863499790176 65533
>>> pijavski.get_minimum(lip=3, xl=-100000, xu=100000, precision=1e-9, maxiter=1000000)
0 -87124.2182511797 2.102279885993885e-10 8.210802078457299 65533
```

### Defining custom functions to optimise

The function to optimise needs to be declared as a callback function for CFFI so that the Pijavski program can process it.
    
- The function definition needs to be preceeded by `@ffi.def_extern()`.

- The function name must be `fun` as this is how the callback function is defined in the CFFI builder.

- When writing the function,  arguments `f` and `x` need to be declared as if they were pointers using the bracket notation f[] and x[].

- Use numpy math functions.


Example:

```    
>>> # Simple declaration of f = -cos^2(x) as callback function.
>>> import numpy as np
>>> from pijavski import get_minimum, ffi, lib
>>> @ffi.def_extern()
... def fun(f, x):
...     f[0] = (-1)*np.cos(x[0])**2
>>> # Call get_minimum
>>> get_minimum(func=lib.fun, xl=-100, xu=100)
0 -1.0 4.6838846e-317 4.6838846e-317 1 
```
