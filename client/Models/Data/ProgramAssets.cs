// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using System.Text.Json;
using Camille.Enums;
using client.Models.Data.DataDragon;

namespace client.Models.Data;

public class ProgramAssets
{
    /// <summary>
    ///     Convert the user's <see cref="PlatformRoute" /> to a string.
    /// </summary>
    private readonly static string regionString =
        Program.Account.Region.AsRegionString().ToLower();
    /// <summary>
    ///     The locale used for the game data downloads.
    /// </summary>
    /// <remarks>
    ///     TODO: This should be an option on Login and in settings once app is
    ///     localized.
    /// </remarks>
    private readonly static string locale = "en_US";

    /// <summary>
    ///     The URL to get all versions available in game data.
    /// </summary>
    private readonly static string versionsURL =
        "https://ddragon.leagueoflegends.com/api/versions.json";

    /// <summary>
    ///     The version of the game on the user's region.
    /// </summary>
    private string _version = "";

    /// <summary>
    ///     The version of the game on the user's region.
    /// </summary>
    public string Version
    {
        get => this._version == "" ? getVersion() : this._version;
    }

    /// <summary>
    ///     Contacts the Data Dragon API and deserializes it into the given response.
    /// </summary>
    /// <param name="url">DataDragon URL</param>
    /// <typeparam name="T">
    ///     Response Class from <see cref="client.Models.Data.DataDragon" />
    /// </typeparam>
    /// <returns>The URL response, formatted into the specified Response</returns>
    private static T getDataDragon<T>(string url)
    {
        // Ensure the type is from the DataDragon namespace
        if (!typeof(T).Namespace!.Contains("DataDragon"))
        {
            throw new ArgumentException(
                    "Type must be from the DataDragon namespace"
                );
        }

        try
        {
            // Call the API
            var client = new HttpClient();
            var response = client.GetAsync(url);
            // Read back the response
            var result = response.Result.Content.ReadAsStringAsync();

            // Return the response, deserialized into the given type, if not Simple
            if (!typeof(Simple).IsAssignableFrom(typeof(T)))
                return JsonSerializer.Deserialize<T>(result.Result)!;

            // Get the type of the first variable in T, and save the variable
            // name
            Type type = typeof(T).GetProperties()[0].PropertyType;
            string variable = typeof(T).GetProperties()[0].Name;

            // Deserialize the response into the type of the first variable in T
            object deserialized = JsonSerializer.Deserialize(
                    result.Result,
                    type
                )!;

            // Create a new instance of T
            var newT = (T)Activator.CreateInstance(typeof(T))!;

            // Set the first variable in T to the deserialized response
            newT.GetType().GetProperty(variable)!.SetValue(
                    newT,
                    deserialized
                );

            // Return the new instance of T
            return newT;
        }
        // Handle un-parseable responses
        catch (Exception)
        {
            throw new ArgumentException(
                    "The response used in the DataDragon namespace does not "
                    + "match the API response: "
                    + url
                    + " -> "
                    + typeof(T)
                );
        }
    }

#pragma warning disable CS1998 // Async method lacks 'await' operators and will run synchronously
    private async Task setup(Action<string, string> updateStatus)
#pragma warning restore CS1998 // Async method lacks 'await' operators and will run synchronously
    {
        updateStatus(
                "Downloading...",
                "Version data"
            );
        getVersion();
        getVersions();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Champion data"
            );
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Item data"
            );
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Summoner Spell data"
            );
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Summoner Spell images"
            );
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Rank images"
            );
        await Task.Delay(200);

        updateStatus(
                "Cleaning up...",
                ""
            );
        await Task.Delay(200);
    }

    public async void checkForUpdates(Action<string, string> updateStatus)
    {
        string versionsFile = Constants.dataDragonFolder + "versions.json";
        updateStatus(
                "Checking for updates...",
                ""
            );

        // Check that every Data Dragon file exists
        if (FileManagement.fileHasContent(
                    Constants.dataDragonFolder + "champions.json"
                )
            && FileManagement.fileHasContent(
                    Constants.dataDragonFolder + "versions.json"
                )
            && FileManagement.fileHasContent(
                    Constants.dataDragonFolder + "items.json"
                )
            && FileManagement.fileHasContent(
                    Constants.dataDragonFolder + "summonerSpells.json"
                )
            && FileManagement.fileHasContent(
                    Constants.dataDragonFolder + "summonerSpells.json"
                )
            && FileManagement.fileHasContent(
                    Constants.imageCacheFolder + "Flash.png"
                ))
        {
            // If all the files exist...

            // If the versions file does exist, check it
            FileManagement.loadFromFile(
                    Constants.dataDragonFolder + "versions.json",
                    out Versions? versions
                );

            // If the latest version is the same as the current version, bail
            if (versions!.latestVersion == this.Version)
                return;
        }

        // Re-download the data dragon files if no check bailed the process
        FileManagement.emptyDirectory(Constants.dataDragonFolder);
        await setup(updateStatus);
    }

    private static void getVersions()
    {
        var versions = getDataDragon<Versions>(versionsURL);

        FileManagement.saveToFile(
                Constants.dataDragonFolder + "versions.json",
                versions
            );
    }

    /// <summary>
    ///     Get the current version of the game data for the user's region.
    /// </summary>
    /// <returns>A League Version</returns>
    private string getVersion()
    {
        var response = getDataDragon<RegionVersion>(this.RegionVersionURL);
        string version = response.Version;

        Program.LeagueVersion = version;
        this._version = version;
        return version;
    }

    #region URLs

    /// <summary>
    ///     The URL to get the current version of the game data given the user's
    ///     region.
    /// </summary>
    // ReSharper disable once MemberCanBeMadeStatic.Local
