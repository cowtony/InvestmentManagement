#pragma once

#include <vector>
#include <map>

class Stock {
public:
    Stock() {
        x = 0;
        solution = 0;

        upper = 1;
        lower = 0;

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


    double solution;
    double x;
    double lower;
    double upper;

    double miu;
    double sigma;
    double s2sigma;   // sqrt(2) * sigma

    int numOfP;
    double* r;
    double* p;

    void getMiuSigma(double E, double var) {
        miu = log(E) - 0.5 * log(1 + var / E / E);
        sigma = sqrt(log(1 + var / E / E));
        s2sigma = sqrt(2) * sigma;
    }
};
