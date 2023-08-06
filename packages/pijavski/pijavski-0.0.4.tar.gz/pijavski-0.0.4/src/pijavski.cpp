
#include "heap.h"

#include <cstdlib>
#include <vector>
#include <cmath>
#include <iostream>


typedef void ( *USER_FUNCTION)(double *, double *);



#pragma optimize( "", off )
#pragma OPTIMIZE OFF

#ifdef _MSC_VER
// if the compiler does not recognise this type, change it to another int type 8 bytes long
// like long long int
typedef  __int64 ULINT; //this type myst be 8 bytes long
#else
typedef unsigned long long int ULINT; //this type myst be 8 bytes long
#endif


KEY_TYPE ft; // global
#define PACKFLOAT(f) ( (f  & 0xFFFFFFFF))
#define f2ulint(a)  (*(unsigned int*) &(a))
#define ulint2f(a) (*(float*) &(a))
unsigned int UL1;

KEY_TYPE _getKey(node_t theNode)
{
    UL1=theNode.data>>32;
    ft=ulint2f(UL1) ;
    // use the first 4 bytes
    return ft;
}

INDEX_TYPE _getIndex(node_t theNode) {    return 0; }
void _setIndex(node_t theNode, INDEX_TYPE I) {}


ULINT UL;
unsigned int UI;

INDEX_TYPE Merge1 (bheap_t *h, float f, unsigned short i, unsigned short j)
{
    UL=f2ulint(f); ///< 32;
#ifdef _MSC_VER
       UL = (UL << 32) & 0xFFFFFFFF00000000UL ;
#else
       UL = (UL << 32) & 0xFFFFFFFF00000000ULL ;
#endif
    UI = i;
    UI = ((UI  << 16) & 0xFFFF0000) | j;
    UL = UL + UI;
    return bh_insert(h, UL);
}

void GetIndices(DATA_TYPE Node, unsigned short int *i, unsigned short int *j)
{
#ifdef _MSC_VER
       UI = Node & 0x00000000FFFFFFFFUL ;
#else
       UI = Node & 0x00000000FFFFFFFFULL ;
#endif
       *j = UI & 0x0000FFFF;
       *i = (UI >> 16) & 0x0000FFFF;
}

#pragma optimize( "", on )

//extern "C"{
void ComputeMin(double x1, double x2, double f1, double f2, double M, double* t, float* f)
{
    *t= 0.5*(x1+x2) + 0.5/M*(f1-f2);
    *f= 0.5*(f1+f2) + 0.5*M*(x1-x2);
}
//}

extern "C"{
int Pijavski(double* x0, double *val, USER_FUNCTION F, double* Lip, double* Xl, double* Xu, double* precision, int* maxiter)
{
    bheap_t* HeapP = bh_alloc();
    DATA_TYPE Node;

    std::vector<double> x, f;
    
    if (*maxiter>=0xFFFD) *maxiter=0xFFFD; // cannot use short indices!

    int Iter=0;
    double Best=10e10;
    double CurrPrecision=10e10;


    double t,t1, t2,t3,f1,f2, f3, M=*Lip;
    float ff;

    unsigned short int i,j,k;

    t1=*Xl;
    F(&t1,&f1);     if(Best>f1) { Best=f1; *x0=t1;}
    x.push_back(t1);
    f.push_back(f1);

    t2=*Xu;
    F(&t2,&f2);        if(Best>f2) { Best=f2; *x0=t2;}
    x.push_back(t2);
    f.push_back(f2);

    i=0; j=1;
    ComputeMin(t1,t2,f1,f2,M,&t,&ff);
    CurrPrecision = Best - ff;

    Merge1(HeapP, -ff, i,j);

    Iter=1;
    while(Iter < *maxiter && CurrPrecision > *precision ) {
        Iter++;
        Node=bh_delete_min(HeapP);
        GetIndices(Node, &i, &j);

        t1=x[i]; t2=x[j]; f1=f[i]; f2=f[j];

        ComputeMin( t1,t2,f1,f2,  M, &t3, &ff);

        F(&t3,&f3);
        x.push_back(t3);
        f.push_back(f3);
        k=Iter;

        if(Best>f3) { Best=f3; *x0=t3;}
        CurrPrecision = Best - ff;
        
// two new minima
        ComputeMin(t1,t3,f1,f3,M,&t,&ff);
        Merge1(HeapP, -ff, i,k);

    //    ComputeMin(t3,t2,f3,f2,M,&t,&ff);  // always the same value ff
        Merge1(HeapP, -ff, k,j);
    
    }

    *val=Best;

    bh_delete_min(HeapP);

    *precision=CurrPrecision;
    *maxiter=Iter;
    if(CurrPrecision<0) return -1;  // too small Lip const


    return 0;
}
}
