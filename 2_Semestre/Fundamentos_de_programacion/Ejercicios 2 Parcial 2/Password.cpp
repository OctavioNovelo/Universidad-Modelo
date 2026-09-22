#include <iostream>
#include <bits/stdc++.h>

using namespace std;

string password;
bool num = false, upper = false, lower = false;

void key_Password()
{
    int cont = 1;
    while (cont == 1)
    {
        string a;
        cout << "Key your password: ";
        cin >> password;
        a = password;
        cout << "Confirm your password: ";
        cin >> password;

        if (a != password){
            cout << "The passwords not match, repeat\n";
        }
        else if (a == password)
        {
            cont = 0;
        }
    }
}

void verificacion()
{
    for (int i = 0; i < password.length(); i++)
    {
        if (password.length() > 8)
        {
            num = true;
        }
        if (password[i] >= 'A' && password[i] <= 'Z')
        {
            upper = true;
        }
        if (password[i] >= 'a' && password[i] <= 'z')
        {
            lower = true;
        }
    }
    
    if (num == true && upper == true && lower == true)
    {
        cout << "The password is valid\n";
    }
    else 
    {
        cout << "The password is not valid.\n";
    }
}
int main()
{
    key_Password();
    verificacion();
}