/* Ideas:
-Al momento de añadir el precio del producto agregar el IVA automaticamente (16%).
-Hacerle un hash las contraseñas
-Hacer una funcion que abra los JSON
-Hacer que el ID se coloque automaticamente
*/
#include <iostream>
#include <fstream>

#include <nlohmann/json.hpp>

using json = nlohmann::json;
using namespace std;

string username;
string password;
json archivo;
json usuario;
int id_empleado; // 1 Gerente 0 Empleado
int a; // Seleccion de archivo
int b; // Seleccion de accion a realizar con los archivos

void limpiarPantalla()
{
    // Si es windows usa cls
    #ifdef _WIN32
        system("cls");
    // Si es otra cosa usa clear
    #else
        system("clear");
    #endif
}

json verificarId()
{
    cout << endl << "Iniciar Sesion\n";
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
            return emp;
        }
    }
    return nullptr;
}


json abrirJson()
{

    if (usuario.is_null())
    {
        cout << "Informacion incorrecta. Intenta de nuevo.\n";
        cout << endl;
        limpiarPantalla();
        return json();
    }
    
    if (usuario["categoria"] == "empleado")
    {
        limpiarPantalla();
        // El empleado solo puede acceder a los productos
        cout << "Bienvenido empleado " << usuario["nombre"] << endl;
        ifstream f("productos.json");
        json productos = json::parse(f);
        limpiarPantalla();
        return archivo = productos;
    }
    else if (usuario["categoria"] == "gerente")
    {
        limpiarPantalla();
        // El gerente puede acceder a tres archvios distintos
        cout << "Bienvenido gerente " << usuario["nombre"] << endl;
        cout << endl << "Que desea revisar ?\n";
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
                limpiarPantalla();
                return archivo = productos;
            }

            case 2:
            {
                ifstream f("empleados.json");
                json empleados = json::parse(f);
                limpiarPantalla();
                return archivo = empleados;
            }

            case 3:
            {
                ifstream f("historial.json");
                json historial = json::parse(f);
                limpiarPantalla();
                return archivo = historial;
            }
            
            default:
            {
                limpiarPantalla();
                return json();
            }

        }
    }
    return json();
}


void seleccionarAccion()
{
    if (usuario["categoria"] == "gerente")
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
            limpiarPantalla();
            break;
        }
        case 2:
        {
            cout << archivo << endl;
            cout << "Que accion desea realizar ?\n" << endl;
            cout << "1 - Agregar empleado.\n" << endl;
            cout << "2 - Eliminar empleado.\n" << endl;
            cout << "3 - Modificar informacion del empleado.\n" << endl;
            cin >> b;
            limpiarPantalla();
            break;
        }
        case 3:
        {
            cout << archivo << endl;
            cout << "Que accion desea realizar ?\n" << endl;
            cout << "1 - Descargar historial de venta.\n" << endl;
            cout << "2 - Imprimir historial de venta.\n" << endl;
            cout << "3 - Borrar historial de venta.\n" << endl;
            cin >> b;
            limpiarPantalla();
            break;
        }
        default:
        {
            limpiarPantalla();
            break;
        }
        }
    }
    else if (usuario["categoria"] == "empleado")
    {
        cout << archivo << endl;
        cout << "Que accion desea realizar ?\n" << endl;
        cout << "1 - Agregar producto.\n" << endl;
        cout << "2 - Eliminar producto.\n" << endl;
        cout << "3 - Modificar producto.\n" << endl;
        cin >> b;
        limpiarPantalla();
    }
}


void modificarDatos()
{
    string nombre;
    string password;
    string categoria;
    int stock;
    int precio;
    int id_producto;

    if (usuario["categoria"] == "gerente")
    {
        if (a == 1) // Productos
        {
            switch (b) // 1, 2, 3
            {
                case 1: 
                {
                    cout << "Nombre del producto: ";
                    cin >> nombre;

                    cout << "ID del producto: ";
                    cin >> id_producto;

                    cout << "Cantidad del producto: ";
                    cin >> stock;

                    cout << "Precio unitario del producto: ";
                    cin >> precio;

                    json nuevo_producto = {
                        {"id", id_producto},
                        {"nombre", nombre},
                        {"stock", stock},
                        {"precio", precio}
                    };

                    archivo["productos"].push_back(nuevo_producto);

                    //Guardamos el archivo
                    ofstream out("productos.json");
                    out << archivo.dump(4);
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

                    cout << "ID del empleado: ";
                    cin >> id_empleado;

                    cout << "Usuario del empleado: ";
                    cin >> username;

                    cout << "Password: ";
                    cin >> password;

                    cout << "Categoria (empleado o gerente): ";
                    cin >> categoria;

                    json nuevo_empleado = {
                        {"id", id_empleado},
                        {"nombre", nombre},
                        {"username", username},
                        {"password", password},
                        {"categoria", categoria}
                    };

                    archivo["empleados"].push_back(nuevo_empleado);

                    ofstream out("empleados.json");
                    out << archivo.dump(4);
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
    else if (usuario["categoria"] == "empleado")
    {
        switch (b) // 1, 2, 3
            {
                case 1: 
                {
                    cout << "Nombre del producto: ";
                    cin >> nombre;

                    cout << "ID del producto: ";
                    cin >> id_producto;

                    cout << "Cantidad del producto: ";
                    cin >> stock;

                    cout << "Precio unitario del producto: ";
                    cin >> precio;

                    json nuevo_objeto = {
                        {"nombre", nombre},
                        {"id", id_producto},
                        {"stock", stock},
                        {"precio", precio}
                    };

                    archivo["productos"].push_back(nuevo_objeto);

                    //Guardamos el archivo
                    ofstream out("productos.json");
                    out << archivo.dump(4);
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
}


int main ()
{
    while (true)
    {
        usuario = verificarId();
        archivo = abrirJson();
        seleccionarAccion();
        modificarDatos();
    }
}