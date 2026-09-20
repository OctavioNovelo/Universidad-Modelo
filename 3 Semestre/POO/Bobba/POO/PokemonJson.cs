using System.Collections.Generic;
using System.Text.Json.Serialization;

public class PokemonJson
{
    [JsonPropertyName("name")]
    public string name { get; set; } = "";

    [JsonPropertyName("type")]
    public List<string> type { get; set; } = new List<string>();

    [JsonPropertyName("hp")]
    public int hp { get; set; }

    [JsonPropertyName("attack")]
    public int Attack { get; set; }
}
