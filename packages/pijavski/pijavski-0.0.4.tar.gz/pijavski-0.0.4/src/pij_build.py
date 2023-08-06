
import cffi
import os

ffibuilder = cffi.FFI()

PATH = os.path.dirname(__file__)

ffibuilder.cdef("""

    typedef void ( *USER_FUNCTION)(double *, double *);
    
    int Pijavski(double* x0, double *val, USER_FUNCTION F, double* Lip, double* Xl, double* Xu, double* precision, int* maxiter);
    
    extern "Python" void fun(double* x, double* f);
    """, override=True)

ffibuilder.set_source("_pijavski", r"""
    #include "heap.h"
    #include "pijavski.h"
""",
    sources=[os.path.join(PATH, "pijavski.cpp")],
    include_dirs=[PATH]
    )


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
