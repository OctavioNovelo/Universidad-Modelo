#include "json.hpp"
#include "general.hpp"

#include <iostream>
#include <string>
#include "json.hpp"

using json = nlohmann::json;
using namespace std;

//Variables globales
json archivo;
json usuario;

// Funciones
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
        // El empleado solo puede acceder a los productos, carrito y salir
        cout << "Bienvenido empleado " << usuario["nombre"] << '\n';
        cout << "Aviso: Para navegar por la interfaz use el teclado numerico.\n" << endl;
        cout << "Que desea hacer ?\n";
        cout << "1 - Carrito.\n";
        cout << "2 - Productos.\n";
        cout << "3 - Regresar.\n";
        cin >> a;
        cout << endl;

        switch (a)
        {
            case 1:
            {
                bool ventaRealizada = venta();
                if(!ventaRealizada){
                regresar_al_menu = true;  
                return json();
                }
                break;
            }
            case 2:
            {
                ifstream f("productos.json");
                json productos = json::parse(f);
                limpiarPantalla();
                return archivo = productos;
            }
            case 3:
            {
                limpiarPantalla();
                regresar_al_menu = false;
                return json();

            }
            default:
            {
                limpiarPantalla();
                return json();
            }
        }
    }
    else if (usuario["categoria"] == "gerente")
    {
        limpiarPantalla();
        // El gerente puede acceder a tres archvios distintos
        cout << "Bienvenido gerente " << usuario["nombre"] << endl;
        cout << "Aviso: Para navegar por la interfaz use el teclado numerico." << endl;
        cout << endl << "Que desea revisar ?\n";
        cout << "1 - Carrito.\n";
        cout << "2 - Productos.\n";
        cout << "3 - Empleados.\n";
        cout << "4 - Historial de ventas.\n";
        cout << "5 - Regresar.\n";
        cin >> a;
        cout << endl;

        switch (a)
        {
            case 1:
            {
                bool ventaRealizada = venta();
                if(!ventaRealizada){
                regresar_al_menu = true;  
                return json();
                }
                break;
            }
            case 2:
            {
                ifstream f("productos.json");
                json productos = json::parse(f);
                limpiarPantalla();
                return archivo = productos;
            }
            case 3:
            {
                ifstream f("empleados.json");
                json empleados = json::parse(f);
                limpiarPantalla();
                return archivo = empleados;
            }
            case 4:
            {
                ifstream f("historial.json");
                json historial = json::parse(f);
                limpiarPantalla();
                return archivo = historial;
            }
            case 5:
            {
                limpiarPantalla();
                regresar_al_menu = false;
                return json();

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

json modificarDatos()
{
    string nombre_producto;
    string nombre_empleado;
    string password;
    string categoria;
    char confirmacion;
    int stock;
    int precio;
    int id_producto;
    int id_empleado;

    if (usuario["categoria"] == "gerente")
    {
        if (a == 2) // Productos
        {
            switch (b) // 1, 2, 3, 4 
            {
                case 1: 
                {
                    cout << "Nombre del producto: ";
                    cin.ignore();
                    getline(cin, nombre_producto);

                    cout << "ID del producto: ";
                    cin >> id_producto;

                    cout << "Cantidad del producto: ";
                    cin >> stock;

                    cout << "Precio unitario del producto: ";
                    cin >> precio;

                    json nuevo_producto = {
                        {"id", id_producto},
                        {"nombre", nombre_producto},
                        {"stock", stock},
                        {"precio", precio}
                    };

                    archivo["productos"].push_back(nuevo_producto);

                    //Guardamos el archivo
                    ofstream out("productos.json");
                    out << archivo.dump(4);
                    break;
                }
                case 2:
                {
                    cout << "Ingresa ID para eliminar: ";
                    cin >> id_producto;

                    bool encontrado = false;

                    // Principio apunta al principio de archivo["productos"] y mientras no llegue al final se le aumentara el valor para recorrer todo el archivo
                    for (auto principio = archivo["productos"].begin(); principio != archivo["productos"].end(); ++principio)
                    {

                        // *principio es como un puntero al elemento
                        if ((*principio)["id"] == id_producto)
                        {
                            encontrado = true;

                            cout << "Eliminar: " << (*principio)["nombre"] << endl;
                            cout << "Stock: " << (*principio)["stock"] << endl;

                            cout << "Cuantos quieres eliminar? ";
                            cin >> stock;

                            int disponible = (*principio)["stock"];

                            if (stock > disponible)
                            {
                                cout << "Advertencia, quieres eliminar todo el stock ?\n Esto eliminara el producto del inventario (s/n).\n";
                                cin >> confirmacion;

                                if (confirmacion == 's')
                                {
                                    archivo["productos"].erase(principio);
                                }

                            }
                            else if (stock == disponible)
                            {
                                cout << "Advertencia, quieres eliminar todo el stock ?\n Esto eliminara el producto del inventario (s/n).\n";
                                cin >> confirmacion;

                                if (confirmacion == 's')
                                {
                                    archivo["productos"].erase(principio);
                                }
                            }
                            else
                            {
                                (*principio)["stock"] = disponible - stock;
                                cout << "Se eliminaron " << stock << " unidades.\n";
                            }
                            break;
                        }
                    }
                    if (!encontrado)
                    {
                        cout << "No se encontro un producto con ese ID.\n";
                    }
                    ofstream out("productos.json");
                    out << archivo.dump(4);
                    break;
                }
                case 3: // Modificar
                {
                    cout << "Ingresa ID del producto a modificar: ";
                    cin >> id_producto;

                    bool encontrado = false;

                    for (auto& prod : archivo["productos"])
                    {
                        if (prod["id"] == id_producto)
                        {
                            encontrado = true;

                            cout << "Que deseas modificar?\n";
                            cout << "1 - Nombre\n";
                            cout << "2 - Stock\n";
                            cout << "3 - Precio\n";
                            cin >> c;
                            cin.ignore();  

                            switch (c)
                            {
                                case 1:
                                {
                                    string nuevoNombre;
                                    cout << "Nuevo nombre: ";
                                    getline(cin, nuevoNombre);
                                    prod["nombre"] = nuevoNombre;
                                    break;
                                }
                                case 2:
                                {
                                    int nuevoStock;
                                    cout << "Nuevo stock: ";
                                    cin >> nuevoStock;
                                    prod["stock"] = nuevoStock;
                                    break;
                                }
                                case 3:
                                {
                                    float nuevoPrecio;
                                    cout << "Nuevo precio: ";
                                    cin >> nuevoPrecio;
                                    prod["precio"] = nuevoPrecio;
                                    break;
                                }
                                default:
                                    cout << "Opcion no valida.\n";
                            }
                            break;
                        }
                    }

                    if (!encontrado)
                        cout << "No se encontro un producto con ese ID.\n";

                    ofstream out("productos.json");
                    out << archivo.dump(4);
                    break;
                }
                case 4:
                {
                    //Regresar
                    return json();
                    break;
                }
            }
        }
        else if (a == 3) // Empleados
        {
            switch (b) // 1, 2, 3, 4
            {
                case 1: 
                {
                    cout << "Nombre del empleado: ";
                    cin.ignore();
                    getline(cin, nombre_empleado);

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
                        {"nombre", nombre_empleado},
                        {"username", username},
                        {"password", password},
                        {"categoria", categoria}
                    };

                    archivo["empleados"].push_back(nuevo_empleado);
                    ofstream out("empleados.json");
                    out << archivo.dump(4);
                    
                    break;
                }
                case 2:
                {
                    cout << "Ingresa ID del empleado: \n";
                    cin >> id_empleado;

                    bool encontrado = false;

                    for (auto it = archivo["empleados"].begin(); it != archivo["empleados"].end(); ++it)
                    {
                        if ((*it)["id"] == id_empleado)
                        {
                            encontrado = true;

                            cout << "Dese eliminar al empleado: " << (*it)["nombre"] << " (s/n) ?" << endl;
                            cin >> confirmacion;

                            if (confirmacion == 's')
                            {
                                archivo["empleados"].erase(it);
                                cout << "Empleado eliminado.\n";
                            }
                            else
                            {
                                cout << "Cancelado.\n";
                            }
                            break;
                        }
                    }

                    if (!encontrado)
                        cout << "No se encontro un empleado con ese ID.\n";

                    ofstream out("empleados.json");
                    out << archivo.dump(4);
                    break;
                }
                case 3: 
                // Modificar
                {
                    cout << "Ingresa ID del empleado: ";
                    cin >> id_empleado;
                    cout << endl;

                    bool encontrado = false;

                    for (auto& emp : archivo["empleados"])
                    {
                        if (emp["id"] == id_empleado)
                        {
                            encontrado = true;

                            cout << "Que deseas modificar?\n";
                            cout << "1 - Nombre\n";
                            cout << "2 - Usuario\n";
                            cout << "3 - Categoria\n";
                            cout << "4 - Password\n";
                            cin >> c;
                            cout << endl;
                            cin.ignore();  

                            switch (c)
                            {
                                case 1:
                                {
                                    string nuevoNombre;
                                    cout << "Nuevo nombre: ";
                                    getline(cin, nuevoNombre);
                                    emp["nombre"] = nuevoNombre;
                                    break;
                                }
                                case 2:
                                {
                                    string nuevoUsuario;
                                    cout << "Nuevo usuario: ";
                                    cin >> nuevoUsuario;
                                    emp["username"] = nuevoUsuario;
                                    break;
                                }
                                case 3:
                                {
                                    string nuevaCategoria;
                                    cout << "Nueva categoria (gerente o empleado): ";
                                    cin >> nuevaCategoria;
                                    emp["categoria"] = nuevaCategoria;
                                    break;
                                }
                                case 4:
                                {
                                    string newPassword;
                                    cout << "Ingresa tu password actual: \n";
                                    cin >> newPassword;

                                    if (newPassword == emp["password"])
                                    {
                                        cout << "Correcto.";
                                        continue;
                                    }
                                    else if (newPassword != emp["pasword"])
                                    {
                                        cout << "Incorrecto. Intente de nuevo";
                                        pausa();
                                        break;
                                    }

                                    cout << "New Password: ";
                                    cin >> newPassword;

                                    emp["password"] = newPassword;
                                    break;
                                }
                                default:
                                    cout << "Opcion no valida.\n";
                            }
                            break;
                        }
                    }

                    if (!encontrado)
                    {
                        cout << "No se encontro a un empleado con ese ID.\n";
                    }
                    ofstream out("empleados.json");
                    out << archivo.dump(4);
                    break;
                }
                case 4:
                {
                    return json();
                    break;
                }
            }
        }
        else if (a == 4) //Historial de ventas
        {
            switch (b) // 1, 2, 3
            {
                case 1: 
                {
                    // Descargar
                    break;
                }
                case 2:
                {
                    // Imprimir
                    break;
                }
                case 3:
                {
                    // Borrar
                    break;
                }
                case 4:
                {
                    // Regresar
                    break;
                }
            }
        }
    }
    else if (usuario["categoria"] == "empleado")
    {
        if (a == 2)
        {
            switch (b) // 2
            {
                case 1:
                {
                    return json();
                    break;
                }
            }
        }
    }
    return json();
}


json seleccionarAccion()
{
    if (usuario["categoria"] == "gerente")
    {
        switch (a)
        {
            case 2:
            // Productos
            {
                mostrarArchvio();
                cout << "Que accion desea realizar ?\n";
                cout << "1 - Agregar producto.\n";
                cout << "2 - Eliminar producto.\n";
                cout << "3 - Modificar producto.\n";
                cout << "4 - Regresar.\n";
                cin >> b;
                cout << endl;
                break;
            }
            case 3: 
            // Empleados
            {
                mostrarArchvio();
                cout << "Que accion desea realizar ?\n";
                cout << "1 - Agregar empleado.\n";
                cout << "2 - Eliminar empleado.\n";
                cout << "3 - Modificar informacion del empleado.\n";
                cout << "4 - Regresar.\n";
                cin >> b;
                cout << endl;
                break;
            }
            case 4:
            // Historial de ventas
            {
                mostrarArchvio();
                cout << "Que accion desea realizar ?\n";
                cout << "1 - Descargar historial de venta.\n";
                cout << "2 - Imprimir historial de venta.\n";
                cout << "3 - Borrar historial de venta.\n";;
                cout << "4 - Regresar.\n";
                cin >> b;
                cout << endl;
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
        // Producto
        mostrarArchvio();
        cout << "1 - Regresar.\n";
        cout << endl;
        cin >> b;
    }
}

json verificarId()
{
    cout << "Iniciar Sesion\n";
    cout << "Username: ";
    cin >> username;
    cout << "Password: ";
    password = "";
    char ch;

    while ((ch = _getch()) != 13 && ch != 10) { 
        if (ch == 8) { 
            if (!password.empty()) {
                password.pop_back();
                cout << "\b \b";
            }
        } 
        else {
            password += ch;
            cout << '*';
        }
    }
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