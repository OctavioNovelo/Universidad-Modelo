#include <iostream>
#include <fstream>

#include <nlohmann/json.hpp>

using json = nlohmann::json;
using namespace std;

int id_empleado = 0; // Empleado = 0 Gerente = 1
string password;

json verificarId()
{
    cout << "Iniciar Sesion: \n";
    cout << "ID: ";
    cin >> id_empleado;
    cout << endl << "Password: ";
    cin >> password;

    ifstream f("empleados.json");
    json empleados = json::parse(f);

    if (id_empleado == empleados["gerentes", "id"])
    {
        id_empleado = 1;
        return id_empleado;
    }
    else if (id_empleado == empleados["empleados", "id"])
    {
        id_empleado = 0;
        return id_empleado;
    }
}

json abrirJson()
{
    if (id_empleado == 0)
    {
        // El empleado solo puede acceder a los productos
        ifstream f("productos.json");
        json productos = json::parse(f);
        return productos;
    }
    else if (id_empleado == 1)
    {
        // El gerente puede acceder a tres archvios distintos
        int a;
        cout << "Que desea revisar ?\n";
        cout << "1 - Productos\n";
        cout << "2 - Empleados\n";
        cin >> a;

        switch (a)
        {
            case 1:
            {
                ifstream f("productos.json");
                json productos = json::parse(f);
                return productos;
            }

            case 2:
            {
                ifstream f("empleados.json");
                json empleados = json::parse(f);
                return empleados;
            }

            case 3:
            {
                ifstream f("historial.json");
                json historial = json::parse(f);
                return historial;

            }
            
            default:
            {
                return json();
            }

        }
    }
    return json();
}


void accederDatos()
{
    /*
    string nombre = j["nombre"];
    string id = j["id"];
    */

}

void modificarDatos()
{
    /*
    j["nombre"] = j["nombre"].get<string>(Pepito);
    j["birthday"] = "12/09/2006";
    */
}

void guardarDatos()
{
    /*
    ofstream out("empleados.json");
    out << j.dump(4);
    */
}

int main ()
{
    abrirJson();
}

//ahuevo listo ya porfavoorrrrrr help
// Litzy ya pudo