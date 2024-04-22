#include <iostream>
#include <fstream>
#include <ctime>
#include "kelly_solver.h"

int main(int argc, char *argv[]) {
    KellyFormula k(2);

    k.stocks[0].getMiuSigma(1.08, 0.1);
    k.stocks[1].getMiuSigma(1.08, 0.1);
    //k.stocks[2].getMiuSigma(1.08, 0.25);
    //k.stocks[3].getMiuSigma(1.08, 0.25);
    //k.stocks[4].getMiuSigma(1.08, 0.27);

    //k.solveMaximum();


    k.final();


/*
    ofstream out;
    out.open("test2.csv");
    for (double E = 1.05; E <= 1.51; E += 0.05)
    {
        for (double V = 0.5; V <= 3.1; V += 0.25)
        {
            k.initialize();
            k.stocks[0].initialize();
            k.stocks[0].getMiuSigma(E, V * V);
            k.solveMaximum();

            out << k.stocks[0].solution << ',';
            cout << E << ": " << V << endl;
        }
        out << endl;
    }
    out.close();
*/

/*
    for (pair<double, double> p: k.curve)
    {
        cout << p.first << ',' << p.second << endl;
    }

    cout << k.stocks[1].miu << endl;
    cout << k.stocks[1].sigma << endl;
*/
    return 0;
}
