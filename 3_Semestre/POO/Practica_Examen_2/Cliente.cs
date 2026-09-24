public class Cliente
{
    public string? Nombre;

    // TODO Ticket 1: encapsula este atributo (campo privado + propiedad pública).
    // Regla: el saldo nunca puede ser menor a $0.
    private double Saldo { 
        get 
        {
            return _saldo;
        } 
        set
        {
            if (value <= 0)
            {
                _saldo = 0;
            }
            else
            {
                _saldo = value;
            }
        }
    }

    public double _saldo;

    public Seguro? MiSeguro;

    // TODO Ticket 2: constructor que solo reciba "nombre" (Saldo inicia en $0).
    public Cliente(string name)
    {
        Nombre = name;
        Saldo = 0;
    }
    
    // TODO Ticket 3: dentro de este constructor, inicializa MiSeguro = new Seguro() e inicializar saldo;
    public Cliente(string name, double saldo)
    {
        Nombre = name;
        Saldo = saldo;
        _ = new Seguro();
    }

}
