namespace PokerClasico;

// Jugador
public class Jugador
{
    public int Id { get; private set; }
    public string Nombre { get; private set; }
    public List<Carta> Mano { get; private set; }
    public int Puntuacion { get; private set; }
    public string DetalleJugada { get; private set; }

    
    // Constructor
    public Jugador(string nombre, int id)
    {
        // Comprobacin de chill
        if (string.IsNullOrWhiteSpace(nombre))
        {
            throw new ArgumentException("El nombre del jugador no puede estar vacío.", nameof(nombre));
        }

        Id = id;
        Nombre = nombre;
        Mano = new List<Carta>();
        Puntuacion = 0;
        DetalleJugada = string.Empty;
    }

    // Con : el constructor delega la incializacion a otro contructor de la misma clase, en este casi el de arriba
    public Jugador(string nombre) : this(nombre, 0)
    {
    }  

    // Metodos
    // Recibir UNA carta
    public void RecibirCarta(Carta carta)
    {
        if (carta == null)
        {
            throw new ArgumentNullException(nameof(carta));
        }
        Mano.Add(carta); // Agregamos la carta a la mano. 
    }

    // Recibir VARIAS cartas
    public void RecibirCarta(List<Carta> cartas)
    {
        if (cartas == null)
        {
            throw new ArgumentNullException(nameof(cartas));
        }
        foreach (Carta carta in cartas)
        {
            RecibirCarta(carta); // omg parece recursivo pero no es xdxdxxdxdxdxd
        }
    }

    // Guarda el resultado de la evaluación de la mano.  
    public void AsignarResultado(int puntuacion, string detalleJugada)
    {
        Puntuacion = puntuacion;
        DetalleJugada = detalleJugada ?? string.Empty;
    }

    // Borramos la mano. 
    public void LimpiarMano()
    {
        Mano.Clear();
        Puntuacion = 0;
        DetalleJugada = string.Empty;
    }

    public override string ToString() => Id > 0 ? $"{Nombre} (#{Id})" : Nombre;
}
