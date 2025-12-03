/* Ideas:
-Al momento de añadir el precio del producto agregar el IVA automaticamente (16%).
-Hacerle un hash las contraseñas.
-Hacer que el ID se coloque automaticamente.
*/

/* Correciones

*/

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <limits>

#include <iomanip>
#include <conio.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;
using namespace std;

// Declaracion de las funciones
// Octavio
string username;
string password;
json archivo;
json usuario;
int a; // Seleccion de archivo
int b; // Seleccion de accion a realizar con los archivos
int c;
bool sesion_iniciada=false;
int error=0;
bool regresar_al_menu=false; 

// Declaracion de las funciones
// Litzy
void guardarEnHistorial(float subtotal);
void nuevoDia();
bool venta();

// Declaracion de las funciones
// Aili
int d; //seleccion de metodo de pago
char e;
int dineroEf;
float cambio;
float total;
float dineroFalt;
int diferencia;

// Check
struct ItemCarrito
{
    int id;
    string nombre;
    int cantidad;
    int precio;
};


// El carrito
vector<ItemCarrito>carrito;


// Check
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


// Check
void pausa(){
    cout<<"Enter para continuar";
    char ch;
    while((ch = _getch()) != 13 && ch != 10){
    }
    cout<<endl;
}


// Check
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


// Check
void mostrarArchvio()
{
    limpiarPantalla();

    if (usuario["categoria"] == "gerente")
    {
        switch (a)
        {
        case 2:
        // Producto
        {
            cout << left
                << setw(5) << "ID"
                << setw(30) << "Nombre"
                << setw(15) << "Cantidad"
                << setw(15) << "Precio\n"
                << string(75, '-') << '\n';

            for (auto& pro : archivo["productos"])
            {
                cout << left;
                cout << setw(5) << pro["id"].get<int>();
                cout << setw(30) << pro["nombre"].get<string>();
                cout << setw(15) << pro["stock"].get<int>();
                cout << setw(15) << pro["precio"].get<int>();
                cout << "\n";
            }

            cout << endl;
            break;
        }
        case 3:
        // Empleado
        {
            cout << left;
            cout << setw(5) << "ID";
            cout << setw(10) << "Usuario";
            cout << setw(30) << "Nombre";
            cout << setw(15) << "Categoria\n";
            cout << string(75, '-') << endl;

            for (auto& emp : archivo["empleados"])
            {
                cout << setw(5) << emp["id"].get<int>();
                cout << setw(10) << emp["username"].get<string>();
                cout << setw(30) << emp["nombre"].get<string>();
                cout << setw(15) << emp["categoria"].get<string>();
                cout << '\n';
            }

            cout << endl;
            break;
        }
        case 4:
        // Historial de ventas
        {
            cout<<"Historial de ventas\n";
            cout<<string(80, '=') << endl;

            ifstream f("historial.json");
            if(!f.good()){ //no exite el archivo?
                cout<<"No hay historial de ventas\n";
                break;
            }
            f.seekg(0, ios::end);
            if(f.tellg() == 0){ //esta vacio
                cout<<"No hay ventas registradas\n";
                break;
            }

            f.seekg(0, ios::beg);
            json historial=json::parse(f);

            if(historial["ventas"].empty()){
                cout<<"No hay ventas registradas en el historial\n";
                break;
            }

            cout<<left
            <<setw(12) <<"Sesion"
            <<setw(15) <<"Total"
            <<setw(10) <<"Productos"
            <<setw(40) <<"Detalles"
            <<"\n";
            cout<<string(77,'-')<<"\n";
            
            for(auto& venta : historial["ventas"]){
                cout<<setw(12) <<venta["sesion"].get<string>();
                cout<<setw(15) <<"$" + to_string((int)venta["total"].get<float>());
                cout<<setw(10) <<venta["productos"].size();
                string detalles = "";
                for(auto& producto : venta["productos"]){
                    detalles += to_string(producto["cantidad"].get<int>()) + "x " + 
                    producto["nombre"].get<string>() + ", ";
                }
                cout<<setw(40) <<detalles;
                cout<<"\n";
            }
            cout<<endl;
            break; 
        }
        default:
        {
            break;
        }
        }
    }
    else if (usuario["categoria"] == "empleado")
    {
        switch (a)
        {
            case 2:
            // Producto
            {
                cout << left
                    << setw(5) << "ID"
                    << setw(30) << "Nombre"
                    << setw(15) << "Cantidad"
                    << setw(15) << "Precio\n"
                    << string(75, '-') << '\n';

                for (auto& pro : archivo["productos"])
                {
                    cout << left;
                    cout << setw(5) << pro["id"].get<int>();
                    cout << setw(30) << pro["nombre"].get<string>();
                    cout << setw(15) << pro["stock"].get<int>();
                    cout << setw(15) << pro["precio"].get<int>();
                    cout << "\n";
                }

                cout << endl;
                break;
            }
            default:
            {
                break;
            }
        }
    }
}


