
namespace PokerClasico;

/// <summary>
/// Reglas del Póker Clásico (Showdown de 5 cartas).
/// </summary>
public class ReglasPoker : ReglasJuegoBase
{
    private const int CartasPorMano = 5;

    /// <summary>
    /// Base numérica de la puntuación ponderada. Los valores de carta van de 2 a 14,
    /// por lo que una base de 15 permite codificar cada desempate como un "dígito".
    /// </summary>
    private const int Base = 15;

    /// <summary>Categorías de jugada, de menor a mayor.</summary>
    private enum Categoria
    {
        CartaAlta = 0,
        Pareja = 1,
        DoblePareja = 2,
        Trio = 3,
        Escalera = 4,
        Color = 5,
        FullHouse = 6,
        Poker = 7,
        EscaleraDeColor = 8,
        EscaleraReal = 9
    }

    public ReglasPoker() : base("Póker Clásico (5 Cartas)", "Showdown de 5 cartas: cada jugador recibe 5 naipes y gana la mejor jugada de la mesa.")
    {
    }

    public override void Repartir(Mazo mazo, List<Jugador> jugadores)
    {
        ArgumentNullException.ThrowIfNull(mazo);
        ArgumentNullException.ThrowIfNull(jugadores);

        if (mazo.CartasRestantes < jugadores.Count * CartasPorMano)
        {
            throw new InvalidOperationException($"No hay cartas suficientes para {jugadores.Count} jugadores.");
        }

        foreach (Jugador jugador in jugadores)
        {
            jugador.LimpiarMano();
        }

        // Reparto tradicional: una carta a la vez, en rondas, a cada jugador.
        for (int ronda = 0; ronda < CartasPorMano; ronda++)
        {
            foreach (Jugador jugador in jugadores)
            {
                jugador.RecibirCarta(mazo.Repartir());
            }
        }
    }

    public override int EvaluarPuntuacion(List<Carta> mano, out string descripcionJugada)
    {
        ArgumentNullException.ThrowIfNull(mano);
        if (mano.Count != CartasPorMano)
        {
            throw new ArgumentException($"La mano debe tener exactamente {CartasPorMano} cartas.", nameof(mano));
        }

        // Grupos por valor: primero los más numerosos, luego los de mayor valor.
        var grupos = mano
            .GroupBy(c => c.Valor)
            .Select(g => (Valor: g.Key, Cantidad: g.Count()))
            .OrderByDescending(g => g.Cantidad)
            .ThenByDescending(g => g.Valor)
            .ToList();

        List<ValorCarta> valoresDesc = mano.Select(c => c.Valor).OrderByDescending(v => v).ToList();
        bool esColor = mano.All(c => c.Palo == mano[0].Palo);
        bool esEscalera = EsEscalera(valoresDesc, out ValorCarta cartaAltaEscalera);

        Categoria categoria;
        List<ValorCarta> desempates;

        if (esEscalera && esColor)
        {
            categoria = cartaAltaEscalera == ValorCarta.As ? Categoria.EscaleraReal : Categoria.EscaleraDeColor;
            desempates = [cartaAltaEscalera];
            descripcionJugada = categoria == Categoria.EscaleraReal
                ? $"Escalera Real de {NombrePalo(mano[0].Palo)}"
                : $"Escalera de Color de {NombrePalo(mano[0].Palo)} al {NombreSingular(cartaAltaEscalera)}";
        }
        else if (grupos[0].Cantidad == 4)
        {
            categoria = Categoria.Poker;
            desempates = [grupos[0].Valor, grupos[1].Valor];
            descripcionJugada = $"Póker de {NombrePlural(grupos[0].Valor)}";
        }
        else if (grupos[0].Cantidad == 3 && grupos[1].Cantidad == 2)
        {
            categoria = Categoria.FullHouse;
            desempates = [grupos[0].Valor, grupos[1].Valor];
            descripcionJugada = $"Full House de {NombrePlural(grupos[0].Valor)} y {NombrePlural(grupos[1].Valor)}";
        }
        else if (esColor)
        {
            categoria = Categoria.Color;
            desempates = valoresDesc;
            descripcionJugada = $"Color de {NombrePalo(mano[0].Palo)} con {NombreSingular(valoresDesc[0])} alto";
        }
        else if (esEscalera)
        {
            categoria = Categoria.Escalera;
            desempates = [cartaAltaEscalera];
            descripcionJugada = $"Escalera al {NombreSingular(cartaAltaEscalera)}";
        }
        else if (grupos[0].Cantidad == 3)
        {
            categoria = Categoria.Trio;
            desempates = grupos.Select(g => g.Valor).ToList();
            descripcionJugada = $"Trío de {NombrePlural(grupos[0].Valor)}";
        }
        else if (grupos[0].Cantidad == 2 && grupos[1].Cantidad == 2)
        {
            categoria = Categoria.DoblePareja;
            desempates = grupos.Select(g => g.Valor).ToList();
            descripcionJugada = $"Doble Pareja de {NombrePlural(grupos[0].Valor)} y {NombrePlural(grupos[1].Valor)}";
        }
        else if (grupos[0].Cantidad == 2)
        {
            categoria = Categoria.Pareja;
            desempates = grupos.Select(g => g.Valor).ToList();
            descripcionJugada = $"Pareja de {NombrePlural(grupos[0].Valor)}";
        }
        else
        {
            categoria = Categoria.CartaAlta;
            desempates = valoresDesc;
            descripcionJugada = $"Carta Alta: {NombreSingular(valoresDesc[0])}";
        }

        return CalcularPuntuacion(categoria, desempates);
    }

