#include "general.hpp"
#include "jsons.hpp"
#include <fstream>


// Funciones
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

void pausa(){
    cout<<"Enter para continuar";
    char ch;
    while((ch = _getch()) != 13 && ch != 10){
    }
    cout<<endl;
}

void mostrarArchivo()
{
    limpiarPantalla();

    if (usuario["categoria"] == "gerente" || usuario["categoria"] == "Gerente")
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
                << setw(15) << "Precio"
                << "\n";
            cout<< string(66, '-') << "\n";

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
            cout << setw(15) << "Categoria";
            cout <<"\n";
            cout << string(62, '-') << endl;

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
            cout<<string(80,'-')<<"\n";
            
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
    else if (usuario["categoria"] == "empleado" || usuario["categoria"] == "Empleado")
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
                    << setw(15) << "Precio"
                    << "\n";
                cout << string(66, '-') << "\n";

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

void guardarEnHistorial(float total)
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
    venta["total"] = total;
    venta["productos"] = json::array();

    for (const auto& item : carrito) // Agregarlo
    {
        json producto;
        producto["id"] = item.id;
        producto["nombre"] = item.nombre;
        producto["cantidad"] = item.cantidad;
        producto["precio_unitario"] = item.precio;
        producto["total"] = item.cantidad * item.precio;
        venta["productos"].push_back(producto);
    }
    historial["ventas"].push_back(venta);
    ofstream o("historial.json");
    o<<setw(4) << historial << endl; // Ponerlo en orden

    cout << "Venta guardada\n";
}

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

bool idProductoExiste(int id_producto) {
    ifstream f("productos.json");
    if(!f.good()) return false; // Si el archivo no existe pues el id no existe tampoco
    
    json productos=json::parse(f);
    
    for(auto& producto : productos["productos"]){
        if(producto["id"].get<int>() == id_producto){
            return true; // ID encontrado
        }
    }
    return false; // ID no encontrado
}

bool idEmpleadoExiste(int id_empleado) {
    ifstream f("empleados.json");
    if(!f.good()) return false; // Si el archivo no existe pues el id no existe tampoco
    
    json empleados=json::parse(f);
    
    for(auto& empleado : empleados["empleados"]){
        if (empleado["id"].get<int>() == id_empleado) {
            return true; // ID encontrado
        }
    }
    return false; // ID no encontrado
}

int validarMayorACero(){
    int valor;
    while(true) {
        cin >> valor;
        /* if(cin.fail()){  //por si escribe letras 
            cin.clear();  
            cin.ignore(numeric_limits<streamsize>::max(), '\n');  //limpia
            cout << "Error; debe ingresar un numero\n";
        } */
        if (valor<=0){
            cout<<"Error, debe ser mayor a 0\n";
        } 
        else{
            return valor;
        }
    }
}