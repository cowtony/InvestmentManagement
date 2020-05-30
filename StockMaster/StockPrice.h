#ifndef STOCKPRICE_H
#define STOCKPRICE_H
#include <fstream>
using namespace std;

class StockPrice
{
public:
    StockPrice();

    unsigned long date;
    double open;
    double high;
    double low;
    double close;
    double adjClose;
    double volume;

    void loadFromCSV(ifstream& in);

};

#endif // STOCKPRICE_H
