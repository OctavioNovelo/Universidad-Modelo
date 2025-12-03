#ifndef FUNCIONES_HPP
#define FUNCIONES_HPP

#include "nlohmann/json.hpp"
#include "general.hpp"

using json = nlohmann::json;

// Funciones
json verificarId();
json seleccionarAccion();
json modificarDatos();
json abrirJson();
bool venta();

#endif