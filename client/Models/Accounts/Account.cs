// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using System.Text.Json;
using Camille.Enums;

namespace client.Models.Accounts;

public struct Account
{
    public Guid ID { get; set; }
    public string GameName { get; set; }
    public string TagLine { get; set; }
    public string RiotID { get; set; }

    public PlatformRoute Region { get; set; }
    public RegionalRoute Continent { get; set; }

    public Account(string gameName, string tagLine, PlatformRoute region)
    {
        this.ID = Guid.NewGuid();

        this.GameName = gameName;
        this.TagLine = tagLine;
        this.RiotID = $"{this.GameName}#{this.TagLine}";

        this.Region = region;
        this.Continent = region.ToRegional();
    }

    public void save()
    {
        string jsonString = JsonSerializer.Serialize(this);
        Console.WriteLine(jsonString);
    }
}
