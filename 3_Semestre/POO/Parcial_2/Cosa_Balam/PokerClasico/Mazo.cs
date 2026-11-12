
namespace PokerClasico;

// Mazo de 52 cartas
public class Mazo
{
    private readonly List<Carta> _cartas = new();
    private readonly Random _random; // Seed


    // CONSTRUCTORES
    // Crear mazo
    public Mazo() : this(Random.Shared)
    {
    }

    // Crear un mazo con una seed.
    public Mazo(Random random)
    {
        // _random = es tipo random? ?? NO puede ser null
        _random = random ?? throw new ArgumentNullException(nameof(random));

        // Por cada palo (4 en total) que haya en el enum Palo
        foreach (Palo palo in Enum.GetValues<Palo>())
        {
            // Y Por cada valor (2-14) que haya en el enum Valor
            foreach (ValorCarta valor in Enum.GetValues<ValorCarta>())
            {
                _cartas.Add(new Carta(palo, valor)); // Agregamos a la lista una carta con su respectivo palo y valor.
            }
        }
    }


    // METODOS
    // Cantidad de cartas restantes. 
    public int CartasRestantes => _cartas.Count;

    // Metodos
    // Fisher Yates / Barajado de Knuth
    public void Barajar()
    {
        // Recorrermos todas las cartas del mazo (0-n)
        for (int i = _cartas.Count - 1; i > 0; i--)
        {
            int j = _random.Next(i + 1); // Se calcula un indice random del 0 al indice actual 
            (_cartas[i], _cartas[j]) = (_cartas[j], _cartas[i]); // Intercambiamos
            // carta actual, carta en el indice calculado === se cambian === carta del indice calcula (ahora en la posicion actual), carta anterior
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

        int carta_superior = _cartas.Count - 1;
        Carta carta = _cartas[carta_superior]; // Se crea una carta con la referencia a la carta ultima (primera para agarrar) carta del mazo.
        _cartas.RemoveAt(carta_superior); // Borramos la referencia a la carta que se econtraba en el mazo
        return carta; // Regresamos la carta.
    }

    // Devuelve una lista con la cantidad de cartas solicitadas
    public List<Carta> Repartir(int cantidad)
    {
        // Que NO se 0 o que no sea mayor a la cantidad de cartas que quedan.
        if (cantidad < 0 || cantidad > _cartas.Count)
        {
            throw new ArgumentOutOfRangeException(nameof(cantidad), cantidad, $"Solo quedan {_cartas.Count} cartas en el mazo.");
        }

        var cartas = new List<Carta>(cantidad); // Creamos una lista temporal
        for (int i = 0; i < cantidad; i++)
        {
            // Agregamos con add a la lista nueva (cartas) usando el metodo TomarCarta(); que agarra la primera carta de mazo.
            // Lo hace "catidad" veces
            cartas.Add(TomarCarta());
        }
        return cartas;
    }

    // Devuelve SOLO 1 cartas
    public Carta Repartir() => TomarCarta();
}
