namespace PokerClasico;

// Controla la partida: administra jugadores, mazo y reglas del juego.
public class MotorJuego
{
    private readonly IReglasJuego _reglas; // Reglas que se utilizarán para repartir y evaluar las jugadas.
    private readonly List<Jugador> _jugadores = new(); // Lista de jugadores de la mesa.
    private Mazo _mazo = new(); // Mazo que se utiliza durante la ronda.

    // Constructor: recibe las reglas del juego y las guarda para utilizarlas durante la partida.
    public MotorJuego(IReglasJuego reglas)
    {
        // Si reglas es null, lanzamos una excepción; de lo contrario, la guardamos.
        _reglas = reglas ?? throw new ArgumentNullException(nameof(reglas));
    }

    // Agrega un jugador a partir de su nombre y le asigna el siguiente número disponible.
    public void AgregarJugador(string nombre)
    {
        // Llamamos al otro método AgregarJugador, creando antes el objeto Jugador.
        AgregarJugador(new Jugador(nombre, _jugadores.Count + 1));
    }

    // Agrega a la lista un objeto Jugador que ya existe.
    public void AgregarJugador(Jugador jugador)
    {
        ArgumentNullException.ThrowIfNull(jugador); // Comprobamos que el jugador no sea null.
        _jugadores.Add(jugador);
    }

    // Ejecuta una ronda completa: barajar, repartir, evaluar y mostrar al ganador.
    public void EjecutarRonda()
    {
        // Si no hay jugadores, mostramos un mensaje y terminamos el método.
        if (_jugadores.Count == 0)
        {
            Console.WriteLine("No hay jugadores en la mesa.");
            return;
        }

        MostrarEncabezado();

        // 1. Creamos un mazo nuevo y lo barajamos para esta ronda.
        _mazo = new Mazo();
        _mazo.Barajar();

        // 2. Repartimos las cartas según las reglas del juego.
        _reglas.Repartir(_mazo, _jugadores);

        // 3. Evaluamos la mano de cada jugador y guardamos su puntuación y descripción.
        foreach (Jugador jugador in _jugadores)
        {
            // El return del método da la puntuación y out guarda la descripción de la jugada.
            int puntuacion = _reglas.EvaluarPuntuacion(jugador.Mano, out string descripcion);
            jugador.AsignarResultado(puntuacion, descripcion);
        }

        // 4. Mostramos las cartas y el resultado de cada jugador.
        foreach (Jugador jugador in _jugadores)
        {
            MostrarJugador(jugador);
        }

        // 5. Obtenemos el ganador o empate y mostramos el veredicto final.
        string veredicto = _reglas.DeterminarGanador(_jugadores);
        Console.WriteLine(new string('═', 60)); // Línea separadora de 60 caracteres.
        Console.ForegroundColor = ConsoleColor.Yellow;
        Console.WriteLine($"  VEREDICTO: {veredicto}");
        Console.ResetColor(); // Restauramos el color predeterminado de la consola.
        Console.WriteLine(new string('═', 60));
    }

    // Muestra el título y la descripción del juego, tomados de las reglas.
    private void MostrarEncabezado()
    {
        Console.WriteLine(new string('═', 60));
        Console.ForegroundColor = ConsoleColor.Cyan; // Cambiamos el color para mostrar el título.
        Console.WriteLine($"  {_reglas.NombreJuego}");
        Console.ResetColor();
        Console.WriteLine($"  {_reglas.Descripcion}");
        Console.WriteLine(new string('═', 60));
        Console.WriteLine();
    }

    // Muestra la información de un jugador: nombre, cartas, jugada y puntuación.
    private static void MostrarJugador(Jugador jugador)
    {
        Console.ForegroundColor = ConsoleColor.Green;
        Console.WriteLine($"► {jugador}"); // Muestra al jugador usando su representación en texto.
        Console.ResetColor();
        Console.WriteLine($"  Mano: {string.Join("  ", jugador.Mano)}"); // Une las cartas en una sola línea, separadas por espacios.
        Carta.Dibujar(jugador.Mano); // Dibuja las cartas una al lado de otra.
        Console.WriteLine($"  Jugada: {jugador.DetalleJugada}");
        Console.WriteLine($"  Puntuación: {jugador.Puntuacion:N0}"); // N0 muestra el número con separadores de miles y sin decimales.
        Console.WriteLine();
    }
}
