#pragma once

#include <iostream>
#include <vector>
#include <map>
#include <cmath>
#include <ctime>
#include "stock.h"

class KellyFormula {
public:
    KellyFormula(const int& number) {
        maximum = 0;

        numOfStocks = number;
        stocks = new Stock [numOfStocks];

        //stocks[0].r[0] = 1.1;
        //stocks[0].r[1] = -0.9;
        //stocks[0].p[0] = 0.7;
        //stocks[0].p[1] = 0.3;
    }

    ~KellyFormula() {
        delete[] stocks;
    }


    double maximum;
    double s2sigmaSqrtPi;

    int derivative;


    std::map<double, double> curve;

    int    numOfStocks;
    Stock* stocks;
    double dx;

    void solveMaximum() {
        time_t startTime = time(0);
        for (dx = 0.25; dx > 0.00000001; dx /= 4) {
            time_t startTimeLittle = time(0);

            findMaximumInMesh();

            for (int i = 0; i < numOfStocks; i++) {
                stocks[i].lower = std::max(0.0, stocks[i].solution - dx);
                stocks[i].upper = std::min(1.0, stocks[i].solution + dx);
            }

            for (int i = 0; i < numOfStocks; i++) {
                printf("%6f ", stocks[i].solution);
            }
            std::cout << time(0) - startTimeLittle << std::endl;
        }
        std::cout << "GPR: " << exp(maximum) - 1 << " " << time(0) - startTime << std::endl;
    }

    void findMaximumInMesh(int depth = 0) {
        if (depth == numOfStocks) {
            //double result = discreteGLR();
            //double result = continiousGLR();
            double result = specialGLR();

            curve[stocks[0].x] = result;  // Debug only

            if (result > maximum) {
                maximum = result;
                for (int i = 0; i < numOfStocks; i++)
                    stocks[i].solution = stocks[i].x;
            }
            return;
        }

        for (stocks[depth].x = stocks[depth].lower; stocks[depth].x <= stocks[depth].upper; stocks[depth].x += dx) {
            findMaximumInMesh(depth + 1);
        }
    }

    double discreteGLR(const int depth = 0, const double E = 1, double P = 1) const {
        if (depth == numOfStocks) {
            return P * log(E);
        }

        double f = 0;
        for (int i = 0; i < stocks[depth].numOfP; i++) {
            f += discreteGLR(depth + 1, E + stocks[depth].x * stocks[depth].r[i], P * stocks[depth].p[i]);
        }
        return f;
    }

    double continiousGLR(int depth = 0, double E = 1, double P = 1) const {
        if (depth == numOfStocks) return log(E) * P;

        double f = 0;
        double dr = 0.001;
        for (double r = -10; r <= 10; r += dr)
        {
            f += continiousGLR(depth + 1, E + stocks[depth].x * (exp(r) - 1), P * pNormal(r, stocks[depth].sigma, stocks[depth].miu) * dr);
        }
        return f;
    }

    double pLogNormal(double r, double sigma, double miu) const {
        if (r > 0)
            return pNormal(log(r), sigma, miu) / r;
        else return 0;
    }

    double specialGLR(int depth = 0, double E = 1, double P = 0) const {
        // This function can only garenntee to get max X value, but not GLR(X)
        if (depth == numOfStocks) return log(E) * exp(P);// * s2sigmaSqrtPi;

        double f = 0;
        double ds = 0.01;
        for (double s = -2; s <= 2; s += ds)
        {
            f += specialGLR(depth + 1, E + (exp(s) - 1) * stocks[depth].x, P - pow((s - stocks[depth].miu) / stocks[depth].s2sigma, 2));
        }
        return f;
    }

