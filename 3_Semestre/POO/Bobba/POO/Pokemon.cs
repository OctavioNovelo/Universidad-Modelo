using System.Text.Json.Nodes;

class Pokemon
{
    public string nombre;
    public List<string> tipos;
    public int ataque;

  
    private int _vida;
    private int _nivel = 1; 

    public int Vida
    {
        get { return _vida; }
        set
        {
            if (value < 0)
            {
                _vida = 0;
            }
            else
            {
                _vida = value;
            }
        }
    }

    public int Nivel
    {
        get { return _nivel; }
        set
        {
            if (value > 100)
            {
                Console.WriteLine($"Nivel {value} inválido: el máximo es 100.");
            }
            else if (value < 1)
            {
                Console.WriteLine($"Nivel {value} inválido: el mínimo es 1.");
            }
            else if (value < _nivel)
            {
                Console.WriteLine($"No se puede bajar el nivel de {_nivel} a {value}.");
            }
            else
            {
                _nivel = value;
            }
        }
    }

    public bool EstaDerrotado()
    {
        return Vida == 0;
    }

    public void RecibirDanio(int danio)
    {
        Vida -= danio; 
        Console.WriteLine($"{nombre} recibió {danio} de daño. Vida restante: {Vida}");
    }

    public void Atacar()
    {
        Console.WriteLine(nombre + " ataco");
    }

    public Pokemon()
    {
        nombre = "Mising No";
        tipos = new List<string>();
        Vida = 100;
        ataque = 20;
        Nivel = 1;
    }

    public Pokemon(string nombre, int vida, int ataque)
    {
        this.nombre = nombre;
        this.tipos = new List<string> { "Normal" };
        this.Vida = vida;
        this.ataque = ataque;
        this.Nivel = 1;
    }

    public Pokemon(PokemonJson data)
    {
        this.nombre = data.name;
        this.tipos = data.type;
        this.Vida = data.hp;
        this.ataque = data.Attack;
        this.Nivel = 1;
    }

    public void MostrarInformacion()
    {
        Console.WriteLine($"=== Pokémon: {nombre} (Nivel {Nivel}) ===");
        Console.WriteLine($"Tipos: {string.Join(", ", tipos)}");
        Console.WriteLine($"Vida (HP): {Vida}");
        Console.WriteLine($"Ataque: {ataque}");
        Console.WriteLine("==================================\n");
    }
}