using PokerClasico.Modelos;

namespace PokerClasico.Reglas;

/// <summary>
/// Contrato que cualquier conjunto de reglas debe proporcionar al motor.
/// </summary>
public interface IReglasJuego
{
    string NombreJuego { get; }
    string Descripcion { get; }
    void Repartir(Mazo mazo, List<Jugador> jugadores);
    int EvaluarPuntuacion(List<Carta> mano, out string descripcionJugada);
    string DeterminarGanador(List<Jugador> jugadores);
}
