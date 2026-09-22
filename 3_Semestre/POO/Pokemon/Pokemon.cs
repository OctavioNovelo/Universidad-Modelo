public class Pokemon
{
    public string nombre = "";
    public List<string> tipos;
    public int vida;
    public int ataque;
    public int  nivel;

    public void Atacar()
    {
        Console.WriteLine( nombre + " ataco ");
    }

    public void MostrarInformacion()
    {
        Console.WriteLine($"=== Pokemon: {nombre} (Nivel {nivel}) ===");
        Console.WriteLine($"Tipos: {string.Join(", ", tipos)}");
        Console.WriteLine($"Vida (HP): {vida}");
        Console.WriteLine($"Ataque: {ataque}");
        Console.WriteLine("========================================\n");
    }
}