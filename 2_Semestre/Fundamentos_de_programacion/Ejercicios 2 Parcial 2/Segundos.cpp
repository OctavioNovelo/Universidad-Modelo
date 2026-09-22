#include <iostream>

using namespace std;

int seg = 0;
int minutes = 0;
int days = 0;

void segundos()
{
    seg = seg + (minutes * 60);
    seg = seg + (days * 86400);
    cout << "Los segundos totales son: " << seg;
}

int main()
{
    cout << "Cuantos dias: ";
    cin >> days;
    cout << "Cuantos minutos: ";
    cin >> minutes;
    cout << "Cuantos segundos: ";
    cin >> seg;

    segundos();
}