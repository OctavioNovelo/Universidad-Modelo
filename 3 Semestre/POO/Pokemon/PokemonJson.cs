using System.Collections.Generic;
using System.Text.Json.Serialization;

public class PokemonJson
{
    [JsonPropertyName("name")]
    public string Name { get; set; } = "";

    [JsonPropertyName("type")]
    public List<string> Type { get; set; } = new List<string>();

    [JsonPropertyName("hp")]
    public int Hp { get; set; }

    [JsonPropertyName("attack")]
    public int Attack { get; set; }
}
