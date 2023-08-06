typedef void ( *USER_FUNCTION)(double *, double *);


int Pijavski(double* x0, double *val, USER_FUNCTION f,double* Lip,  double* Xl, double* Xu, double* precision, int* maxiter);

