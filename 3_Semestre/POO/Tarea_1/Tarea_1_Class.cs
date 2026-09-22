interface IAcciones
{
    void Atacar(Papu objetivo);
    void Damage(int dano);
}
class Papu : IAcciones
{
    public string nombre;
    public int vida;
    public int ataque;
    public int nivel;


    // Constructor
    public Papu()
    {
        vida = 100;
        ataque = 10;
        nivel = 1;
    }

    public void Atacar(Papu objetivo)
    {
        Console.WriteLine(nombre + " ataca a " + objetivo.nombre + " por " + ataque + " de daño");
        objetivo.Damage(ataque);
    }

    public void Damage(int dano)
    {
        vida -= dano;
        if (vida < 0) vida = 0;
        Console.WriteLine(nombre + " recibe " + dano + " de daño. Vida restante: " + vida);
    }
}