// Check
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
        cout << "Que accion desea realizar ?\n";
        cout << "1 - Agregar producto.\n";
        cout << "2 - Eliminar producto.\n";
        cout << "3 - Modificar producto.\n";
        cout << "4 - Regresar.\n";
        cout << endl;
        cin >> b;
    }
}


// Check
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

                    json nuevo_objeto = {
                        {"nombre", nombre_producto},
                        {"id", id_producto},
                        {"stock", stock},
                        {"precio", precio}
                    };

                    archivo["productos"].push_back(nuevo_objeto);

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

                            cout << "Qué deseas modificar?\n";
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
                    return json();
                    break;
                }
            }
        }
    }
    return json();
}

// Propina
float propina(float subtotal)
{
    float propPersonalizada;
    int propina;

    cout << "Gracias! Ingresa tu porcentaje de propina\n";
    cout << "1. 10%\n";
    cout << "2. 15%";
    cout << "3. Propina personalizada";
    cin >> propina;

    switch (propina)
    {
    case 1:
        total = (subtotal)*(0.9);
        break;

    case 2:
        total = (subtotal)*(0.85);
        break;

    case 3:
        cout << "Ingresa la cantidad";
        cin >> propPersonalizada;
        total = subtotal + propPersonalizada;
        if (propPersonalizada <= 0) {
            cout << "No se agregó propina a la cuenta total";
            total = subtotal;
        } else {
            total = subtotal + propPersonalizada;
        }            
        break;
    
    default:
        cout << "Error. Selecciona una opción válida";
        break;
    }
    return total;
}

