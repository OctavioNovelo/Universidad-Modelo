using PokerClasico.Enums;

namespace PokerClasico.Modelos;

/// <summary>
/// Baraja estándar de 52 cartas.
/// </summary>
public class Mazo
{
    private readonly List<Carta> _cartas = new();
    private readonly Random _random;

    public Mazo() : this(Random.Shared)
    {
    }

    /// <summary>Permite inyectar un generador aleatorio (útil para pruebas reproducibles).</summary>
    public Mazo(Random random)
    {
        _random = random ?? throw new ArgumentNullException(nameof(random));

        foreach (Palo palo in Enum.GetValues<Palo>())
        {
            foreach (ValorCarta valor in Enum.GetValues<ValorCarta>())
            {
                _cartas.Add(new Carta(palo, valor));
            }
        }
    }

    public int CartasRestantes => _cartas.Count;

    /// <summary>Barajado aleatorio con el algoritmo de Fisher-Yates.</summary>
    public void Barajar()
    {
        for (int i = _cartas.Count - 1; i > 0; i--)
        {
            int j = _random.Next(i + 1);
            (_cartas[i], _cartas[j]) = (_cartas[j], _cartas[i]);
        }
    }

    /// <summary>Extrae y devuelve la carta superior del mazo.</summary>
    public Carta TomarCarta()
    {
        if (_cartas.Count == 0)
        {
            throw new InvalidOperationException("El mazo está vacío.");
        }

        int indiceSuperior = _cartas.Count - 1;
        Carta carta = _cartas[indiceSuperior];
        _cartas.RemoveAt(indiceSuperior);
        return carta;
    }

    /// <summary>Devuelve una lista con la cantidad de cartas solicitadas.</summary>
    public List<Carta> Repartir(int cantidad)
    {
        if (cantidad < 0 || cantidad > _cartas.Count)
        {
            throw new ArgumentOutOfRangeException(nameof(cantidad), cantidad,
                $"Solo quedan {_cartas.Count} cartas en el mazo.");
        }

        var cartas = new List<Carta>(cantidad);
        for (int i = 0; i < cantidad; i++)
        {
            cartas.Add(TomarCarta());
        }
        return cartas;
    }

    /// <summary>Devuelve una sola carta.</summary>
    public Carta Repartir() => TomarCarta();
}