#pragma warning disable CA1822
    private string RegionVersionURL
#pragma warning restore CA1822
    {
        get => $"https://ddragon.leagueoflegends.com/realms/{regionString}.json";
    }

    /// <summary>
    ///     The URL to get the current champion list data.
    /// </summary>
    private string ChampionDataURL
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this.Version}/data/{locale}/champion.json";
    }

    /// <summary>
    ///     The URL Format to get a champion's picture.
    /// </summary>
    /// <remarks>
    ///     {0} must be replaced with the champion's name.
    /// </remarks>
    private string ChampionPictureURLFormat
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this.Version}/img/champion/{{0}}.png";
    }

    /// <summary>
    ///     The URL Format to get a champion's passive picture.
    /// </summary>
    /// <remarks>
    ///     {0} must be replaced with the champion's name.
    /// </remarks>
    private string ChampionPassivePictureURL
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this.Version}/img/passive/{{0}}_P.png";
    }

    /// <summary>
    ///     The URL Format to get a champion's ability picture.
    /// </summary>
    /// <remarks>
    ///     {0} must be replaced with the ability's name.
    /// </remarks>
    private string ChampionAbilityPictureURLFormat
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this.Version}/img/spell/{{0}}.png";
    }

    /// <summary>
    ///     The URL to get the current item list data.
    /// </summary>
    private string ItemDataURL
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this.Version}/data/{locale}/item.json";
    }

    /// <summary>
    ///     The URL Format to get an item's picture.
    /// </summary>
    /// <remarks>
    ///     {0} must be replaced with the item's ID.
    /// </remarks>
    private string ItemPictureURLFormat
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this.Version}/img/item/{{0}}.png";
    }

    /// <summary>
    ///     The URL to get the current summoner spell list data.
    /// </summary>
    private string SummonerSpellDataURL
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this.Version}/data/{locale}/summoner.json";
    }

    /// <summary>
    ///     The URL Format to get a summoner spell's picture.
    /// </summary>
    /// <remarks>
    ///     {0} must be replaced with the summoner spell's name.
    /// </remarks>
    private string SummonerSpellPictureURLFormat
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this.Version}/img/spell/Summoner{{0}}.png";
    }

    /// <summary>
    ///     The URL Format to get a profile picture.
    /// </summary>
    /// <remarks>
    ///     {0} must be replaced with the profile picture ID.
    /// </remarks>
    private string ProfilePictureURLFormat
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this.Version}/img/profileicon/{{0}}.png";
    }

    #endregion
}
