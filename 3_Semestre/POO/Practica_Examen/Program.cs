class Program
{
    static void Main()
    {

        LocalGaming nexuz = new LocalGaming("Nexuz Center Centro");


        Equipo pc1 = new Equipo("PC Master Race RTX 4090", 50.0);
        Equipo consola1 = new Equipo("PS5 Sala Privada", 80.0);

        nexuz.AgregarEquipo(pc1);
        nexuz.AgregarEquipo(consola1);


        Gamer jugador1 = new Gamer("Faker");
        jugador1.Saldo = 200;

        Gamer jugador2 = new Gamer("Ibai", 500);

        Console.WriteLine("--- Sistema de Rentas NEXUZ ---");
        nexuz.RentarEquipo(jugador1, pc1, 3);
        nexuz.RentarEquipo(jugador2, consola1, 2);


        Console.WriteLine("\n--- Prueba De Seguridad ---");
        nexuz.RentarEquipo(jugador1, pc1, 10);
    }
}