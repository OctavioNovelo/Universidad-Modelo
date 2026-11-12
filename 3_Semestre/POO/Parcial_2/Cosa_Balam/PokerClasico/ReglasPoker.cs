namespace PokerClasico;

// Reglas del Póker Clásico (Showdown de 5 cartas).
public class ReglasPoker : ReglasJuegoBase
{
    private const int CartasPorMano = 5;

    // Base numérica de la puntuación ponderada. Los valores de carta van de 2 a 14,
    // por lo que una base de 15 permite codificar cada desempate como un "dígito".
    private const int Base = 15;

    // Categorías de jugada, de menor a mayor puntaje.
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

    // Constructor, llama directamente a base. (Nombre / Descripcion)
    public ReglasPoker() : base("Póker Clásico", "Showdown de 5 cartas: cada jugador recibe 5 cartas y gana la mejor jugada de la mesa.")
    {
    }

    // Se sobreescribe el metodo Repartir.
    // Este repartir es repartir para inciar la partida.
    public override void Repartir(Mazo mazo, List<Jugador> jugadores)
    {
        // Verificaciones.
        if (mazo == null)
        {
            throw new ArgumentNullException(nameof(mazo));
        }
        if (jugadores == null)
        {
            throw new ArgumentNullException(nameof(jugadores));
        }
        // Verificamos si las cartas del mazo son suficientes para repartir a los jugadores actuales
        if (mazo.CartasRestantes < jugadores.Count * CartasPorMano)
        {
            throw new InvalidOperationException($"No hay cartas suficientes para {jugadores.Count} jugadores.");
        }
        // Limpiamos todas las manos
        foreach (Jugador jugador in jugadores)
        {
            jugador.LimpiarMano();
        }
        // Reparto tradicional: una carta a la vez, en rondas, a cada jugador. En este caso 5 veces, 5 cartas.
        for (int ronda = 0; ronda < CartasPorMano; ronda++)
        {
            foreach (Jugador jugador in jugadores)
            {
                jugador.RecibirCarta(mazo.Repartir());
            }
        }
    }

