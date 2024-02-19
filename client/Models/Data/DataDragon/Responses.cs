// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

// ReSharper disable InconsistentNaming
// ReSharper disable UnusedMember.Global
// ReSharper disable IdentifierTypo
// ReSharper disable ClassNeverInstantiated.Global
// ReSharper disable CollectionNeverUpdated.Global
// ReSharper disable UnusedAutoPropertyAccessor.Global

#pragma warning disable CS8618 // Non-nullable field must contain a non-null value when exiting constructor. Consider declaring as nullable.
namespace client.Models.Data.DataDragon;

public class RegionVersion
{
    public string Version
    {
        get => this.v;
    }

    public Dictionary<string, string> n { get; set; }
    public string v { get; set; }
    public string l { get; set; }
    public string cdn { get; set; }
    public string dd { get; set; }
    public string lg { get; set; }
    public string css { get; set; }
    public int profileiconmax { get; set; }
    public object store { get; set; }
}

public class Versions : Simple
{
    public List<string> versions { get; set; }

    public string latestVersion
    {
        get => this.versions[0];
    }
}

public interface Simple { }
