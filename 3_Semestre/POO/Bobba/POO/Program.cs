using System.Globalization;
using System.Text.Json;

class Program
{
    static void Main()
    {
        string json = File.ReadAllText("pokemon.json");
        List<PokemonJson> datos = JsonSerializer.Deserialize<List<PokemonJson>>(json);

        Pokemon Default = new Pokemon();
        Default.MostrarInformacion();

    }
}