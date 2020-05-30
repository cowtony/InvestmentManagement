#ifndef KELLYFORMULA_H
#define KELLYFORMULA_H

#include <iostream>
#include <vector>
#include "Stock.h"
using namespace std;

class KellyFormula
{
public:
    KellyFormula();
    vector<Stock> stocks;
    int numOfStocks = 2;
    Stock* stock;



    double maximum;

    void calculateXY(int depth = 0, double remaining = 1, double dx = 0.1);
    double calculateF(int depth = 0, double P = 1, double E = 1) const;

private:
    double pX(double r);
    double pY(double r);
    double pLgN(double r);
    double round(double value, double min, double max);

};

#endif // KELLYFORMULA_H
