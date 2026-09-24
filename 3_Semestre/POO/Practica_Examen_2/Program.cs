using System;

class Program
{
    static void Main()
    {
        AutoExpress renta = new AutoExpress("AutoExpress Centro");

        Vehiculo auto1 = new Vehiculo("Toyota Corolla", 20.0);
        Vehiculo auto2 = new Vehiculo("Jeep Wrangler 4x4", 45.0);

        renta.AgregarVehiculo(auto1);
        renta.AgregarVehiculo(auto2);

        Cliente cliente1 = new Cliente("Laura");
        cliente1._saldo = 100;

        Cliente cliente2 = new Cliente("Marco", 400);

        Console.WriteLine("--- Sistema de Rentas AutoExpress ---");
        renta.RentarVehiculo(cliente1, auto1, 3);
        renta.RentarVehiculo(cliente2, auto2, 2);

        Console.WriteLine("\n--- Prueba de Seguridad ---");
        renta.RentarVehiculo(cliente1, auto1, 10);
    }
}
