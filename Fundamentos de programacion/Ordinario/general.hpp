#ifndef GENERAL_HPP
#define GENERAL_HPP

#include <iostream>
#include <string>
#include <conio.h>
#include "jsons.hpp"
#include "nlohmann/json.hpp"

using json = nlohmann::json;
using namespace std;

// Variables Globales
extern json archivo;
extern json usuario;
extern int a; // Seleccion de archivo
extern bool regresar_al_menu;
extern string username;
extern string password;
extern int b; // Seleccion de accion a realizar con los archivos
extern int c;
extern bool sesion_iniciada;
extern int error;
extern int d; //seleccion de metodo de pago
extern char e;
extern int dineroEf;
extern float cambio;
extern float total;
extern float dineroFalt;
extern int diferencia;
extern bool banderaCambio;
extern int f;
extern int nTarjeta;
extern int nip;
extern float saldo;
extern int id_producto;
extern int id_empleado;
extern bool coincide;

struct ItemCarrito
{
    int id;
    string nombre;
    int cantidad;
    int precio;
};

extern vector<ItemCarrito>carrito;

// Funciones
void limpiarPantalla();
void pausa();
void mostrarArchivo();
void guardarEnHistorial(float subtotal);
void nuevoDia();
bool idEmpleadoExiste(int id_empleado);
bool idProductoExiste(int id_producto);
int validarMayorACero();
#endif