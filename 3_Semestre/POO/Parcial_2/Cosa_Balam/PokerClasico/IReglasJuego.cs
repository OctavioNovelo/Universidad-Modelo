
namespace PokerClasico;

// Conjunto de reglas
public interface IReglasJuego
{
    string NombreJuego { get; }
    string Descripcion { get; }
    void Repartir(Mazo mazo, List<Jugador> jugadores);
    int EvaluarPuntuacion(List<Carta> mano, out string descripcionJugada);
    string DeterminarGanador(List<Jugador> jugadores);
}