// Check
bool venta()
{
    int id;
    int cantidad;
    float subtotal = 0;
    bool existe = false;
    bool pago = false;
    char confirmar;
    bool encontrado = false;

    do
    {
        limpiarPantalla(); //Limpiar antes de volver a poner todos los datos
        subtotal = 0;
        cout << "Carrito:\n" << endl;

        if(carrito.empty()) //Si esta vacio, cada vez que se inicia una venta
        { 
            cout << "El carrito esta vacio\n" << endl;
        } 
        else
        {
            cout << left //Tabla
                << setw(5) << "ID"
                << setw(30) << "Nombre"
                << setw(15) << "Cantidad"
                << setw(15) << "Precio\n"
                << string(75, '-') << '\n';

            for (const auto& item : carrito) {
                cout << setw(5) << item.id;
                cout << setw(30) << item.nombre;
                cout << setw(15) << item.cantidad; //Checar cantidad importante
                cout << setw(15) << item.precio;
                cout << "\n";
                subtotal = subtotal + (item.cantidad * item.precio);
            }
            cout << "\nSubtotal: $" << subtotal << "\n\n";
        }

        cout << "1. Agregar producto\n";
        cout << "2. Eliminar producto\n";
        cout << "3. Proceder al pago\n";
        cout << "4. Cancelar todo\n";
        cout << "5. Regresar\n";
        cout << "Selecciona una opcion: ";
        cin >> a;

        switch(a)
        {
            case 1: 
            {
                // Agregar producto
                cout << "Ingresa ID: ";
                cin >> id;

                ifstream f("productos.json"); // Buscar el producto en el Json
                json productos=json::parse(f);
                json productoEncontrado=nullptr;

                for (auto& pro : productos["productos"])
                {
                    if (pro["id"].get<int>()==id)
                    {
                        productoEncontrado=pro;
                        break; // Ya se encontro, se sale de aca
                    }
                }

                if (productoEncontrado==nullptr)
                {
                    cout << "No existe ese producto\n"; // No hay en el Json eso
                    pausa();
                    break;
                }

                cout << "Ingresa cantidad: ";
                cin >> cantidad;

                int stockDisponible=productoEncontrado["stock"].get<int>(); // Validar que si se pueda agarrar esa cantidad
                if (cantidad>stockDisponible)
                {
                    cout << "Error: No hay suficiente stock\n";
                    cout << "Stock disponible: "<< stockDisponible << "\n";
                    cout << "Cantidad solicitada: " << cantidad << "\n";
                    pausa();
                    break; 
                }

                if (cantidad <= 0)
                {
                    cout << "Error: La cantidad debe ser mayor a 0\n";
                    pausa();
                    break;
                    }

                existe = false;
                for (auto& item : carrito)  // Si ya esta en el carrito se suma la cantidad del producto
                {
                    if (item.id==id)
                    {
                        item.cantidad = item.cantidad + cantidad;
                        existe = true;
                        break;
                    }
                }

                if (!existe)  // Si no existe se agrega al vector para mostrarlo
                {
                    carrito.push_back(
                        {
                        id,
                        productoEncontrado["nombre"].get<string>(),
                        cantidad,
                        productoEncontrado["precio"].get<int>()
                    }
                    );
                }
                 break;
            }
            case 2:
            {
                // Eliminar producto
                if (carrito.empty())
                { // Esta vacio y no se puede eliminar nada
                    cout << "El carrito esta vacio\n";
                    pausa();
                    break;
                }

                cout << "Ingresa ID para eliminar: ";
                cin >> id;

                
                for (int i=0; i<carrito.size(); i++)
                {
                    if (carrito[i].id == id)
                    {
                    encontrado = true;
                    cout << "Producto: " << carrito[i].nombre << endl;
                    cout << "Cantidad actual en carrito: " << carrito[i].cantidad << endl;
                    cout << "Cuantos quieres eliminar? ";
                    cin >> cantidad;

                    if (cantidad <= 0)
                    {
                        cout << "Error, la cantidad debe ser mayor a 0\n";
                        pausa();
                        break;
                    }

                    if (cantidad > carrito[i].cantidad)
                    {
                        cout << "Error, no puedes eliminar mss de lo que hay en el carrito\n";
                        cout << "Maximo a eliminar: " << carrito[i].cantidad << endl;
                        pausa();
                        break;
                    }

                    if(cantidad == carrito[i].cantidad) // Si elimina todo
                    {
                        carrito.erase(carrito.begin()+i); // .begin apunta al primer elemento del vector, se le suma la posición para eliminar el producto deseado
                        cout << "Producto eliminado\n";
                    }
                    else 
                    {
                       carrito[i].cantidad -= cantidad;
                       cout << "Se eliminaron " << cantidad << "unidades\n";
                    }

                    break;

                    }
                }
                if (!encontrado)
                {
                    cout << "Producto no encontrado en el carrito\n";
                    pausa();
                }

                break;
            }

            case 3:
            {
                // Proceder al pago
                if (carrito.empty()) // Carrito vacio no se hace nada
                {
                    cout << "El carrito esta vacio\n";
                    pausa();
                    break;
                }

                cout << "Confirmar compra(s/n): ";
                cin >> confirmar;

                if (confirmar=='s' || confirmar=='S') // Se actualiza el stock aca
                {
                guardarEnHistorial(subtotal); // Para el historial
                ifstream f("productos.json");   
                json productos= json::parse(f);

                cout << "Selecciona tu metodo de pago\n";
                cout << "1. Pago en efectivo\n";
                cout << "2. Pago por tarjeta\n";

                switch (d) 
                {
                    case 1:
                    {
                        cout << "Le gustaría dejar propina?(s/n)\n";
                        cin >> e;

                        if ((e == 's') || (e == 'S')) {
                            float total = propina(subtotal);
                            std::cout << "Tu total es de $" << total;
                        } else if ((e == 'n') || (e == 'N')) {
                        } else {
                            cout << "Respuesta no válida";
                            return pago = true;
                        }

                        cout << "Ingresa el dinero";
                        cin >> dineroEf;

                        if (dineroEf >= total) {
                            if (dineroEf == total) {
                                cout << "El pago ha sido realizado correctamente\n";
                            } else if (dineroEf > total) {
                                cambio = dineroEf - total;
                                cout << "El pago ha sido realizado correctamente\n";
                                cout << "Tu cambio es de $" << cambio;
                            }
                        } else {
                            for (int i = 0; i >= total; i++) 
                            {
                                dineroFalt = total - dineroEf;
                                cout << "Saldo insuficiente. Faltan $" << dineroFalt;
                                cin >> diferencia;
                                dineroEf = dineroEf + diferencia;        
                            }
                        }
                        break;
                    }

                    case 2:
                    {
                        break;
                    }
                }

                for (auto& item : carrito)
                {
                   for(auto& pro : productos["productos"])
                   {
                      if (pro["id"].get<int>()== item.id)
                      {
                        int stockActual = pro["stock"].get<int>(); // Para ver cuanto tiene ahora
                        pro["stock"] = stockActual-item.cantidad; // Restarle la cantidad que se ocupo en el carrito
                        break;
                      }
                    }
                }

                ofstream o("productos.json");
                o << setw(4) << productos << endl; // Esto para mantener el mismo formato del json

                carrito.clear();
                regresar_al_menu = true;
                return pago = true;
                }
                else
                {
                    cout << "Compra cancelada\n";
                }

                break;
            }

            case 4:
            {
                // Cancelar todo
                carrito.clear();
                cout << "Carrito vaciado\n";
                break;
            }
            case 5:
            {
                carrito.clear();
                regresar_al_menu = true;
                return false;

            }
            default:
            cout << "Opcion no valida\n";
            break;

        }

    } while (pago == false);
}


