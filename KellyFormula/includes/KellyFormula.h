#ifndef KELLYFORMULA_H
#define KELLYFORMULA_H

#include <iostream>
#include <vector>
#include <map>
#include "Stock.h"
using namespace std;

class KellyFormula
{
public:
    KellyFormula(const int& number);
    ~KellyFormula();
    void initialize();


    double maximum;
    double s2sigmaSqrtPi;

    void solveMaximum();


    int derivative;


    map<double, double> curve;

//private:
    int    numOfStocks;
    Stock* stocks;
    double dx;

    void findMaximumInMesh(int depth = 0);

    double discreteGLR(const int depth = 0, const double E = 1, double P = 1) const;
    double continiousGLR(int depth = 0, double E = 1, double P = 1) const;

    double pNormal(double r, double sigma, double miu) const;
    double pLogNormal(double r, double sigma, double miu) const;


    double specialGLR(int depth = 0, double E = 1, double P = 0) const;

    void final();
    double solveDerivative();
    double specialGLR_D(int depth = 0, double E = 0, double P = 0) const;
    double specialGLR_D2(int depth = 0, double E = 0, double P = 0) const;
};

#endif // KELLYFORMULA_H
