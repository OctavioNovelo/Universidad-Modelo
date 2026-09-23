using System.Dynamic;
using System.Security.Cryptography.X509Certificates;

public class Gamer
{
    public string Nickname = "";

    public double Saldo
    {
        get {return _saldo;}
        set {
            if (value < 0) 
            { 
                _saldo = 0;
            }
            else
            {
                _saldo = value;
            }
            }
    }

    private double _saldo;

    public Membresia? MiMembresia; // Con ? lo marcamos como nullable.

    public Gamer(string name)
    {
        Nickname = name;
        Saldo = 0;
        Membresia membresia = new Membresia();
    }

    public Gamer(string name, int Saldo)
    {
        Nickname = name;
        this.Saldo = Saldo;
        Membresia membresia = new Membresia();
    }
}
