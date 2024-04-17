// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using Camille.Enums;

#endregion

namespace client.Models.Data.DataDragon;

public class DataDragonURLs(string version, string locale)
{
    /// <summary>
    ///     The URL to get all versions available in game data.
    /// </summary>
    public const string VERSIONS_URL =
        "https://ddragon.leagueoflegends.com/api/versions.json";

    /// <summary>
    ///     Convert the user's <see cref="PlatformRoute">Platform</see> to a string.
    /// </summary>
    private readonly static string regionString =
        Program.Account.Region.AsRegionString().ToLower();

    /// <summary>
    ///     The locale used for the game data downloads.
    /// </summary>
    private readonly string _locale = locale;

    /// <summary>
    ///     The version of the game on the user's region from the Data Dragon API.
    /// </summary>
    private readonly string _version = version;

    /// <summary>
    ///     The URL to get the current version of the game data given the user's
    ///     region.
    /// </summary>
    public static string RegionVersionURL
    {
        get => $"https://ddragon.leagueoflegends.com/realms/{regionString}.json";
    }

    /// <summary>
    ///     The URL to get the current champion list data.
    /// </summary>
    public string ChampionsDataURL
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this._version}/data/{this._locale}/champion.json";
    }

    /// <summary>
    ///     The URL to get a specific champion's data.
    /// </summary>
    public string ChampionDataURL
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this._version}/data/{this._locale}/champion/{{0}}.json";
    }

    /// <summary>
    ///     The URL to get the current item list data.
    /// </summary>
    public string ItemDataURL
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this._version}/data/{this._locale}/item.json";
    }

    /// <summary>
    ///     The URL to get the current summoner spell list data.
    /// </summary>
    public string SummonerSpellDataURL
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this._version}/data/{this._locale}/summoner.json";
    }

    /// <summary>
    ///     The URL to get the current rune list data.
    /// </summary>
    public string RuneDataURL
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this._version}/data/{this._locale}/runesReforged.json";
    }

    /// <summary>
    ///     The URL to get profile picture list data.
    /// </summary>
    public string ProfilePictureDataURL
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this._version}/data/{this._locale}/profileicon.json";
    }
}
