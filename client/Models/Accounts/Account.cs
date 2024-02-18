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
}
