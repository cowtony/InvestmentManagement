#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <fstream>
#include "Stock.h"
#include "KellyFormula.h"
using namespace std;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
/*
    ifstream in("C:\\Users\\Nium\\Google Drive\\Programming\\Qt Creator\\StockMaster\\release\\SPY.csv", ios::in);
    if (in.is_open())
    {
        string s;
        getline(in, s);

        while (in.good())
        {
            StockPrice price;
            price.loadFromCSV(in);

        }

        in.close();
    }
*/



    KellyFormula kF;


    double dx = 0.1;
    for (int i = 0; i< 5; i++)
    {
        kF.calculateXY(0, 1, dx);

        for (int j = 0; j < kF.stocks.size(); j++)
        {
            kF.stocks[j].lower = kF.stocks[j].maxX - dx;
            kF.stocks[j].upper = kF.stocks[j].maxX + dx;
            if (kF.stocks[j].lower < 0)kF.stocks[j].lower = 0;
            if (kF.stocks[j].upper > 1)kF.stocks[j].upper = 1;
        }


        ui->textBrowser->append(QString::number(kF.maximum));
        ui->textBrowser->append(QString::number(kF.stocks[0].maxX) + " " + QString::number(kF.stocks[0].lower) + " " + QString::number(kF.stocks[0].upper));
        ui->textBrowser->append(QString::number(kF.stocks[1].maxX) + " " + QString::number(kF.stocks[1].lower) + " " + QString::number(kF.stocks[1].upper));
        ui->textBrowser->append(QString::number(kF.stocks[2].maxX) + " " + QString::number(kF.stocks[2].lower) + " " + QString::number(kF.stocks[2].upper));
        ui->textBrowser->append(QString::number(kF.stocks[3].maxX) + " " + QString::number(kF.stocks[3].lower) + " " + QString::number(kF.stocks[3].upper));
        //ui->textBrowser->append(QString::number(kF.stocks[4].maxX) + " " + QString::number(kF.stocks[4].lower) + " " + QString::number(kF.stocks[4].upper));
        //ui->textBrowser->append(QString::number(kF.stocks[5].maxX) + " " + QString::number(kF.stocks[5].lower) + " " + QString::number(kF.stocks[5].upper));
        ui->textBrowser->append("\n");
        dx /= 10;
    }



    //double result = kF.calculateF();
    //ui->textBrowser->append(QString::number(result));

}

MainWindow::~MainWindow()
{
    delete ui;
}
