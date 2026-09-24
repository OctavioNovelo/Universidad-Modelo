class Program
{
    static void Main()
    {
        
        Cine miCine = new Cine("Cine POO Plaza");

        Pelicula peliTerror = new Pelicula("Masacre en la Consola", 18);
        Sala sala1 = new Sala(1, 2, peliTerror);

        miCine.AgregarSala(sala1);

        Espectador cliente1 = new Espectador("Timmy", 12);
        Espectador cliente2 = new Espectador("Juan"); 
        Espectador cliente3 = new Espectador("María", 25);


        Console.WriteLine("--- ABRIENDO TAQUILLA ---");

        miCine.VenderBoleto(cliente1, sala1); // Timmy
        miCine.VenderBoleto(cliente2, sala1); // Juan
        miCine.VenderBoleto(cliente3, sala1); // 

        Espectador hacker = new Espectador("Hacker", 30);
        miCine.VenderBoleto(hacker, sala1);

        Console.WriteLine("\n--- PRUEBA DE SEGURIDAD ---");
        sala1.AsientosOcupados = 5000; 
        Console.WriteLine($"Ocupados reales: {sala1.AsientosOcupados} / {sala1.CapacidadMaxima}");
        Console.WriteLine($"Disponibles: {sala1.AsientosDisponibles}");
    }
}