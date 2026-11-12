namespace PokerClasico;

// Representa una carta de la baraja.
public class Carta
{
    private const int AnchoCarta = 9; // Ancho interior del naipe ASCII.

    // El palo y el valor se pueden consultar desde fuera, pero solo modificar dentro de Carta.
    public Palo Palo { get; private set; }
    public ValorCarta Valor { get; private set; }

    // Constructor principal: recibe el palo y el valor de la carta.
    public Carta(Palo palo, ValorCarta valor)
    {
        // Comprobamos que el valor exista dentro del enum ValorCarta.
        if (!Enum.IsDefined(valor))
        {
            throw new ArgumentOutOfRangeException(nameof(valor), valor, "Valor de carta inválido.");
        }
        Palo = palo;
        Valor = valor;
    }

    // Constructor secundario: recibe el valor como número y llama al constructor principal.
    public Carta(Palo palo, int valorNumerico): this(palo, ConvertirValor(valorNumerico))
    {
    }

    // Devuelve el símbolo Unicode correspondiente al palo de la carta.
    public string Simbolo => Palo switch
    {
        Palo.Corazones => "♥",
        Palo.Diamantes => "♦",
        Palo.Treboles => "♣",
        Palo.Picas => "♠",
        _ => "?" // Si no coincide con ningún palo conocido.
    };

    // Devuelve el valor en formato corto: 2..10, J, Q, K o A.
    public string ValorCorto => Valor switch
    {
        ValorCarta.Jota => "J",
        ValorCarta.Reina => "Q",
        ValorCarta.Rey => "K",
        ValorCarta.As => "A",
        _ => ((int)Valor).ToString() // Para cartas numéricas, convierte su valor en texto.
    };

    // Determina el color del texto de la carta: rojo para corazones y diamantes, blanco para los demás.
    public ConsoleColor Color => Palo is Palo.Corazones or Palo.Diamantes ? ConsoleColor.Red : ConsoleColor.White;

    // Devuelve una representación corta de la carta, por ejemplo: "A ♥".
    public override string ToString() => $"{ValorCorto} {Simbolo}";

    // Genera las líneas del dibujo ASCII de la carta usando caracteres Unicode.
    public string[] RenderizarAscii()
    {
        // Creamos las líneas horizontales y los espacios del ancho indicado.
        string borde = new('─', AnchoCarta);
        string vacio = new(' ', AnchoCarta);

        // Cada elemento del arreglo corresponde a una línea del dibujo de la carta.
        return
        [
            $"┌{borde}┐",
            $"│{ValorCorto.PadRight(AnchoCarta)}│", // Valor alineado a la izquierda.
            $"│{vacio}│",
            $"│{Centrar(Simbolo, AnchoCarta)}│", // Palo centrado.
            $"│{vacio}│",
            $"│{ValorCorto.PadLeft(AnchoCarta)}│", // Valor alineado a la derecha.
            $"└{borde}┘"
        ];
    }

    // Dibuja esta carta llamando al método que dibuja una lista de cartas.
    public void Dibujar() => Dibujar([this]);

    // Dibuja varias cartas una al lado de otra, respetando el color de cada una.
    public static void Dibujar(IReadOnlyList<Carta> cartas, string sangria = "  ")
    {
        // Si la lista es null, lanzamos una excepción.
        ArgumentNullException.ThrowIfNull(cartas);
        if (cartas.Count == 0)
        {
            return; // No hay cartas que dibujar.
        }

        // Convertimos cada carta en sus líneas de dibujo y guardamos todos esos arreglos.
        string[][] dibujos = cartas.Select(c => c.RenderizarAscii()).ToArray();
        int lineas = dibujos[0].Length; // Número de líneas que tiene cada dibujo.
        ConsoleColor colorOriginal = Console.ForegroundColor; // Guardamos el color actual de la consola.

        // Recorremos las líneas del dibujo, de arriba hacia abajo.
        for (int linea = 0; linea < lineas; linea++)
        {
            Console.Write(sangria);

            // En cada línea, imprimimos la parte correspondiente de todas las cartas.
            for (int i = 0; i < cartas.Count; i++)
            {
                Console.ForegroundColor = cartas[i].Color; // Usamos el color de esta carta.
                Console.Write(dibujos[i][linea]); // Imprimimos la línea actual de esta carta.
                Console.ForegroundColor = colorOriginal;
                Console.Write(' '); // Separamos una carta de la siguiente.
            }
            Console.WriteLine(); // Pasamos a la siguiente línea de los dibujos.
        }

        Console.ForegroundColor = colorOriginal; // Restauramos el color original.
    }

    // Convierte un número entre 2 y 14 al valor correspondiente del enum ValorCarta.
    private static ValorCarta ConvertirValor(int valorNumerico)
    {
        // Comprobamos que el número esté dentro de los valores permitidos.
        if (valorNumerico < (int)ValorCarta.Dos || valorNumerico > (int)ValorCarta.As)
        {
            throw new ArgumentOutOfRangeException(nameof(valorNumerico), valorNumerico, "El valor numérico debe estar entre 2 y 14.");
        }

        return (ValorCarta)valorNumerico; // Convertimos el entero al tipo ValorCarta.
    }

    // Centra un texto en un espacio de ancho fijo, agregando espacios a ambos lados.
    private static string Centrar(string texto, int ancho)
    {
        int izquierda = (ancho - texto.Length) / 2; // Calculamos cuántos espacios van antes del texto.
        return texto.PadLeft(izquierda + texto.Length).PadRight(ancho); // Añadimos espacios a la izquierda y luego a la derecha.
    }
}