// Check
void guardarEnHistorial(float subtotal)
{
    int sesion_actual;
    json historial;
    ifstream f("historial.json");

    if(f.good())
    {
        f.seekg(0, ios::end);
        if(f.tellg() == 0)
        {
            historial["ventas"]=json::array();
            historial["ultima_sesion"]=1;
        } 
        else
        {
            f.seekg(0, ios::beg);
            historial=json::parse(f);
        }
    }
    else
    {
        historial["ventas"] = json::array();
        historial["ultima_sesion"] = 1;
    }

    if (historial.contains("ultima_sesion")) // Checar la sesion en la que esta
    {
        sesion_actual = historial["ultima_sesion"].get<int>();
    } 
    else
    {
        sesion_actual=1;
        historial["ultima_sesion"] = sesion_actual;
    }

    json venta;
    venta["sesion"] = "Sesion "+ to_string(sesion_actual);
    venta["total"] = subtotal;
    venta["productos"] = json::array();

    for (const auto& item : carrito) // Agregarlo
    {
        json producto;
        producto["id"] = item.id;
        producto["nombre"] = item.nombre;
        producto["cantidad"] = item.cantidad;
        producto["precio_unitario"] = item.precio;
        producto["subtotal"] = item.cantidad * item.precio;
        venta["productos"].push_back(producto);
    }
    historial["ventas"].push_back(venta);
    ofstream o("historial.json");
    o<<setw(4) << historial << endl; // Ponerlo en orden

    cout << "Venta guardada\n";
}


// Check
void nuevoDia()
{
    if (sesion_iniciada)
    {
        return; 
    }

    json historial;
    ifstream f("historial.json");
    if (f.good())
    {
        f.seekg(0, ios::end);
        if(f.tellg()==0) // Vacio
        {
            historial["ventas"]=json::array();
            historial["ultima_sesion"] = 0;
        }
        else
        {
            f.seekg(0, ios::beg);
            historial=json::parse(f);
        }
    }
    else
    {
        historial["ventas"]=json::array();
        historial["ultima_sesion"] = 1;
    }

    if (historial.contains("ultima_sesion"))
    {
        int ultima_sesion = historial["ultima_sesion"].get<int>();
        historial["ultima_sesion"] = ultima_sesion+1;
    } 
    else
    {
        historial["ultima_sesion"] = 1;
    }

    ofstream o("historial.json");
    o<<setw(4) << historial << endl;
    sesion_iniciada = true;
}


// Check
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


// Check
int main ()
{
    while (true)  
    {
        error = 0;  
        limpiarPantalla();

        do
        {
            limpiarPantalla();
            if(error >= 1)
            {
                cout<<"Informacion incorrecta. Intenta de nuevo.\n";
            }

            usuario = verificarId();
        
            if (usuario.is_null())
            {
                error++;
                cin.ignore(numeric_limits<streamsize>::max(), '\n');
            }

        } while (usuario.is_null());

        nuevoDia();
        
        while (true)
        { 
            archivo = abrirJson();

            if (archivo.is_null())
            { 
               if (regresar_al_menu)
               {
               regresar_al_menu = false;  
               continue;                  
               }   
               else
               {
               break;  // Volver al login
               } 
            }
            mostrarArchvio();
            seleccionarAccion();
            modificarDatos();
        }
    }
}