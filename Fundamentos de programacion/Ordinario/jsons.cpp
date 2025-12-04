#include "jsons.hpp"
#include "general.hpp"
#include <fstream>

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

    if (usuario["categoria"] == "empleado" || usuario["categoria"] == "Empleado")
    {
        limpiarPantalla();
        // El empleado solo puede acceder a los productos, carrito y salir
        cout << "Bienvenido empleado " << usuario["nombre"] << '\n';
        cout << "Aviso: Para navegar por la interfaz use el teclado numerico.\n"
             << endl;
        cout << "Que desea hacer ?\n";
        cout << "1 - Carrito.\n";
        cout << "2 - Productos.\n";
        cout << "3 - Regresar.\n"
             << endl;
        cout << "Opcion: ";
        cin >> a;
        cout << endl;

        switch (a)
        {
        case 1:
        {
            bool ventaRealizada = venta();
            if (!ventaRealizada)
            {
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
    else if (usuario["categoria"] == "gerente" || usuario["categoria"] == "Gerente")
    {
        limpiarPantalla();
        // El gerente puede acceder a tres archvios distintos
        cout << "Bienvenido gerente " << usuario["nombre"] << endl;
        cout << "Aviso: Para navegar por la interfaz use el teclado numerico." << endl;
        cout << endl
             << "Que desea revisar ?\n";
        cout << "1 - Carrito.\n";
        cout << "2 - Productos.\n";
        cout << "3 - Empleados.\n";
        cout << "4 - Historial de ventas.\n";
        cout << "5 - Regresar.\n"
             << endl;
        cout << "Opcion: ";
        cin >> a;
        cout << endl;

        switch (a)
        {
        case 1:
        {
            bool ventaRealizada = venta();
            if (!ventaRealizada)
            {
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
    bool si_o_no = false;
    char confirmacion;
    int stock;
    int precio;
    bool id_valido=false;
    int id_producto;
    int id_empleado;

    if (usuario["categoria"] == "gerente" || usuario["categoria"] == "Gerente")
    {
        if (a == 2) // Productos
        {
            switch (b) // 1, 2, 3, 4
            {
            case 1:
            {
                cin.ignore();
                while (si_o_no == false)
                {
                    cout << "Nombre del producto: ";
                    getline(cin, nombre_producto);

                    if (nombre_producto.length() <= 0)
                    {
                        si_o_no = false;
                    }
                    else
                    {
                        si_o_no = true;
                    }
                }

                //verificacion
                id_valido=false;
                while(!id_valido){
                    cout << "ID del producto: ";
                    cin >> id_producto;

                    if(idProductoExiste(id_producto)){
                        cout<<"Error el id ya existe";
                    }
                    else{
                        id_valido=true;
                    }
                }


                cout << "Cantidad del producto: ";
                cin >> stock;

                cout << "Precio unitario del producto: ";
                cin >> precio;

                json nuevo_producto = {
                    {"id", id_producto},
                    {"nombre", nombre_producto},
                    {"stock", stock},
                    {"precio", precio}};

                archivo["productos"].push_back(nuevo_producto);

                // Guardamos el archivo
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
                        cout << endl;
                        int disponible = (*principio)["stock"];

                        if (stock > disponible)
                        {
                            cout << "Advertencia, quieres eliminar todo el stock ?\n"
                                << "Esto eliminara el producto del inventario (S/N).\n";
                            cin >> confirmacion;

                            if (confirmacion == 's' || confirmacion == 'S')
                            {
                                archivo["productos"].erase(principio);
                            }
                        }
                        else if (stock == disponible)
                        {
                            cout << "Advertencia, quieres eliminar todo el stock ?\n" 
                                << "Esto eliminara el producto del inventario (S/N).\n";
                            cin >> confirmacion;

                            if (confirmacion == 's' || confirmacion == 'S')
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

                for (auto &prod : archivo["productos"])
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
                            while (si_o_no == false)
                            {
                                cout << "Nuevo nombre: ";
                                getline(cin, nuevoNombre);

                                if (nuevoNombre.length() <= 0)
                                {
                                    si_o_no = false;
                                }
                                else
                                {
                                    si_o_no = true;
                                }
                            }
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
                // Regresar
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
                si_o_no = false;
                cin.ignore();
                while (si_o_no == false)
                {
                    cout << "Nombre del empleado: ";
                    getline(cin, nombre_empleado);

                    if (nombre_empleado.length() <= 0)
                    {
                        si_o_no = false;
                    }
                    else
                    {
                        si_o_no = true;
                    }
                }

                id_valido=false;
                while(!id_valido){
                cout << "ID del empleado: ";
                cin >> id_empleado;

                if(idEmpleadoExiste(id_empleado)){
                    cout<<"Error ya existe ese id";
                }
                else{
                    id_valido=true;
                }
                }

                si_o_no = false;

                cout << "Usuario del empleado: ";
                cin >> username;

                cout << "Password: ";
                cin >> password;

                while (si_o_no == false)
                {
                    cout << "Categoria (Gerente o Empleado): ";
                    cin >> categoria;
                    if (categoria == "gerente" || categoria == "Gerente" || categoria == "empleado" || categoria == "Empleado")
                    {
                        si_o_no = true;
                    }
                }

                json nuevo_empleado = {
                    {"id", id_empleado},
                    {"nombre", nombre_empleado},
                    {"username", username},
                    {"password", password},
                    {"categoria", categoria}};

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

                        cout << "Dese eliminar al empleado: " << (*it)["nombre"] << " (S/N) ?" << endl;
                        cin >> confirmacion;

                        if (confirmacion == 's' || confirmacion == 'S')
                        {
                            archivo["empleados"].erase(it);
                            cout << "Empleado eliminado.\n";
                        }
                        else
                        {
                            cout << "Cancelado.\n";
                            pausa();
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

                    for (auto &emp : archivo["empleados"])
                    {
                        if (emp["id"] == id_empleado)
                        {
                            encontrado = true;

                            cout << "Que deseas modificar?\n";
                            cout << "1 - Nombre\n";
                            cout << "2 - Usuario\n";
                            cout << "3 - Categoria\n";
                            cout << "4 - Password\n";
                            cout << "5 - Regresar\n"
                                 << endl;
                            cout << "Opcion: ";
                            cin >> c;
                            cout << endl;
                            cin.ignore();

                            switch (c)
                            {
                            case 1:
                            {
                                cin.ignore();
                                string nuevoNombre;
                                while (si_o_no == false)
                                {
                                    cout << "Nuevo nombre: ";
                                    getline(cin, nuevoNombre);

                                    if (nuevoNombre.length() <= 0)
                                    {
                                        si_o_no = false;
                                    }
                                    else
                                    {
                                        si_o_no = true;
                                    }
                                }
                                emp["nombre"] = nuevoNombre;
                                break;
                            }
                            case 2:
                            {
                                string nuevoUsuario;
                                cout << "Nuevo usuario: ";
                                getline(cin, nuevoUsuario);
                                emp["username"] = nuevoUsuario;
                                break;
                            }
                            case 3:
                            {
                                string nuevaCategoria;
                                bool si_o_no = false;
                                char confirmacion;

                                while (si_o_no == false)
                                {
                                    cout << "Nueva categoria (Gerente o Empleado): ";
                                    cin >> nuevaCategoria;
                                    if (nuevaCategoria == "gerente" || nuevaCategoria == "Gerente" || nuevaCategoria == "empleado" || nuevaCategoria == "Empleado")
                                    {
                                        si_o_no = true;
                                    }
                                }

                                cout << endl
                                     << "Esta seguro de cambiar de categoria a " << emp["nombre"] << " a la categoria de " << nuevaCategoria << " ? (S/N)" << endl;
                                cin >> confirmacion;

                                if (confirmacion == 'S' || confirmacion == 's')
                                {
                                    emp["categoria"] = nuevaCategoria;
                                }
                                break;
                            }
                            case 4:
                            {
                                string newPassword;
                                string newPassword1;
                                char confirmacion;

                                cout << "Ingresa tu password actual: \n";
                                cin >> newPassword;

                                if (newPassword == emp["password"])
                                {
                                    cout << "Correcto.\n" << endl;
                                }
                                else if (newPassword != emp["pasword"])
                                {
                                    cout << "Incorrecto. Intente de nuevo";
                                    pausa();
                                    break;
                                }

                                cout << "New Password: ";
                                cin >> newPassword;
                                cout << "Confirm password: ";
                                cin >> newPassword1;

                                if (newPassword1 == newPassword)
                                {
                                    cout << "Are you sure about to change the password ? (S/N)" << endl;
                                    cin >> confirmacion;

                                    if (confirmacion == 'S' || confirmacion == 's')
                                    {
                                        emp["password"] = newPassword;
                                    }
                                }
                                else
                                {
                                    cout << endl << "Passwords not match. Try Again" << endl;
                                    pausa();
                                }
                                break;
                            }
                            case 5:
                            {
                                return json();
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
        else if (a == 4) // Historial de ventas
        {
            switch (b) // 1, 2, 3
            {
            case 1:
            {
                return json();
                break;
            }
            }
        }
    }
    else if (usuario["categoria"] == "empleado" || usuario["categoria"] == "Empleado")
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
    if (usuario["categoria"] == "gerente" || usuario["categoria"] == "Gerente")
    {
        switch (a)
        {
        case 2:
            // Productos
            {
                mostrarArchivo();
                cout << "Que accion desea realizar ?\n";
                cout << "1 - Agregar producto.\n";
                cout << "2 - Eliminar producto.\n";
                cout << "3 - Modificar producto.\n";
                cout << "4 - Regresar.\n"
                     << endl;
                cout << "Opcion: ";
                cin >> b;
                cout << endl;
                break;
            }
        case 3:
            // Empleados
            {
                mostrarArchivo();
                cout << "Que accion desea realizar ?\n";
                cout << "1 - Agregar empleado.\n";
                cout << "2 - Eliminar empleado.\n";
                cout << "3 - Modificar informacion del empleado.\n";
                cout << "4 - Regresar.\n"
                     << endl;
                cout << "Opcion: ";
                cin >> b;
                cout << endl;
                break;
            }
        case 4:
            // Historial de ventas
            {
                mostrarArchivo();
                cout << "1 - Regresar.\n" << endl;
                cout << "Opcion: ";
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
    else if (usuario["categoria"] == "empleado" || usuario["categoria"] == "Empleado")
    {
        // Producto
        mostrarArchivo();
        cout << endl;
        cout << "1 - Regresar.\n";
        cout << endl;
        cout << "Opcion: ";
        cin >> b;
    }
}

json verificarId()
{
    cout << "Iniciar Sesion\n";
    cout << "Para salir del programa, use Ctrl + C\n"
         << endl;
    cout << "Username: ";
    cin >> username;
    cout << "Password: ";
    password = "";
    char ch;

    while ((ch = _getch()) != 13 && ch != 10)
    {
        if (ch == 8)
        {
            if (!password.empty())
            {
                password.pop_back();
                cout << "\b \b";
            }
        }
        else
        {
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
    for (auto &emp : empleados["empleados"])
    {
        if (username == emp["username"] && password == emp["password"])
        {
            return emp;
        }
    }
    return nullptr;
}

//Funciones
json verificarTarjeta()
{
    cout << "Datos de pago\n";
    cout << "Número de tarjeta: " << endl;
    cin >> nTarjeta;
    cout << "Nip: " << endl;
    cin >> nip;

    ifstream y("banco.json");
    json tarjetas = json::parse(y);

    for (auto &tarj : tarjetas["cuentas"])
    {
        if (nTarjeta == tarj["tarjeta"] && nip == tarj["nip"])
        {
            cout << "Tarjeta confirmada\n";
            cout << "Saldo: " << datos["cuentas"][i]["saldo"] << endl;
        } else
        {
            cout << "Tarjeta inexistente\n";
        }
        
    }
    return nullptr;
}