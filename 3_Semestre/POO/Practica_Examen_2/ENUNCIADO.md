# PRÁCTICA — AutoExpress (Sistema de Renta de Vehículos)

Contexto: **AutoExpress** es una rentadora de autos. El programador anterior dejó el
sistema a medias. Debes repararlo aplicando **Encapsulamiento, Constructores/Sobrecarga
y Relaciones entre Objetos (Composición y Agregación)**, igual que en el examen.

Los archivos base están en la carpeta `AutoExpress/` (código incompleto, con TODOs).

---

## Ticket 1: Encapsulamiento — get / set
En la clase `Cliente`, el atributo `Saldo` está público. Un cliente se puso saldo
negativo y crasheó el sistema.

**Tu tarea:** Encapsula `Saldo`. Crea el campo privado y la propiedad pública.
Regla: el saldo nunca puede ser menor a $0. Si alguien intenta poner un saldo
negativo, asígnale 0.

## Ticket 2: Constructores y Sobrecarga
En la clase `Cliente`, necesitamos registrar clientes de dos formas:

1. Uno que solo reciba el `nombre` (por defecto, `Saldo` inicia en $0).
2. Otro que reciba el `nombre` y un `saldoInicial` (para promociones).

## Ticket 3: Composición
Todo cliente recibe automáticamente un seguro básico vinculado a su cuenta. Si el
cliente se elimina, el seguro desaparece con él.

**Tu tarea:** En `Cliente` ya existe el atributo `MiSeguro` (tipo `Seguro`).
Inicialízalo (`new Seguro()`) dentro de los dos constructores del Ticket 2.

## Ticket 4: Agregación
Una sucursal (clase `AutoExpress`) tiene muchos vehículos disponibles, pero los
vehículos se compran por fuera (existen independientemente de la sucursal).

**Tu tarea:** En `AutoExpress`, crea una lista de tipo `Vehiculo` llamada `Flota`.
Inicialízala en el constructor de `AutoExpress`, y crea un método
`AgregarVehiculo(Vehiculo nuevo)` que guarde los vehículos en esa lista.

## Ticket 5: Asociación
La sucursal solo administra el proceso, uniendo a un `Cliente` con un `Vehiculo`.

**Tu tarea:** Completa el método `RentarVehiculo` en `AutoExpress`. Recibe un
`Cliente`, un `Vehiculo` y los días a rentar.

- Calcula el total (`PrecioPorDia * dias`).
- Réstale ese total al `Saldo` del cliente.
- Imprime un recibo, ej: `"Laura rentó Toyota Corolla por 3 días. Saldo restante: $60"`.

---

### Cómo probarlo
`Program.cs` ya intenta usar todo esto (registra clientes, agrega vehículos y renta).
Si armaste bien las 5 clases, correrá sin errores y el último renglón mostrará que a
"Laura" no le queda saldo negativo aunque intente rentar más de lo que tiene.

> Tip de estudio: no copies el código del examen. Ciérralo, mira solo este enunciado,
> y escribe las 5 clases desde cero. Compáralo después con tu versión del examen para
> ver si el patrón te quedó claro.
