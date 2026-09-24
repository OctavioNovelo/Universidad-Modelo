using System.Collections.Generic;
using System.IO.Compression;
using System.Runtime.Intrinsics.X86;

public class AutoExpress
{
    public string NombreSucursal;

    // TODO Ticket 4: crea aquí la lista "Flota" de tipo Vehiculo.
    List<Vehiculo> Flota;

    public AutoExpress(string nombre)
    {
        NombreSucursal = nombre;
        Flota = new List<Vehiculo>();
        // TODO Ticket 4: inicializa Flota en este constructor.
    }

    // TODO Ticket 4: método AgregarVehiculo(Vehiculo nuevo) que lo guarde en Flota.
    public void AgregarVehiculo(Vehiculo a)
    {
        Flota.Add(a);
    }


    public void RentarVehiculo(Cliente cliente, Vehiculo auto, int dias)
    {
        // TODO Ticket 5:
        // 1. Calcula el total (PrecioPorDia * dias).
        // 2. Réstalo al Saldo del cliente.
        // 3. Imprime un recibo, ej:
        //    "Laura rentó Toyota Corolla por 3 días. Saldo restante: $60"
        double total = auto.PrecioPorDia * dias;
        if (cliente._saldo <= total)
        {
            Console.WriteLine("Saldo Insuficiente");
            return;
        }
        else
        {
            cliente._saldo -= total;
            Console.WriteLine($"{cliente.Nombre} rentó {auto.Nombre} por {dias} días. Saldo restante: {cliente._saldo}");
        }
    }
}