    void final() {
        s2sigmaSqrtPi = 1.00;
        for (int i = 0; i < numOfStocks; i++)
            s2sigmaSqrtPi /= stocks[i].s2sigma * sqrt(3.1415926);

        double coeficient = 0;
        bool flag;

        do
        {
            flag = false;
            for (derivative = 0; derivative < numOfStocks; derivative++)
            {
                double dx = specialGLR_D();
                if (coeficient == 0) coeficient = dx / 0.2;
                dx /= coeficient;

                if (dx > 0.001 || dx < -0.001) flag = true;


                stocks[derivative].solution = stocks[derivative].x + dx;

                std::cout << stocks[derivative].x << ' ' << dx << std::endl;

                if (stocks[derivative].solution > 1) stocks[derivative].solution = 1;
                if (stocks[derivative].solution < 0) stocks[derivative].solution = 0;
            }

            double sum = 0;
            for (int i = 0; i < numOfStocks; i++)
            {
                stocks[i].x = stocks[i].solution;
                sum += stocks[i].x;
            }

            std::cout << "SUM: " << sum << std::endl << std::endl;
        }while (flag);


    /*
        redo:
        for (derivative = 0; derivative < numOfStocks; derivative++)
        {
            stocks[derivative].x = stocks[derivative].solution;
            if (abs(specialGLR_D()) > 1e-5)
            {
                solveDerivative();

                cout << derivative << ": ";
                for (int i = 0; i < numOfStocks; i++)
                {
                    cout << stocks[i].solution << ' ';
                }
                cout << endl;
                //system("pause");

                goto redo;
            }
        }


        cout << "final result:" << endl;
        for (int i = 0; i < numOfStocks; i++)
        {
            cout << stocks[i].solution << ' ';
        }
        cout << endl;

    */
    }
    
    double solveDerivative() {
        stocks[derivative].lower = 0;
        stocks[derivative].x = 0;
        if (specialGLR_D() < 0)
            return 0;

        stocks[derivative].upper = 1;
        stocks[derivative].x = 1;
        if (specialGLR_D() > 0)
            return 1;

        while (true)
        {
            stocks[derivative].x = (stocks[derivative].lower + stocks[derivative].upper) / 2;
            double mid = specialGLR_D();
            if (mid > 1e-5)
                stocks[derivative].lower = stocks[derivative].x;
            else if (mid < -1e-5)
                stocks[derivative].upper = stocks[derivative].x;
            else
            {
                stocks[derivative].solution = stocks[derivative].x;
                return stocks[derivative].solution;
            }
        }
    }

    double specialGLR_D(int depth = 0, double E = 0, double P = 0) const {
        if (depth == numOfStocks) return  1 / E * exp(P) * s2sigmaSqrtPi;

        double df = 0;
        double ds = 0.1;
        for (double s = -2; s <= 2; s += ds)
        {
            if (depth == derivative)
                df += specialGLR_D(depth + 1, E + 1 / (exp(s) - 1) + stocks[depth].x, P - pow((s - stocks[depth].miu) / stocks[depth].s2sigma, 2));
            else
                df += specialGLR_D(depth + 1, E + (exp(s) - 1) * stocks[depth].x, P - pow((s - stocks[depth].miu) / stocks[depth].s2sigma, 2));
        }
        return df;
    }

    double specialGLR_D2(int depth = 0, double E = 0, double P = 0) const {
        if (depth == numOfStocks) return  -1 / E / E * exp(P) * s2sigmaSqrtPi;

        double df = 0;
        double ds = 0.1;
        for (double s = -2; s <= 2; s += ds)
        {
            if (depth == derivative)
                df += specialGLR_D(depth + 1, E + 1 / (exp(s) - 1) + stocks[depth].x, P - pow((s - stocks[depth].miu) / stocks[depth].s2sigma, 2));
            else
                df += specialGLR_D(depth + 1, E + (exp(s) - 1) * stocks[depth].x, P - pow((s - stocks[depth].miu) / stocks[depth].s2sigma, 2));
        }
        return df;
    }

private:
    // TODO: Move to Stock class
    static double pNormal(double r, double sigma, double miu) {
        double s2sigma = sigma * sqrt(2);
        return exp(-pow((r - miu) / s2sigma, 2)) / s2sigma / sqrt(PI);
    }

    static constexpr double PI = 3.14159265358979323846;
};