    public override string DeterminarGanador(List<Jugador> jugadores)
    {
        ArgumentNullException.ThrowIfNull(jugadores);
        if (jugadores.Count == 0)
        {
            return "No hay jugadores en la mesa.";
        }

        int mejorPuntuacion = jugadores.Max(j => j.Puntuacion);
        List<Jugador> ganadores = jugadores.Where(j => j.Puntuacion == mejorPuntuacion).ToList();

        if (ganadores.Count == 1)
        {
            Jugador ganador = ganadores[0];
            return $"🏆 Gana {ganador.Nombre} con {ganador.DetalleJugada}.";
        }

        string nombres = string.Join(" y ", ganadores.Select(j => j.Nombre));
        return $"🤝 Empate entre {nombres} con {ganadores[0].DetalleJugada}. El bote se divide.";
    }

    /// <summary>
    /// Puntuación ponderada: la categoría es el dígito más significativo y los
    /// desempates (hasta 5) ocupan los siguientes dígitos en base 15.
    /// </summary>
    private static int CalcularPuntuacion(Categoria categoria, List<ValorCarta> desempates)
    {
        int puntuacion = (int)categoria;
        for (int i = 0; i < CartasPorMano; i++)
        {
            int valor = i < desempates.Count ? (int)desempates[i] : 0;
            puntuacion = puntuacion * Base + valor;
        }
        return puntuacion;
    }

    /// <summary>
    /// Determina si los valores (ordenados de mayor a menor) forman una escalera.
    /// Contempla la escalera baja A-2-3-4-5, en la que el As vale 1.
    /// </summary>
    private static bool EsEscalera(List<ValorCarta> valoresDesc, out ValorCarta cartaAlta)
    {
        cartaAlta = valoresDesc[0];

        if (valoresDesc.Distinct().Count() != CartasPorMano)
        {
            return false;
        }

        if (valoresDesc[0] - valoresDesc[^1] == CartasPorMano - 1)
        {
            return true;
        }

        bool esEscaleraBaja = valoresDesc.SequenceEqual(
            [ValorCarta.As, ValorCarta.Cinco, ValorCarta.Cuatro, ValorCarta.Tres, ValorCarta.Dos]);
        if (esEscaleraBaja)
        {
            cartaAlta = ValorCarta.Cinco;
        }
        return esEscaleraBaja;
    }

    private static string NombrePalo(Palo palo) => palo switch
    {
        Palo.Corazones => "Corazones",
        Palo.Diamantes => "Diamantes",
        Palo.Treboles => "Tréboles",
        Palo.Picas => "Picas",
        _ => palo.ToString()
    };

    private static string NombreSingular(ValorCarta valor) => valor switch
    {
        ValorCarta.Dos => "Dos",
        ValorCarta.Tres => "Tres",
        ValorCarta.Cuatro => "Cuatro",
        ValorCarta.Cinco => "Cinco",
        ValorCarta.Seis => "Seis",
        ValorCarta.Siete => "Siete",
        ValorCarta.Ocho => "Ocho",
        ValorCarta.Nueve => "Nueve",
        ValorCarta.Diez => "Diez",
        ValorCarta.Jota => "Jota",
        ValorCarta.Reina => "Reina",
        ValorCarta.Rey => "Rey",
        ValorCarta.As => "As",
        _ => valor.ToString()
    };

    private static string NombrePlural(ValorCarta valor) => valor switch
    {
        ValorCarta.Dos => "Doses",
        ValorCarta.Tres => "Treses",
        ValorCarta.Cuatro => "Cuatros",
        ValorCarta.Cinco => "Cincos",
        ValorCarta.Seis => "Seises",
        ValorCarta.Siete => "Sietes",
        ValorCarta.Ocho => "Ochos",
        ValorCarta.Nueve => "Nueves",
        ValorCarta.Diez => "Dieces",
        ValorCarta.Jota => "Jotas",
        ValorCarta.Reina => "Reinas",
        ValorCarta.Rey => "Reyes",
        ValorCarta.As => "Ases",
        _ => valor.ToString()
    };
}
