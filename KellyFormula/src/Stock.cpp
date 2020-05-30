#include "Stock.h"
#include <cmath>

Stock::Stock()
{
    initialize();


    numOfP = 4;
    r = new double[numOfP];
    p = new double[numOfP];
    r[0] = 1.05;    p[0] = 0.42;
    r[1] = 0.05;   p[1] = 0.28;
    r[2] = -0.05;    p[2] = 0.18;
    r[3] = -0.95;   p[3] = 0.12;

    //double E = 1.05;
    //double var = pow(0.0, 2);
    //getMiuSigma(E, var);
}

void Stock::initialize()
{
    x = solution = 0;

    upper = 1;
    lower = 0;
}


void Stock::getMiuSigma(double E, double var)
{
    miu = log(E) - 0.5 * log(1 + var / E / E);
    sigma = sqrt(log(1 + var / E / E));
    s2sigma = sqrt(2) * sigma;
}
