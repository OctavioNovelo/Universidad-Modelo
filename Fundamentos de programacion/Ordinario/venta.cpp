#include "venta.hpp"
#include "general.hpp"
#include <vector>
#include <fstream>
#include "jsons.hpp"

float propina(float subtotal)
{
    float propPersonalizada;
    int propina;

    cout << "Gracias! Ingresa tu porcentaje de propina\n";
    cout << "1. 10%\n";
    cout << "2. 15%\n";
    cout << "3. Propina personalizada\n";
    cin >> propina;

    switch (propina)
    {
    case 1:
        total = subtotal+(subtotal)*(0.1);
        break;

    case 2:
        total = subtotal+(subtotal)*(0.15);
        break;

    case 3:
        cout << "Ingresa la cantidad: $";
        cin >> propPersonalizada;
        if (propPersonalizada <= 0) {
            cout << endl << "No se agrego propina a la cuenta total\n";
            total = subtotal;
        } else {
            total = subtotal + propPersonalizada;
        }            
        break;
    
    default:
        cout << "Error. Selecciona una opcion valida \n";
        break;
    }
    return total;
}


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

                limpiarPantalla();
                
                cout << "Tu subtotal es de $" << subtotal << endl;

                cout << "Selecciona tu metodo de pago: \n"; 
                cout << "1. Pago en efectivo\n";
                cout << "2. Pago por tarjeta\n";
                cout << "3. Regresar\n";
                cin >> d;

                switch (d) 
                {
                    case 1:
                    {
                        cout << "Le gustaria dejar propina?(s/n): ";
                        cin >> e;

                        if ((e == 's') || (e == 'S')) {
                            total = propina(subtotal);
                            cout << "Tu total es de $" << total << endl;
                        } else if ((e == 'n') || (e == 'N')) {
                            total = subtotal;
                            cout << "Tu total es de $" << total << endl;
                        } else {
                            cout << "Respuesta no valida";
                            pausa();
                        }

                        while (banderaCambio==false)
                        {
                        cout << endl << "Ingresa el dinero: $";
                        cin >> dineroEf;
                        dineroEf = dineroEf + cambio;

                          if (dineroEf >= total) {
                            if (dineroEf == total) {
                                cout << "El pago ha sido realizado correctamente\n";
                                banderaCambio = true;
                                carrito.clear();
                                pausa();
                                } else if (dineroEf > total) {
                                    cambio = dineroEf - total;
                                    cout << "El pago ha sido realizado correctamente\n";
                                    cout << "Tu cambio es de $" << cambio << endl;
                                    banderaCambio = true;
                                    pausa();
                                }
                            } else
                            {
                                if ((dineroEf < total) && (dineroEf > 0))
                                {
                                    dineroFalt = total - dineroEf;
                                    cout << "Saldo insuficiente. Faltan $" << dineroFalt << endl;
                                    cambio = dineroEf;
                                } else
                                {
                                    cout << "Error. Ingresa una cantidad positiva\n";
                                    pausa();
                                }
                            }  
                        }
                        break;
                    }
                    case 2:
                    {
                        cout << "Le gustaria dejar propina?(s/n): ";
                        cin >> e;

                        if ((e == 's') || (e == 'S')) {
                            total = propina(subtotal);
                            cout << "Tu total es de $" << total << endl;
                        } else if ((e == 'n') || (e == 'N')) {
                            total = subtotal;
                            cout << "Tu total es de $" << total << endl;
                        } else {
                            cout << "Respuesta no valida";
                            pausa();
                        }

                        cout << "Selecciona una opcion \n";
                        cout << "1. Pagar con tarjeta existente\n";
                        cout << "2. Regresar \n";
                        cin >> f;

                        switch (f)
                        {
                        case 1:
                        {
                            verificarTarjeta();
                            pausa();
                            break;
                        }

                        case 2:
                        {
                            carrito.clear();
                            regresar_al_menu = true;
                            return pago = true;
                        }
                            
                        default:
                        {
                            cout << "Error. Ingresa una opcion valida";
                            pausa();
                            break;
                        }
                        }

                        break;
                    }
                    case 3:
                    {
                        carrito.clear();
                        regresar_al_menu = true;
                        return pago = true;
                    }
                } 
                
                guardarEnHistorial(total); // Para el historial
                ifstream f("productos.json");   
                json productos= json::parse(f);
                
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
                cout<<"Seguro que desea regresar?";
                cin >> confirmar;
                if(confirmar=='s' || confirmar=='S'){
                carrito.clear();
                regresar_al_menu = true;
                return false;
                }
                else{
                    break;
                }

            }
            default:
            cout << "Opcion no valida\n";
            break;

        }

    } while (pago == false);
    return pago;

}