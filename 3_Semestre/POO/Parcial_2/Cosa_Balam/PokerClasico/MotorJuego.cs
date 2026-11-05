
namespace PokerClasico;

/// <summary>
/// Orquestador genérico de una mesa de cartas. No conoce ninguna regla concreta:
/// toda la lógica del juego se delega al contrato <see cref="IReglasJuego"/>.
/// </summary>
public class MotorJuego
{
    private readonly IReglasJuego _reglas;
    private readonly List<Jugador> _jugadores = new();
    private Mazo _mazo = new();

    public MotorJuego(IReglasJuego reglas)
    {
        _reglas = reglas ?? throw new ArgumentNullException(nameof(reglas));
    }

    public void AgregarJugador(string nombre)
    {
        AgregarJugador(new Jugador(nombre, _jugadores.Count + 1));
    }

    public void AgregarJugador(Jugador jugador)
    {
        ArgumentNullException.ThrowIfNull(jugador);
        _jugadores.Add(jugador);
    }

    public void EjecutarRonda()
    {
        if (_jugadores.Count == 0)
        {
            Console.WriteLine("No hay jugadores en la mesa.");
            return;
        }

        MostrarEncabezado();

        // 1. Baraja el mazo (uno completo y nuevo en cada ronda).
        _mazo = new Mazo();
        _mazo.Barajar();

        // 2. Reparte según las reglas.
        _reglas.Repartir(_mazo, _jugadores);

        // 3. Evalúa la puntuación de cada jugador.
        foreach (Jugador jugador in _jugadores)
        {
            int puntuacion = _reglas.EvaluarPuntuacion(jugador.Mano, out string descripcion);
            jugador.AsignarResultado(puntuacion, descripcion);
        }

        // 4. Muestra las cartas y resultados.
        foreach (Jugador jugador in _jugadores)
        {
            MostrarJugador(jugador);
        }

        // 5. Determina e imprime el veredicto final.
        string veredicto = _reglas.DeterminarGanador(_jugadores);
        Console.WriteLine(new string('═', 60));
        Console.ForegroundColor = ConsoleColor.Yellow;
        Console.WriteLine($"  VEREDICTO: {veredicto}");
        Console.ResetColor();
        Console.WriteLine(new string('═', 60));
    }

    private void MostrarEncabezado()
    {
        Console.WriteLine(new string('═', 60));
        Console.ForegroundColor = ConsoleColor.Cyan;
        Console.WriteLine($"  {_reglas.NombreJuego}");
        Console.ResetColor();
        Console.WriteLine($"  {_reglas.Descripcion}");
        Console.WriteLine(new string('═', 60));
        Console.WriteLine();
    }

    private static void MostrarJugador(Jugador jugador)
    {
        Console.ForegroundColor = ConsoleColor.Green;
        Console.WriteLine($"► {jugador}");
        Console.ResetColor();
        Console.WriteLine($"  Mano: {string.Join("  ", jugador.Mano)}");
        Carta.Dibujar(jugador.Mano);
        Console.WriteLine($"  Jugada: {jugador.DetalleJugada}");
        Console.WriteLine($"  Puntuación: {jugador.Puntuacion:N0}");
        Console.WriteLine();
    }
}
