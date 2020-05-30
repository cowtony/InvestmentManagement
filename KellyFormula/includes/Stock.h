#ifndef STOCK_H
#define STOCK_H
#include <vector>
#include <map>
using namespace std;

class Stock
{
public:
    Stock();
    void initialize();

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

    void getMiuSigma(double E, double var);
};

#endif // STOCK_H
