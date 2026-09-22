#include <iostream>

using namespace std;

string term;
string assesment;
string palindrome;

void palindromo()
{
    cout << "Escribe la palabra: " << '\n';

    cin >> term;

    string palindrome = term;

    int size = term.length();

    for (int i = size - 1; i >= 0; i--)
    {
        palindrome[size-i-1] = term[i]; /*Guarda los valores correspondeintes en los arrays
        palindrome y term, cada que incia el ciclo for se le resta 2 a la varaible i haciendo
        que se sustituya cada indice de los arrays */
    }

    cout << "Al revez se escribe: " << palindrome << '\n'; //Imprime la palabra ingresada al revez

    if (palindrome == term){
        cout << "Si es un palindromo" << '\n';   
    }
    else{
        cout << "No es un palindromo" << '\n';
    }
}

int main ()
{
    palindromo();
}