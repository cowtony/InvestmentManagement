#include "Stock.h"

Stock::Stock()
{
    maxX = 0;
    lower   = 0;
    upper   = 1;

    r = new double[2];
    r[0] = 1;
    r[1] = -1;
}