    // Se sobreescribe EvaluarPuntuacion.
    public override int EvaluarPuntuacion(List<Carta> mano, out string descripcionJugada)
    {
        // Verificaciones
        if (mano == null)
        {
            throw new ArgumentNullException(nameof(mano));
        }
        if (mano.Count != CartasPorMano)
        {
            throw new ArgumentException($"La mano debe tener exactamente {CartasPorMano} cartas.", nameof(mano));
        }
        // Lista nueva llamada grupos, es una lista de tuplas.
        List<(ValorCarta Valor, int Cantidad)> grupos = new();
        // Por cada carta en la mano
        foreach (Carta carta in mano)
        {
            bool encontrado = false;
            // Pasamos cada grupo
            for (int i = 0; i < grupos.Count; i++)
            {
                // Si el valor actual es igual al valor de la carta actual
                if (grupos[i].Valor == carta.Valor)
                {
                    // Se le suma uno a la cantidad de cartas con ese valor.
                    grupos[i] = (grupos[i].Valor, grupos[i].Cantidad + 1);
                    encontrado = true; // Marcamos como encontrado
                    break;
                }
            }
            // Si no lo encontramos
            if (!encontrado)
            {
                // Agregamos el valor de la carta y su cantidad (1 porque seria la primera)
                grupos.Add((carta.Valor, 1));
            }
        }
        // Pasamos cada grupo (por indice) que aqui lo ordenamos
        for (int i = 0; i < grupos.Count - 1; i++)
        {
            // j = siguiente grupo
            for (int j = i + 1; j < grupos.Count; j++)
            {
                // Si la cantidad de j es mayor de i, o, si j == i && valor del grupo j es mayor a valor de i
                if (grupos[j].Cantidad > grupos[i].Cantidad || (grupos[j].Cantidad == grupos[i].Cantidad && grupos[j].Valor > grupos[i].Valor))
                {
                    var a = grupos[i]; // Guardamos grupo i
                    grupos[i] = grupos[j]; // grupo en posicion i ahora es grupo j
                    grupos[j] = a; // grupo jota ahora es el anterior grupo en posicion i
                }
            }
        }
        List<ValorCarta> valoresDesc = new(); // Nueva lista ValorCarta
        // Por cada carta en mano
        foreach (Carta carta in mano)
        {
            valoresDesc.Add(carta.Valor); // Agregamos el valor a la lista
        }
        // Por cada valor encontrado.
        for (int i = 0; i < valoresDesc.Count - 1; i++)
        {
            // j = siguiente valor.
            for (int j = i + 1; j < valoresDesc.Count; j++)
            {
                // Si el siguiente valor es mayor al valor actual
                if (valoresDesc[j] > valoresDesc[i])
                {
                    ValorCarta a = valoresDesc[i]; // Guardamos valor actual.
                    valoresDesc[i] = valoresDesc[j]; // Sobreescribimos el valor actual por el valor sigueinte.
                    valoresDesc[j] = a; // El valor siguiente se conveirte en el valor anteriormente actual.
                }
            }
        }
        // CHECAMOS SI LA MANO ES UN COLOR.
        bool esColor = true;
        // Por cada carta en mano
        foreach (Carta carta in mano)
        {
            // Si el palo es diferente al palo de la primera carta de la mano.
            if (carta.Palo != mano[0].Palo)
            {
                esColor = false;
                break;
            }
        }
        // CHECAMOS SI LA MANO ES UNA ESCALERA
        bool esEscalera = EsEscalera(valoresDesc, out ValorCarta cartaAltaEscalera);
        // Guardamos la categoría de la mano y los valores necesarios para desempatar.
        Categoria categoria;
        List<ValorCarta> desempates;
        // Escalera real o escalera de color: mismo palo y valores consecutivos.
        if (esEscalera && esColor)
        {
            categoria = cartaAltaEscalera == ValorCarta.As ? Categoria.EscaleraReal : Categoria.EscaleraDeColor;
            desempates = [cartaAltaEscalera];
            descripcionJugada = categoria == Categoria.EscaleraReal
                ? $"Escalera Real de {NombrePalo(mano[0].Palo)}"
                : $"Escalera de Color de {NombrePalo(mano[0].Palo)} al {NombreSingular(cartaAltaEscalera)}";
        }
        // Póker: cuatro cartas con el mismo valor.
        else if (grupos[0].Cantidad == 4)
        {
            categoria = Categoria.Poker;
            desempates = [grupos[0].Valor, grupos[1].Valor];
            descripcionJugada = $"Póker de {NombrePlural(grupos[0].Valor)}";
        }
        // Full House: tres cartas de un valor y dos de otro.
        else if (grupos[0].Cantidad == 3 && grupos[1].Cantidad == 2)
        {
            categoria = Categoria.FullHouse;
            desempates = [grupos[0].Valor, grupos[1].Valor];
            descripcionJugada = $"Full House de {NombrePlural(grupos[0].Valor)} y {NombrePlural(grupos[1].Valor)}";
        }
        // Color: las cinco cartas tienen el mismo palo.
        else if (esColor)
        {
            categoria = Categoria.Color;
            desempates = valoresDesc;
            descripcionJugada = $"Color de {NombrePalo(mano[0].Palo)} con {NombreSingular(valoresDesc[0])} alto";
        }
        // Escalera: cinco valores consecutivos, pero no todos del mismo palo.
        else if (esEscalera)
        {
            categoria = Categoria.Escalera;
            desempates = [cartaAltaEscalera];
            descripcionJugada = $"Escalera al {NombreSingular(cartaAltaEscalera)}";
        }
        // Trío: tres cartas con el mismo valor.
        else if (grupos[0].Cantidad == 3)
        {
            categoria = Categoria.Trio;
            desempates = new List<ValorCarta>();
            foreach (var grupo in grupos)
            {
                desempates.Add(grupo.Valor);
            }
            descripcionJugada = $"Trío de {NombrePlural(grupos[0].Valor)}";
        }
        // Doble pareja: dos grupos de dos cartas.
        else if (grupos[0].Cantidad == 2 && grupos[1].Cantidad == 2)
        {
            categoria = Categoria.DoblePareja;
            desempates = new List<ValorCarta>();
            foreach (var grupo in grupos)
            {
                desempates.Add(grupo.Valor);
            }
            descripcionJugada = $"Doble Pareja de {NombrePlural(grupos[0].Valor)} y {NombrePlural(grupos[1].Valor)}";
        }
        // Pareja: dos cartas del mismo valor.
        else if (grupos[0].Cantidad == 2)
        {
            categoria = Categoria.Pareja;
            desempates = new List<ValorCarta>();
            foreach (var grupo in grupos)
            {
                desempates.Add(grupo.Valor);
            }
            descripcionJugada = $"Pareja de {NombrePlural(grupos[0].Valor)}";
        }
        else
        {
            // Si no se cumple ninguna jugada anterior, se considera carta alta.
            categoria = Categoria.CartaAlta;
            desempates = valoresDesc;
            descripcionJugada = $"Carta Alta: {NombreSingular(valoresDesc[0])}";
        }
        // Convertimos la jugada y los desempates en una puntuación numérica.
        return CalcularPuntuacion(categoria, desempates);
    }

