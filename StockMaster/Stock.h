#ifndef STOCK_H
#define STOCK_H
#include <vector>
#include <map>
#include "StockPrice.h"
using namespace std;

class Stock
{
public:
    Stock();

    double* r;

    map<double, double> RnP;
    double x;
    double lower;
    double upper;
    double maxX;



    vector<StockPrice> price;
};

#endif // STOCK_H
