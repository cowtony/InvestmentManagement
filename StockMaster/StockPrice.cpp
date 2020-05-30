#include "StockPrice.h"

StockPrice::StockPrice()
{

}

void StockPrice::loadFromCSV(ifstream& in)
{
    in >> date;
    in >> open;
    in >> high;
    in >> low;
    in >> close;
    in >> adjClose;
    in >> volume;
}
