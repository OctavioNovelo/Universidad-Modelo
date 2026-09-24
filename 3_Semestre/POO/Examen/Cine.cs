using System.Runtime.InteropServices.Marshalling;

public class Cine
{
    public string NombreCine;
    public List<Sala> SalasHabilitadas; 
    public Cine(string nombre)
    {
        NombreCine = nombre;
        SalasHabilitadas = new List<Sala>();
    }

   

  
    public void VenderBoleto(Espectador cliente, Sala salaCine)
    {
        if (cliente.Edad >= salaCine.PeliculaProyectada.EdadMinima)
        {
            if (salaCine.AsientosDisponibles > 0)
            {
                salaCine.AsientosOcupados += 1;
                Console.WriteLine($"\nProcesando venta para {cliente.Nombre} - Película: {salaCine.PeliculaProyectada.Titulo}...");
            }
            else
            {
                Console.WriteLine($"Sin asientos disponibles para {cliente.Nombre}");
            }
        }
        else
        {
            Console.WriteLine($"{cliente.Nombre} no tiene la edad minima permitida");
        }      
    }

    public void AgregarSala(Sala a)
    {
        SalasHabilitadas.Add(a);
    }
}