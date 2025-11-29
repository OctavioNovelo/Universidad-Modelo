/* Ideas:
-Al momento de añadir el precio del producto agregar el IVA automaticamente (16%).
*/
#include <iostream>
#include <fstream>

#include <nlohmann/json.hpp>

using json = nlohmann::json;
using namespace std;

string username;
string categoria;
string password;
json archivo;
int id_empleado; // 1 Gerente 0 Empleado
int a; // Seleccion de archivo
int b; // Seleccion de accion a realizar con los archivos

json verificarId()
{
    cout << "Iniciar Sesion\n";
    cout << "Username: ";
    cin >> username;
    cout << endl << "Password: ";
    cin >> password;
    cout << endl;

    ifstream f("empleados.json");
    json empleados = json::parse(f);

    // Para cada empleado (Objeto JSON) dentro del arreglo empleados llamalo emp, y usalo como referencia
    // for (auto x : arreglo) Para cada elemento del arreglo, nómbralo x y ejecuta el bloque
    // auto = nlohmann::json Esto le dice al compilador el tipo de datos
    for (auto& emp : empleados["empleados"])
    {
        if (username == emp["username"] && password == emp["password"])
        {
            cout << "Inicio de sesion exitoso.\n";
            return emp;
        }
    }

    cout << "Informacion incorrecta. Intente de nuevo" << endl;
    return nullptr;
}


json abrirJson()
{
    if (categoria == "empleado")
    {
        // El empleado solo puede acceder a los productos
        ifstream f("productos.json");
        json productos = json::parse(f);
        return archivo = productos;
    }
    else if (categoria == "gerente")
    {
        // El gerente puede acceder a tres archvios distintos
        cout << "Que desea revisar ?\n";
        cout << "1 - Productos.\n";
        cout << "2 - Empleados.\n";
        cout << "3 - Historial de ventas.\n";
        cin >> a;

        switch (a)
        {
            case 1:
            {
                ifstream f("productos.json");
                json productos = json::parse(f);
                return archivo = productos;
            }

            case 2:
            {
                ifstream f("empleados.json");
                json empleados = json::parse(f);
                return archivo = empleados;
            }

            case 3:
            {
                ifstream f("historial.json");
                json historial = json::parse(f);
                return archivo = historial;
            }
            
            default:
            {
                return json();
            }

        }
    }
    return json();
}


void seleccionarAccion()
{
    if (categoria == "gerente")
    {
        switch (a)
        {
        case 1:
        {
            cout << archivo << endl;
            cout << "Que accion desea realizar ?\n" << endl;
            cout << "1 - Agregar producto.\n" << endl;
            cout << "2 - Eliminar producto.\n" << endl;
            cout << "3 - Modificar producto.\n" << endl;
            cin >> b;
        }
        case 2:
        {
            cout << archivo << endl;
            cout << "Que accion desea realizar ?\n" << endl;
            cout << "1 - Agregar empleado.\n" << endl;
            cout << "2 - Eliminar empleado.\n" << endl;
            cout << "3 - Modificar informacion del empleado.\n" << endl;
            cin >> b;
        }
        case 3:
        {
            cout << archivo << endl;
            cout << "Que accion desea realizar ?\n" << endl;
            cout << "1 - Descargar historial de venta.\n" << endl;
            cout << "2 - Imprimir historial de venta.\n" << endl;
            cout << "3 - Borrar historial de venta.\n" << endl;
            cin >> b;
        }
        default:
        {
            break;
        }
        }
    }
    else if (id_empleado == 0)
    {
        cout << archivo << endl;
        cout << "Que accion desea realizar ?\n" << endl;
        cout << "1 - Agregar producto.\n" << endl;
        cout << "2 - Eliminar producto.\n" << endl;
        cout << "3 - Modificar producto.\n" << endl;
        cin >> b;
    }
}

void modificarDatos()
{
    if (categoria == "gerente")
    {
        string nombre;
        string password;
        int categoria;
        int stock;
        int precio;
        int id;

        if (a == 1) // Productos
        {
            switch (b) // 1, 2, 3
            {
                case 1: 
                {
                    cout << "Nombre del producto: ";
                    cin >> nombre;
                    archivo["nombre"] = nombre;

                    cout << "ID del producto: ";
                    cin >> id;
                    archivo["id"] = id;

                    cout << endl << "Cantidad del producto: ";
                    cin >> stock;
                    archivo["stock"] = stock;

                    cout << endl << "Precio unitario del producto: ";
                    cin >> precio;
                    archivo["precio"] = precio;
                }
                case 2:
                {
                    // Eliminar
                }
                case 3:
                {
                    // Modificar
                }
            }
        }
        else if (a == 2) // Empleados
        {
            switch (b) // 1, 2, 3
            {
                case 1: 
                {
                    cout << "Nombre del empleado: ";
                    cin >> nombre;
                    archivo["nombre"] = nombre;

                    cout << "ID del empleado: ";
                    cin >> id;
                    archivo["id"] = id;

                    cout << endl << "Usuario del empleado: ";
                    cin >> username;
                    archivo["usrname"] = username;

                    cout << endl << "Password: ";
                    cin >> password;
                    archivo["password"] = password;

                    cout << endl << "Categoria: ";
                    cin >> categoria;
                    archivo["categoria"] = categoria;
                }
                case 2:
                {
                    // Eliminar
                }
                case 3:
                {
                    // Modificar
                }
            }
        }
        else if (a == 3) //Historial de ventas
        {
            switch (b) // 1, 2, 3
            {
                case 1: 
                {
                    // Descargar
                }
                case 2:
                {
                    // Imprimir
                }
                case 3:
                {
                    // Borrar
                }
            }
        }
    }
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
    json categoria = verificarId();

    if (categoria.is_null())
    {
        return 0;
    }

    if (categoria["categoria"] == "gerente")
    {
        //Abrir pagina principal
        // Escoger entre:
        // productos.json
        // Carrito
        // empleados.json
        // historial.json
    }
    else if (categoria["categoria"] == "empleado")
    {
        //Escoger entre: 
        // Carrito
        // productos.json
    }
}