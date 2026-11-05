using PokerClasico.Modelos;

namespace PokerClasico.Reglas;

/// <summary>
/// Clase base abstracta para cualquier juego de cartas.
/// </summary>
public abstract class ReglasJuegoBase : IReglasJuego
{
    public string NombreJuego { get; protected set; }
    public string Descripcion { get; protected set; }

    protected ReglasJuegoBase(string nombreJuego, string descripcion)
    {
        NombreJuego = nombreJuego;
        Descripcion = descripcion;
    }

    public abstract void Repartir(Mazo mazo, List<Jugador> jugadores);
    public abstract int EvaluarPuntuacion(List<Carta> mano, out string descripcionJugada);
    public abstract string DeterminarGanador(List<Jugador> jugadores);
}
