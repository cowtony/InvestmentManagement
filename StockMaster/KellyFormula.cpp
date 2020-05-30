#include "KellyFormula.h"
#include <cmath>

KellyFormula::KellyFormula()
{
    maximum = 0;
    Stock a;

    stocks.push_back(a);
    stocks[0].RnP[1] = 0.6;
    stocks[0].RnP[-1] = 0.4;

    stocks.push_back(a);
    stocks[1].RnP[1] = 0.6;
    stocks[1].RnP[-1] = 0.4;

    stocks.push_back(a);
    stocks[2].RnP[1] = 0.6;
    stocks[2].RnP[-1] = 0.4;

    stocks.push_back(a);
    stocks[3].RnP[1] = 0.6;
    stocks[3].RnP[-1] = 0.4;

    //stocks.push_back(a);
    //stocks[4].RnP[1] = 0.6;
    //stocks[4].RnP[-1] = 0.4;

    //stocks.push_back(a);
    //stocks[5].RnP[1] = 0.6;
    //stocks[5].RnP[-1] = 0.4;
}

void KellyFormula::calculateXY(int depth, double remaining, double dx)
{
    if (depth == stocks.size())
    {
        double result = calculateF();
        if (result > maximum)
        {
            maximum = result;
            for (int i = 0; i < stocks.size(); i++)
            {
                stocks[i].maxX = stocks[i].x;
            }
        }
        return;
    }

    for (stocks[depth].x = stocks[depth].lower; stocks[depth].x <= remaining && stocks[depth].x <= stocks[depth].upper; stocks[depth].x += dx)
    {
        calculateXY(depth + 1, remaining - stocks[depth].x, dx);
    }
}

double KellyFormula::calculateF(int depth, double P, double E)
{
    if (depth == stocks.size())
    {
        return P * log(E);
    }

    double f = 0;
    for (pair<double, double> rNp: stocks[depth].RnP)
    {
        f += calculateF(depth + 1, P * rNp.second, E + stocks[depth].x * rNp.first);
    }
    return f;
}

double KellyFormula::pX(double r)
{
    if (r > 0) return 0.6;
    else return 0.4;
}

double KellyFormula::pY(double r)
{
    if (r > 0) return 0.6;
    else return 0.4;
}

double KellyFormula::pLgN(double r)
{
    static const double pi = 3.14159265358979;
    static const double sqrt2pi = sqrt(2 * pi);
    double sigma = 1;
    double miu = 0;
    return exp(-pow(log(r) - miu, 2) / (2 * sigma * sigma)) / (r * sigma * sqrt2pi);
}

double KellyFormula::round(double value, double min, double max)
{
    if (value < min) return min;
    else if (value > max) return max;
    else return value;
}
