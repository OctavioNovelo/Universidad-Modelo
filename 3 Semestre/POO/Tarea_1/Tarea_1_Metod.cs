class Tarea_1_Metod
{
    public static Papu[] papus = new Papu[50];
    public static int cantidadPapus = 0;

    public static Papu Crear()
    {
        Console.Write("Nombra a tu Papu: ");
        string nombreIngresado = Console.ReadLine();

        Papu nuevoPapu = new Papu
        {
            nombre = nombreIngresado
        };

        papus[cantidadPapus] = nuevoPapu;
        cantidadPapus++;

        Console.WriteLine(nuevoPapu.nombre + " ha sido creado.");

        return nuevoPapu;
    }

    public static void Print(Papu jugador)
    {
        Console.WriteLine();
        Console.WriteLine(jugador.nombre);
        Console.WriteLine("Vida: " + jugador.vida);
        Console.WriteLine("Ataque: " + jugador.ataque);
        Console.WriteLine("Nivel: " + jugador.nivel);
    }
}