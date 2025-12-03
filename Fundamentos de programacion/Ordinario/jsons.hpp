#ifndef FUNCIONES_HPP
#define FUNCIONES_HPP

#include <iostream>
#include <string>
#include "json.hpp"

using json = nlohmann::json;
using namespace std;

// Variables globales
json archivo;
json usuario;

// Funciones
json verificarId();
json seleccionarAccion();
json modificarDatos();
json abrirJson();

#endif