// See https://aka.ms/new-console-template for more information
using System.Text.Json;

class Program
{
    static void Main()
    {
        string json = File.ReadAllText("pokemon.json");
        List<PokemonJson> datos = JsonSerializer.Deserialize<List<PokemonJson>>(json) ?? new List<PokemonJson>();


        Pokemon Bulbasur = new Pokemon();
        Bulbasur.name = datos[0].name;
        Bulbasur.tipos = datos[0].type;
        Bulbasur.vida = datos[0].hp;
        Bulbasur.ataque = datos[0].attack;
        Bulbasur.nivel = 1;
        Bulbasur.MostrarInformacion();

        Console.WriteLine(datos[0].Name);
    }
}
