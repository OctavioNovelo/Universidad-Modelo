namespace PokerClasico;

/// <summary>
/// Participante de la mesa.
/// </summary>
public class Jugador
{
    public int Id { get; private set; }
    public string Nombre { get; private set; }
    public List<Carta> Mano { get; private set; }
    public int Puntuacion { get; private set; }
    public string DetalleJugada { get; private set; }

    public Jugador(string nombre) : this(nombre, 0)
    {
    }

    public Jugador(string nombre, int id)
    {
        if (string.IsNullOrWhiteSpace(nombre))
        {
            throw new ArgumentException("El nombre del jugador no puede estar vacío.", nameof(nombre));
        }

        Id = id;
        Nombre = nombre;
        Mano = new List<Carta>();
        Puntuacion = 0;
        DetalleJugada = string.Empty;
    }

    public void RecibirCarta(Carta carta)
    {
        ArgumentNullException.ThrowIfNull(carta);
        Mano.Add(carta);
    }

    public void RecibirCarta(List<Carta> cartas)
    {
        ArgumentNullException.ThrowIfNull(cartas);
        foreach (Carta carta in cartas)
        {
            RecibirCarta(carta);
        }
    }

    /// <summary>Guarda el resultado de la evaluación de la mano.</summary>
    public void AsignarResultado(int puntuacion, string detalleJugada)
    {
        Puntuacion = puntuacion;
        DetalleJugada = detalleJugada ?? string.Empty;
    }

    /// <summary>Vacía la mano y reinicia el resultado para una nueva ronda.</summary>
    public void LimpiarMano()
    {
        Mano.Clear();
        Puntuacion = 0;
        DetalleJugada = string.Empty;
    }

    public override string ToString() => Id > 0 ? $"{Nombre} (#{Id})" : Nombre;
}
