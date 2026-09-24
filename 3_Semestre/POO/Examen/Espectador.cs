public class Espectador
{
    public string Nombre;
    public int Edad;
    public TarjetaClub? MiTarjeta;


    public Espectador(string name)
    {
        Nombre = name;
        Edad = 18;
        _ = new TarjetaClub();
    }
    public Espectador(string name, int a)
    {
        Nombre = name;
        Edad = a;
        _ = new TarjetaClub();
    }
}