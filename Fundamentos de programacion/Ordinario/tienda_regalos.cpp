#include <iostream>
#include <fstream>

#include <nlohmann.json/include/nlohmann/json.hpp>

using json = nlohmann::json;
using namespace std;

void abrirJson()
{
    ifstream ifs("empleados.json");
    /*
    json j;
    file >> j;
    */ //Falta agregar la biblioteca
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
}

//ahuevo listo ya porfavoorrrrrr help
// Litzy ya pudo