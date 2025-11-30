/* Ideas:
-Al momento de añadir el precio del producto agregar el IVA automaticamente (16%).
-Hacerle un hash las contraseñas
-Hacer una funcion que abra los JSON
-Hacer que el ID se coloque automaticamente
*/

/* Correciones
- Cuando vuelvo a llamar verificarId() la sesion no cambia
*/
#include <iostream>
#include <fstream>

#include <vector>
#include <iomanip>

#include <nlohmann/json.hpp>

using json = nlohmann::json;
using namespace std;

string username;
string password;
json archivo;
json usuario;
int a; // Seleccion de archivo
int b; // Seleccion de accion a realizar con los archivos
int pago=0; //Decide si se procede al pago

struct ItemCarrito{
    int id;
    string nombre;
    int cantidad;
    int precio;
};
vector<ItemCarrito>carrito;

//Lista
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

//Lista
json verificarId()
{
    cout << "Iniciar Sesion\n";
    cout << "Username: ";
    cin >> username;
    cout << "Password: ";
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

//Lista 
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
        // El empleado solo puede acceder a los productos y salir
        cout << "Bienvenido empleado " << usuario["nombre"] << endl;
        cout << "Que desea hacer ?\n";
        cout << "1 - Productos.\n";
        cout << "2 - Regresar.\n";
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
                limpiarPantalla();
                verificarId();
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
        cout << endl << "Que desea revisar ?\n";
        cout << "1 - Productos.\n";
        cout << "2 - Empleados.\n";
        cout << "3 - Historial de ventas.\n";
        cout << "4 - Regresar.\n";
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
            case 4:
            {
                // Regresar a la pantalla anterior
                limpiarPantalla();
                verificarId();
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


void mostrarArchvio()
{
    limpiarPantalla();

    if (usuario["categoria"] == "gerente")
    {
        switch (a)
        {
        case 1:
            // Producto
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
        case 2:
            // Empleado
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
        case 3:
            // Historial de ventas
            break;
        case 4:
        {
            limpiarPantalla();
            break;
        }
        default:
            break;
        }
    }
    else if (usuario["categoria"] == "empleado")
    {
        switch (a)
        {
            case 1:
            {
                // Producto
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
            case 2:
            {
                limpiarPantalla();
                verificarId();
            }
        }
    }
}


void seleccionarAccion()
{
    if (usuario["categoria"] == "gerente")
    {
        switch (a)
        {
        case 1:
        {
            mostrarArchvio();
            cout << "Que accion desea realizar ?\n";
            cout << "1 - Agregar producto.\n";
            cout << "2 - Eliminar producto.\n";
            cout << "3 - Modificar producto.\n";
            cout << "4 - Regresar.\n";
            cin >> b;
            limpiarPantalla();
            break;
        }
        case 2:
        {
            mostrarArchvio();
            cout << "Que accion desea realizar ?\n";
            cout << "1 - Agregar empleado.\n";
            cout << "2 - Eliminar empleado.\n";
            cout << "3 - Modificar informacion del empleado.\n";
            cout << "4 - Regresar.\n";
            cin >> b;
            limpiarPantalla();
            break;
        }
        case 3:
        {
            mostrarArchvio();
            cout << "Que accion desea realizar ?\n";
            cout << "1 - Descargar historial de venta.\n";
            cout << "2 - Imprimir historial de venta.\n";
            cout << "3 - Borrar historial de venta.\n";;
            cout << "4 - Regresar.\n";
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
        cout << "Que accion desea realizar ?\n";
        cout << "1 - Agregar producto.\n";
        cout << "2 - Eliminar producto.\n";
        cout << "3 - Modificar producto.\n";
        cout << "4 - Regresar";
        cin >> b;
        limpiarPantalla();
    }
}


json modificarDatos()
{
    string nombre_producto;
    string nombre_empleado;
    string password;
    string categoria;
    int stock;
    int precio;
    int id_producto;
    int id_empleado;

    if (usuario["categoria"] == "gerente")
    {
        if (a == 1) // Productos
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
                    // Eliminar
                    break;
                }
                case 3:
                {
                    // Modificar
                    break;
                }
                case 4:
                {
                    //Regresar
                    break;
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
                    // Eliminar
                    break;
                }
                case 3:
                {
                    // Modificar
                    break;
                }
                case 4:
                {
                    // Regresar
                    break;
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
                case 4:
                {
                    // Regresar
                    return;
                }
            }
        }
        else if (a == 4)
        {
            usuario = verificarId();
            return usuario;
        }
    }
    else if (usuario["categoria"] == "empleado")
    {
        if (a == 1)
        {
            switch (b) // 1, 2, 3, 4
            {
                case 1: 
                {
                    cout << "Nombre del producto: ";
                    cin >> nombre_producto;

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
                    // Eliminar
                    break;
                }
                case 3:
                {
                    // Modificar
                    break;
                }
                case 4:
                {
                    break;
                }
            }
        }
        else if (a == 2) // Carrito
        {
            switch (b) // 1, 2, 3, 4
            {
                case 1: 
                {
                    cout << "Nombre del producto: ";
                    cin >> nombre_producto;

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
                    // Eliminar
                    break;
                }
                case 3:
                {
                    // Modificar
                    break;
                }
                case 4:
                {
                    usuario = verificarId();
                    return usuario;
                }
            }
        }
    }
}


//Modulo de venta
bool venta(){
    int id;
    int cantidad;
    float subtotal=0;
    bool existe=false;
    bool pago=false;
    char confirmar;

    do{
        limpiarPantalla(); //Limpiar antes de volver a poner todos los datos
        subtotal=0;
        cout<<"Carrito:\n";

        if(carrito.empty()){ //Si esta vacio, cada vez que se inicia una venta
            cout<<"El carrito esta vacio\n";
        } 
        else{
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
                subtotal=subtotal+(item.cantidad * item.precio);
            }
        cout<<"\nSubtotal: $" <<subtotal <<"\n\n";
        }

        cout<<"1. Agregar producto\n";
        cout<<"2. Eliminar producto\n";
        cout<<"3. Proceder al pago\n";
        cout<<"4. Cancelar todo\n";
        cout<<"Selecciona una opcion: ";
        cin>>a;

        switch(a){
            case 1: {
                // Agregar producto
                cout << "Ingresa ID: ";
                cin >> id;

                ifstream f("productos.json"); //Buscar el producto en el Json
                json productos=json::parse(f);
                json productoEncontrado=nullptr;

                for(auto& pro : productos["productos"]){
                    if(pro["id"].get<int>()==id) {
                        productoEncontrado=pro;
                        break; //ya se encontro, se sale de aca
                    }
                }

                if (productoEncontrado==nullptr) {
                    cout<<"No existe ese producto\n"; //No hay en el Json eso
                    break;
                }

                cout<<"Ingresa cantidad: ";
                cin>>cantidad;

                int stockDisponible=productoEncontrado["stock"].get<int>(); //Validar que si se pueda agarrar esa cantidad
                if(cantidad>stockDisponible){
                    cout<<"Error: No hay suficiente stock\n";
                    cout<<"Stock disponible: "<<stockDisponible <<"\n";
                    cout<<"Cantidad solicitada: " <<cantidad <<"\n";
                    break; 
                }

                if(cantidad<=0){
                    cout<< "Error: La cantidad debe ser mayor a 0\n";
                    break;
                    }

                existe=false;
                for(auto& item : carrito){  //Si ya esta en el carrito se suma la cantidad del producto
                    if(item.id==id) {
                        item.cantidad=item.cantidad+cantidad;
                        existe=true;
                        break;
                    }
                }

                if (!existe){ //Si no existe se agrega al vector para mostrarlo
                    carrito.push_back({
                        id,
                        productoEncontrado["nombre"].get<string>(),
                        cantidad,
                        productoEncontrado["precio"].get<int>()
                    });
                }
                 break;
            }

            case 2: {
                //Eliminar producto
                if(carrito.empty()){ //Esta vacio y no se puede eliminar nada
                    cout<<"El carrito esta vacio\n";
                    break;
                }

                cout<<"Ingresa ID para eliminar: ";
                cin >>id;

                for(int i=0; i<carrito.size(); i++){
                    if(carrito[i].id==id){
                        carrito.erase(carrito.begin()+i); //.begin apunta al primer elemento del vector, se le suma la posición para eliminar el producto deseado
                        cout<<"Producto eliminado\n";
                        break;
                    }
                }
                break;
            }

            case 3: {
                 //Proceder al pago
                if(carrito.empty()){ //Carrito vacio no se hace nada
                    cout<<"El carrito esta vacio\n";
                    break;
                }

                cout<<"Confirmar compra(s/n): ";
                cin>>confirmar;

                if(confirmar=='s' || confirmar=='S'){ //Se actualiza el stock aca
                ifstream f("productos.json");   
                json productos= json::parse(f);

                for(auto& item : carrito){
                   for(auto& pro : productos["productos"]){
                      if (pro["id"].get<int>()== item.id){
                        int stockActual=pro["stock"].get<int>(); //para ver cuanto tiene ahora
                        pro["stock"]=stockActual-item.cantidad; //restarle la cantidad que se ocupo en el carrito
                        break;
                      }
                    }
                }

                ofstream o("productos.json");
                o << setw(4) << productos << endl; //Esto para mantener el mismo formato del json

                return pago=true;
                }
                else{
                    cout<<"Compra cancelada\n";
                }

                break;
            }

            case 4:
                //Cancelar todo
                carrito.clear();
                cout<<"Carrito vaciado\n";
                break;

            default:
            cout<<"Opción no valida\n";
            break;

        }

    }while(pago==false);
}


int main ()
{
    limpiarPantalla();
    
    usuario = verificarId();
    
    while (true)
    { 
        if (usuario.is_null()) {
            cout << "Informacion incorrecta. Intenta de nuevo.\n";
            continue;
        }

        archivo = abrirJson();

        if (archivo.is_null()) { 
            continue;
        }

        mostrarArchvio();
    }
}