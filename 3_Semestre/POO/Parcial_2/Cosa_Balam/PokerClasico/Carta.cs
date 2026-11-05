
namespace PokerClasico;

/// <summary>
/// Representa un naipe de la baraja francesa (palo + valor).
/// </summary>
public class Carta
{
    private const int AnchoCarta = 9; // ancho interior del naipe ASCII

    public Palo Palo { get; private set; }
    public ValorCarta Valor { get; private set; }

    /// <summary>Constructor principal.</summary>
    public Carta(Palo palo, ValorCarta valor)
    {
        if (!Enum.IsDefined(valor))
        {
            throw new ArgumentOutOfRangeException(nameof(valor), valor, "Valor de carta inválido.");
        }

        Palo = palo;
        Valor = valor;
    }

    /// <summary>Constructor sobrecargado: recibe el valor como número (2..14).</summary>
    public Carta(Palo palo, int valorNumerico)
        : this(palo, ConvertirValor(valorNumerico))
    {
    }

    /// <summary>Símbolo Unicode del palo.</summary>
    public string Simbolo => Palo switch
    {
        Palo.Corazones => "♥",
        Palo.Diamantes => "♦",
        Palo.Treboles => "♣",
        Palo.Picas => "♠",
        _ => "?"
    };

    /// <summary>Texto corto del valor (2..10, J, Q, K, A).</summary>
    public string ValorCorto => Valor switch
    {
        ValorCarta.Jota => "J",
        ValorCarta.Reina => "Q",
        ValorCarta.Rey => "K",
        ValorCarta.As => "A",
        _ => ((int)Valor).ToString()
    };

    /// <summary>Color de consola asociado al palo (rojo para ♥ ♦, blanco para ♣ ♠).</summary>
    public ConsoleColor Color =>
        Palo is Palo.Corazones or Palo.Diamantes ? ConsoleColor.Red : ConsoleColor.White;

    public override string ToString() => $"{ValorCorto} {Simbolo}";

    /// <summary>
    /// Genera las líneas del dibujo ASCII de la carta usando caracteres Unicode.
    /// </summary>
    public string[] RenderizarAscii()
    {
        string borde = new('─', AnchoCarta);
        string vacio = new(' ', AnchoCarta);

        return
        [
            $"┌{borde}┐",
            $"│{ValorCorto.PadRight(AnchoCarta)}│",
            $"│{vacio}│",
            $"│{Centrar(Simbolo, AnchoCarta)}│",
            $"│{vacio}│",
            $"│{ValorCorto.PadLeft(AnchoCarta)}│",
            $"└{borde}┘"
        ];
    }

    /// <summary>Dibuja esta carta en consola con su color.</summary>
    public void Dibujar() => Dibujar([this]);

    /// <summary>Dibuja un conjunto de cartas una al lado de otra, cada una con su color.</summary>
    public static void Dibujar(IReadOnlyList<Carta> cartas, string sangria = "  ")
    {
        ArgumentNullException.ThrowIfNull(cartas);
        if (cartas.Count == 0)
        {
            return;
        }

        string[][] dibujos = cartas.Select(c => c.RenderizarAscii()).ToArray();
        int lineas = dibujos[0].Length;
        ConsoleColor colorOriginal = Console.ForegroundColor;

        for (int linea = 0; linea < lineas; linea++)
        {
            Console.Write(sangria);
            for (int i = 0; i < cartas.Count; i++)
            {
                Console.ForegroundColor = cartas[i].Color;
                Console.Write(dibujos[i][linea]);
                Console.ForegroundColor = colorOriginal;
                Console.Write(' ');
            }
            Console.WriteLine();
        }

        Console.ForegroundColor = colorOriginal;
    }

    private static ValorCarta ConvertirValor(int valorNumerico)
    {
        if (valorNumerico < (int)ValorCarta.Dos || valorNumerico > (int)ValorCarta.As)
        {
            throw new ArgumentOutOfRangeException(nameof(valorNumerico), valorNumerico,
                "El valor numérico debe estar entre 2 y 14.");
        }

        return (ValorCarta)valorNumerico;
    }

    private static string Centrar(string texto, int ancho)
    {
        int izquierda = (ancho - texto.Length) / 2;
        return texto.PadLeft(izquierda + texto.Length).PadRight(ancho);
    }
}
