public class Sala
{
    public int NumeroSala;
    public int CapacidadMaxima;
    public Pelicula PeliculaProyectada;

    private int _asientosOcupados;
  
    public int AsientosOcupados 
    { 
        get { return _asientosOcupados; }
        set { if (value >= CapacidadMaxima) _asientosOcupados = CapacidadMaxima;
            else
            {
                _asientosOcupados = value;
            } 
        }
    }

  
    public int AsientosDisponibles 
    {
        get {return CapacidadMaxima - _asientosOcupados ; }
    }

    public Sala(int numero, int capacidad, Pelicula pelicula)
    {
        NumeroSala = numero;
        CapacidadMaxima = capacidad;
        PeliculaProyectada = pelicula;
        _asientosOcupados = 0;
    }
}