    // Busca la puntuación más alta y determina si hay un ganador o un empate.
    public override string DeterminarGanador(List<Jugador> jugadores)
    {
        // Verificamos que la lista de jugadores no sea null.
        ArgumentNullException.ThrowIfNull(jugadores);
        // Si no hay jugadores, no podemos determinar un ganador.
        if (jugadores.Count == 0)
        {
            return "No hay jugadores en la mesa.";
        }
        // Obtenemos la puntuación más alta entre todos los jugadores.
        int mejorPuntuacion = jugadores.Max(j => j.Puntuacion);
        // Guardamos a todos los jugadores que tengan esa misma puntuación.
        List<Jugador> ganadores = jugadores.Where(j => j.Puntuacion == mejorPuntuacion).ToList();
        // Si solamente hay uno, devolvemos su nombre y la jugada ganadora.
        if (ganadores.Count == 1)
        {
            Jugador ganador = ganadores[0];
            return $"Gana {ganador.Nombre} con {ganador.DetalleJugada}.";
        }
        // Si hay empate, unimos los nombres de los ganadores con " y ".
        string nombres = string.Join(" y ", ganadores.Select(j => j.Nombre));
        return $"Empate entre {nombres} con {ganadores[0].DetalleJugada}. El bote se divide.";
    }

    private static int CalcularPuntuacion(Categoria categoria, List<ValorCarta> desempates)
    {
        // Comenzamos con el valor numérico de la categoría de jugada.
        int puntuacion = (int)categoria;
        // Añadimos hasta cinco valores para poder desempatar jugadas de la misma categoría.
        for (int i = 0; i < CartasPorMano; i++)
        {
            // Si ya no quedan valores de desempate, utilizamos 0.
            int valor = i < desempates.Count ? (int)desempates[i] : 0;
            // Desplazamos la puntuación una posición en base 15 y agregamos el valor.
            puntuacion = puntuacion * Base + valor;
        }
        return puntuacion;
    }

    // Determina si los valores (ordenados de mayor a menor) forman una escalera.
    // Recibe: La lista de valores ordenados y devuelve mediante out la carta más alta de la escalera.
    private static bool EsEscalera(List<ValorCarta> valoresDesc, out ValorCarta cartaAlta)
    {
        // Carta Alta == al valor más alto.
        cartaAlta = valoresDesc[0];
        // Si hay valores repetidos, no puede ser una escalera.
        if (valoresDesc.Distinct().Count() != CartasPorMano)
        {
            return false;
        }
        // Si la diferencia entre la carta mayor y la menor es 4, forman una escalera.
        if (valoresDesc[0] - valoresDesc[^1] == CartasPorMano - 1)
        {
            return true;
        }
        // Comprobamos si es una escalera baja.
        bool esEscaleraBaja = valoresDesc.SequenceEqual([ValorCarta.As, ValorCarta.Cinco, ValorCarta.Cuatro, ValorCarta.Tres, ValorCarta.Dos]);
        // Si es una escalera baja, la carta más alta es el 5 y no el As.
        if (esEscaleraBaja)
        {
            cartaAlta = ValorCarta.Cinco;
        }
        // Devuelve true si es escalera baja; de lo contrario, false.
        return esEscaleraBaja;
    }

    // Convierte el palo de una carta en texto para mostrarlo en la descripción.
    private static string NombrePalo(Palo palo) => palo switch
    {
        Palo.Corazones => "Corazones",
        Palo.Diamantes => "Diamantes",
        Palo.Treboles => "Tréboles",
        Palo.Picas => "Picas",
        _ => palo.ToString()
    };

    // Convierte el valor de una carta a su nombre en singular (por ejemplo, "Rey").
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

    // Convierte el valor a plural para describir parejas, tríos y póker (por ejemplo, "Reyes").
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
