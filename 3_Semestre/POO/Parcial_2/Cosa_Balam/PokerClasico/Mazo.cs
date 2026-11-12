
namespace PokerClasico;

// Mazo de 52 cartas
public class Mazo
{
    private readonly List<Carta> _cartas = new(); // Lista de cartas == Mano
    private readonly Random _random; // Seed

    // Crear mazoS
    public Mazo() : this(Random.Shared)
    {
    }

    // Crear un mazo con una seed.
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

    // Metodos
    // Checar algoritmo
    public void Barajar()
    {
        for (int i = _cartas.Count - 1; i > 0; i--)
        {
            int j = _random.Next(i + 1);
            (_cartas[i], _cartas[j]) = (_cartas[j], _cartas[i]);
        }
    }

    // Toma la primera carta del mazo
    public Carta TomarCarta()
    {
        // Si el MAZO esta vacio
        if (_cartas.Count == 0)
        {
            throw new InvalidOperationException("El mazo está vacío.");
        }

        int indiceSuperior = _cartas.Count - 1;
        Carta carta = _cartas[indiceSuperior];
        _cartas.RemoveAt(indiceSuperior);
        return carta;
    }

    // Devuelve una lista con la cantidad de cartas solicitadas
    public List<Carta> Repartir(int cantidad)
    {
        // Que NO se 0 o que no sea mayor a la cantidad de cartas que quedan.
        if (cantidad < 0 || cantidad > _cartas.Count)
        {
            throw new ArgumentOutOfRangeException(nameof(cantidad), cantidad, $"Solo quedan {_cartas.Count} cartas en el mazo.");
        }

        var cartas = new List<Carta>(cantidad);
        for (int i = 0; i < cantidad; i++)
        {
            cartas.Add(TomarCarta());
        }
        return cartas;
    }

    // Devuelve SOLO 1 cartas
    public Carta Repartir() => TomarCarta();
}
