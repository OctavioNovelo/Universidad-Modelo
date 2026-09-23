using System.IO.Compression;

public class LocalGaming
{
    public string NombreLocal;

    List<Equipo> Inventario = new List<Equipo>();

    public LocalGaming(string nombre)
    {
        NombreLocal = nombre;
        List<Equipo> Inventario = new List<Equipo>();
    }


    public void RentarEquipo(Gamer cliente, Equipo pc, int horas)
    {
        double total = pc.PrecioPorHora * horas;
        if (total >= cliente.Saldo)
        {
            Console.WriteLine("Saldo Insuficiente");
            return;
        }
        cliente.Saldo -= total;
        Console.WriteLine($"{cliente.Nickname} rentó {pc.Nombre} por {horas} horas. Saldo restante: {cliente.Saldo}");
    }

    public void AgregarEquipo(Equipo name)
    {
        Inventario.Add(name);
    }
}