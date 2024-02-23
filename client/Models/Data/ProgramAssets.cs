// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using System.Text.Json;
using Camille.Enums;
using client.Models.Data.DataDragon;
using Champion = client.Models.Data.DataDragon.Champion;

namespace client.Models.Data;

public class ProgramAssets
{
    /// <summary>
    ///     Contacts the Data Dragon API and deserializes it into the given response
    ///     type.
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
            var error = new ArgumentException(
                    "Type must be from the DataDragon namespace"
                );
            Program.log(
                    source: nameof(ProgramAssets),
                    method: "getDataDragon()",
                    message: "Type must be from the DataDragon namespace\n" + error,
                    debugSymbols: [typeof(T).Name],
                    url: url,
                    logLevel: LogLevel.fatal
                );
            throw error;
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
            {
                Program.log(
                        source: nameof(ProgramAssets),
                        method: "getDataDragon()",
                        doing: "Downloading",
                        message: typeof(T).Name + " (complex)",
                        url: url,
                        logLevel: LogLevel.debug
                    );
                return JsonSerializer.Deserialize<T>(result.Result)!;
            }

            Program.log(
                    source: nameof(ProgramAssets),
                    method: "getDataDragon()",
                    doing: "Downloading",
                    message: typeof(T).Name + " (simple)",
                    url: url,
                    logLevel: LogLevel.debug
                );

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
        catch (Exception e)
        {
            throw new ArgumentException(
                    "The response used in the DataDragon namespace does not "
                    + "match the API response: \n"
                    + url
                    + " -> "
                    + typeof(T)
                    + "\n"
                    + e
                    + "\n"
                );
        }
    }

    /// <summary>
    ///     Run the download of all current game data, and some images.
    /// </summary>
    /// <param name="updateStatus">The action to update the status text</param>
    private async Task setup(Action<string, string> updateStatus)
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
        getChampions();
        getEachChampion();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Champion images"
            );
        getChampionImages();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Item data"
            );
        getItems();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Runes data"
            );
        getRunes();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Runes images"
            );
        getRuneImages();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Summoner Spell data"
            );
        getSummonerSpells();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Summoner Spell images"
            );
        getSummonerSpellImages();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Rank images"
            );
        getRankImages();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Profile Picture data"
            );
        getProfilePictures();
        await Task.Delay(200);

        updateStatus(
                "Cleaning up...",
                ""
            );
        await Task.Delay(700);
    }

    /// <summary>
    ///     Check the downloaded files and the live game version to see if the game
    ///     data should be re-downloaded.
    /// </summary>
    /// <param name="updateStatus">The action to update the status text</param>
    /// <seealso cref="setup" />
    public async Task checkForUpdates(Action<string, string> updateStatus)
    {
        updateStatus(
                "Checking for updates...",
                ""
            );

        bool haveFiles = noMissingFiles();
        bool versionUp = versionUpToDate();

        Program.log(
                source: nameof(ProgramAssets),
                method: "checkForUpdates()",
                message: "Checking if update is necessary...",
                debugSymbols:
                [
                    $"files all available: {haveFiles}",
                    $"version up to date: {versionUp}",
                ],
                logLevel: LogLevel.debug
            );

        // Check if all files are accessible and the version is up to date
        if (haveFiles && versionUp)
        {
            Program.log(
                    source: nameof(ProgramAssets),
                    method: "checkForUpdates()",
                    message: $"Already on {this.Version}",
                    logLevel: LogLevel.info
                );
            await Task.Delay(1200);
            return;
        }

        // Re-download the data dragon files if no check bailed the process
        Program.log(
                source: nameof(ProgramAssets),
                method: "checkForUpdates()",
                message: $"Updating to {this.Version}...",
                logLevel: LogLevel.info
            );
        FileManagement.emptyDirectory(Constants.dataDragonFolder);
        FileManagement.createDirectory(Constants.dataDragonChampionFolder);
        FileManagement.emptyDirectory(Constants.imageCacheDataDragonFolder);
        await setup(updateStatus);

        // Succeed
        Program.log(
                source: nameof(ProgramAssets),
                method: "checkForUpdates()",
                message: "Updated",
                logLevel: LogLevel.info
            );
    }

    /// <summary>
    ///     Check if the game data is missing from the user's computer.
    /// </summary>
    /// <returns>If all downloaded files are present</returns>
    private static bool noMissingFiles()
    {
        return
            FileManagement.fileHasContent(
                    Constants.dataDragonFolder + "champions.json"
                )
            || FileManagement.fileHasContent(
                    Constants.dataDragonFolder + "versions.json"
                )
            || FileManagement.fileHasContent(
                    Constants.dataDragonFolder + "items.json"
                )
            || FileManagement.fileHasContent(
                    Constants.dataDragonFolder + "summonerSpells.json"
                )
            || FileManagement.fileHasContent(
                    Constants.dataDragonFolder + "runes.json"
                )
            || FileManagement.fileHasContent(
                    Constants.dataDragonFolder + "profilePictures.json"
                )
            || FileManagement.fileHasContent(
                    Constants.imageCacheDataDragonFolder + "spell.Flash.png"
                )
            || FileManagement.fileHasContent(
                    Constants.imageCacheDataDragonFolder + "rank.Emerald.png"
                );
    }

    /// <summary>
    ///     Check if the latest version data is out of date.
    /// </summary>
    /// <returns>
    ///     If the latest downloaded version matches the latest game version
    /// </returns>
    private bool versionUpToDate()
    {
        // If the versions file does exist, check it
        FileManagement.loadFromFile(
                Constants.dataDragonFolder + "versions.json",
                out Versions? versions
            );

        // If the latest version is the same as the current version
        return versions!.latestVersion == this.Version;
    }

    /// <summary>
    ///     Get the current version of the game data for the user's region from the
    ///     Data Dragon API.
    /// </summary>
    /// <returns>A League Version</returns>
    private string getVersion()
    {
        var response = getDataDragon<RegionVersion>(this.RegionVersionURL);
        string version = response.Version;

        this._version = version;
        return version;
    }

    /// <summary>
    ///     Get the versions list from the Data Dragon API.
    /// </summary>
    /// <returns>A list of League Versions</returns>
    private Versions getVersions()
    {
        Versions versions;
        string file = Constants.dataDragonFolder + "versions.json";

        // Load the versions list if it exists
        if (FileManagement.fileHasContent(file))
        {
            FileManagement.loadFromFile(
                    file,
                    out versions!
                );
        }
        // Download and save the versions list
        else
        {
            versions = getDataDragon<Versions>(versionsURL);

            FileManagement.saveToFile(
                    file,
                    versions
                );
        }

        this._versions = versions;
        return versions;
    }

    /// <summary>
    ///     Get the champion list from the Data Dragon API.
    /// </summary>
    /// <returns>A list of League Champions</returns>
    private Champions getChampions()
    {
        Champions champions;
        string file = Constants.dataDragonFolder + "champions.json";

        // Load the versions list if it exists
        if (FileManagement.fileHasContent(file))
        {
            FileManagement.loadFromFile(
                    file,
                    out champions!
                );
        }
        // Download and save the versions list
        else
        {
            champions = getDataDragon<Champions>(this.ChampionsDataURL);

            FileManagement.saveToFile(
                    file,
                    champions
                );
        }

        this._champions = champions;
        return champions;
    }

    /// <summary>
    ///     Get the individual champion data from the Data Dragon API.
    /// </summary>
    /// <returns>A League Champion</returns>
    private List<IndividualChampion> getEachChampion()
    {
        List<IndividualChampion> champions = [];
        string folder = Constants.dataDragonChampionFolder;

        // Iterate over each champion from the champion list
        foreach (string championName in this.Champions.data.Select(
                         champion => champion.Value.id
                     ))
        {
            IndividualChampion individualChampion;
            string file = folder + championName + ".json";

            // Load the individual champion if it exists
            if (FileManagement.fileHasContent(file))
            {
                FileManagement.loadFromFile(
                        file,
                        out individualChampion!
                    );
            }
            // Download and save the individual champion
            else
            {
                individualChampion = getDataDragon<IndividualChampion>(
                        string.Format(
                                this.ChampionDataURL,
                                championName
                            )
                    );

                FileManagement.saveToFile(
                        file,
                        individualChampion
                    );
            }

            champions.Add(individualChampion);
        }

        this._champion = champions;
        return champions;
    }

    /// <summary>
    ///     Get the images for each champion and their abilities from the Data Dragon
    ///     API.
    /// </summary>
    private void getChampionImages()
    {
        string folder = Constants.imageCacheDataDragonFolder;

        // Iterate over each champion where the image does not already exist
        foreach (Champion champion in this
                     .Champion
                     .Select(individualChampion => individualChampion.Champion)
                     .Where(
                             champion => !FileManagement.fileHasContent(
                                     folder + "champion." + champion.image.full
                                 )
                         ))
        {
            // Download the champion's image if not
            Task.Run(
                    () => FileManagement.downloadImage(
                            champion.image.imageURL,
                            folder + "champion." + champion.image.full
                        )
                );

            #region Abilities

            // Iterate over each ability from the champion
            var abilityLabels = new List<string> { "Q", "W", "E", "R", "P" };
            int counter = 0;
            foreach (ChampionSpell ability in champion.spells)
                // Download the ability's image
            {
                int counterForTask = counter;
                Task.Run(
                        () => FileManagement.downloadImage(
                                ability.image.imageURL,
                                folder
                                + "champion_ability."
                                + champion.id
                                + abilityLabels[counterForTask]
                                + ability.image.full[
                                    ability.image.full.LastIndexOf('.')..]
                            )
                    );
                counter++;
            }

            // Download the passive's image
            Task.Run(
                    () => FileManagement.downloadImage(
                            champion.passive.image.imageURL,
                            folder
                            + "champion_ability."
                            + champion.id
                            + "P"
                            + champion.passive.image.full[
                                champion.passive.image.full.LastIndexOf('.')..]
                        )
                );

            #endregion
        }
    }

    /// <summary>
    ///     Get the item list from the Data Dragon API.
    /// </summary>
    /// <returns>A list of League Items</returns>
    private Items getItems()
    {
        Items items;
        string file = Constants.dataDragonFolder + "items.json";

        // Load the versions list if it exists
        if (FileManagement.fileHasContent(file))
        {
            FileManagement.loadFromFile(
                    file,
                    out items!
                );
        }
        // Download and save the versions list
        else
        {
            items = getDataDragon<Items>(this.ItemDataURL);

            FileManagement.saveToFile(
                    file,
                    items
                );
        }

        this._items = items;
        return items;
    }

    /// <summary>
    ///     Get the rune list from the Data Dragon API.
    /// </summary>
    /// <returns>A list of League Runes</returns>
    private Runes getRunes()
    {
        Runes runes;
        string file = Constants.dataDragonFolder + "runes.json";

        // Load the versions list if it exists
        if (FileManagement.fileHasContent(file))
        {
            FileManagement.loadFromFile(
                    file,
                    out runes!
                );
        }
        // Download and save the versions list
        else
        {
            runes = getDataDragon<Runes>(this.RuneDataURL);

            FileManagement.saveToFile(
                    file,
                    runes
                );
        }

        this._runes = runes;
        return runes;
    }

    /// <summary>
    ///     Get the images for each rune and keystone from the Data Dragon API.
    /// </summary>
    private void getRuneImages()
    {
        string folder = Constants.imageCacheDataDragonFolder;

        // Iterate over each rune where the image does not already exist
        foreach (RuneTree runeTree in this.Runes.runetrees.Where(
                         rune => !FileManagement.fileHasContent(
                                 folder + "rune_tree." + rune.image.sprite
                             )
                     ))
        {
            // Download the tree's image
            Task.Run(
                    () => FileManagement.downloadImage(
                            runeTree.image.imageURL,
                            folder
                            + "rune_tree."
                            + runeTree.image.sprite
                            + runeTree.image.full[
                                runeTree.image.full.LastIndexOf('.')..],
                            32
                        )
                );

            // Iterate over each rune in the tree
            foreach (Rune rune in runeTree.slots.SelectMany(slot => slot.runes))
            {
                // Download the rune's image
                Task.Run(
                        () => FileManagement.downloadImage(
                                rune.image.imageURL,
                                folder
                                + "rune."
                                + rune.image.sprite
                                + rune.image.full[
                                    rune.image.full.LastIndexOf('.')..],
                                32
                            )
                    );
            }
        }
    }

    /// <summary>
    ///     Get the summoner spell list from the Data Dragon API.
    /// </summary>
    /// <returns>A list of League Summoner Spells</returns>
    private SummonerSpells getSummonerSpells()
    {
        SummonerSpells summonerSpells;
        string file = Constants.dataDragonFolder + "summonerSpells.json";

        // Load the versions list if it exists
        if (FileManagement.fileHasContent(file))
        {
            FileManagement.loadFromFile(
                    file,
                    out summonerSpells!
                );
        }
        // Download and save the versions list
        else
        {
            summonerSpells =
                getDataDragon<SummonerSpells>(this.SummonerSpellDataURL);

            FileManagement.saveToFile(
                    file,
                    summonerSpells
                );
        }

        this._summonerSpells = summonerSpells;
        return summonerSpells;
    }

    /// <summary>
    ///     Get the images for each summoner spell from the Data Dragon API.
    /// </summary>
    private void getSummonerSpellImages()
    {
        string folder = Constants.imageCacheDataDragonFolder;

        // Iterate over each summoner spell where the image does not already exist
        foreach (SummonerSpell summonerSpell in
                 this.SummonerSpells.data.Values.Where(
                         spell => !FileManagement.fileHasContent(
                                 folder
                                 + "spell."
                                 + spell.name
                                 + spell.image.full[
                                     spell.image.full.LastIndexOf('.')..]
                             )
                     ))
        {
            // Download the spell's image
            Task.Run(
                    () => FileManagement.downloadImage(
                            summonerSpell.image.imageURL,
                            folder
                            + "spell."
                            + summonerSpell.name
                            + summonerSpell.image.full[
                                summonerSpell.image.full.LastIndexOf('.')..]
                        )
                );
        }
    }

    /// <summary>
    ///     Get the profile picture list from the Data Dragon API.
    /// </summary>
    /// <returns>A list of League Profile Pictures</returns>
    private ProfileIcons getProfilePictures()
    {
        ProfileIcons profilePictures;
        string file = Constants.dataDragonFolder + "profilePictures.json";

        // Load the versions list if it exists
        if (FileManagement.fileHasContent(file))
        {
            FileManagement.loadFromFile(
                    file,
                    out profilePictures!
                );
        }
        // Download and save the versions list
        else
        {
            profilePictures =
                getDataDragon<ProfileIcons>(this.ProfilePictureDataURL);

            FileManagement.saveToFile(
                    file,
                    profilePictures
                );
        }

        this._profilePictures = profilePictures;
        return profilePictures;
    }

    /// <summary>
    ///     Get the Ranked Images from a Data Dragon bundle.
    /// </summary>
    private void getRankImages()
    {
        string folder = Constants.imageCacheDataDragonFolder;

        Program.log(
                source: nameof(ProgramAssets),
                method: "getRankImages()",
                doing: "Downloading",
                message: "Ranked Images",
                debugSymbols:
                [
                    $"path: {folder}",
                    "size: 256",
                ],
                url: this.RankedEmblemsURL,
                logLevel: LogLevel.debug
            );

        // Skip downloading if the images already exist
        if (FileManagement.fileHasContent(folder + "rank.Emerald.png"))
            return;

        // Download the ranked emblems and unpack them
        FileManagement.downloadFile(
                this.RankedEmblemsURL,
                folder + "ranked_emblems.zip"
            );
        FileManagement.unpackFile(
                folder + "ranked_emblems.zip",
                folder
            );

        // Delete the zip file
        FileManagement.deleteFile(folder + "ranked_emblems.zip");

        // Go into the folder
        string tempFolder = folder + "Ranked Emblems Latest\\";

        // Delete the folders we don't need
        FileManagement.deleteDirectory(tempFolder + "Wings\\");
        FileManagement.deleteDirectory(tempFolder + "Tier Wings\\");

        // Iterate over each file in the folder and move them up a directory
        foreach (string file in Directory.GetFiles(tempFolder))
        {
            // Rename the file to remove the "Rank=" part
            string fileName = Path.GetFileName(file);
            string oldDestination = tempFolder + fileName;
            string newFileName =
                "rank." + fileName[(fileName.LastIndexOf('=') + 1)..];
            string destination = folder + newFileName;

            // Resize the crazy-big images
            FileManagement.resizeImage(
                    oldDestination,
                    256
                );

            // Move the files up out of the temporary folder
            File.Move(
                    oldDestination,
                    destination
                );
        }

        // Delete the temporary folder
        FileManagement.deleteDirectory(tempFolder);
    }

    #region Variables and their Backers

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
    // ReSharper disable once ConvertToConstant.Local
    private readonly static string locale = "en_US";

    /// <summary>
    ///     The URL to get all versions available in game data.
    /// </summary>
    // ReSharper disable once ConvertToConstant.Local
    private readonly static string versionsURL =
        "https://ddragon.leagueoflegends.com/api/versions.json";

    /// <summary>
    ///     Each champion from the Data Dragon API.
    /// </summary>
    private List<IndividualChampion>? _champion;

    /// <summary>
    ///     The champion list from the Data Dragon API.
    /// </summary>
    private Champions? _champions;

    /// <summary>
    ///     The item list from the Data Dragon API.
    /// </summary>
    private Items? _items;

    /// <summary>
    ///     The profile picture list from the Data Dragon API.
    /// </summary>
    private ProfileIcons? _profilePictures;

    /// <summary>
    ///     The rune list from the Data Dragon API.
    /// </summary>
    private Runes? _runes;

    /// <summary>
    ///     The summoner spell list from the Data Dragon API.
    /// </summary>
    private SummonerSpells? _summonerSpells;

    /// <summary>
    ///     The version of the game on the user's region from the Data Dragon API.
    /// </summary>
    private string? _version;

    /// <summary>
    ///     The versions list from the Data Dragon API.
    /// </summary>
    private Versions? _versions;

    /// <summary>
    ///     The version of the game on the user's region from the Data Dragon API.
    /// </summary>
    public string Version
    {
        get => this._version ?? getVersion();
    }

    /// <summary>
    ///     The versions list from the Data Dragon API.
    /// </summary>
    public Versions Versions
    {
        get => this._versions ?? getVersions();
    }

    /// <summary>
    ///     The champion list from the Data Dragon API.
    /// </summary>
    public Champions Champions
    {
        get => this._champions ?? getChampions();
    }

    /// <summary>
    ///     Each champion from the Data Dragon API.
    /// </summary>
    public IEnumerable<IndividualChampion> Champion
    {
        get => this._champion ?? getEachChampion();
    }

    /// <summary>
    ///     The item list from the Data Dragon API.
    /// </summary>
    public Items Items
    {
        get => this._items ?? getItems();
    }

    /// <summary>
    ///     The summoner spell list from the Data Dragon API.
    /// </summary>
    public SummonerSpells SummonerSpells
    {
        get => this._summonerSpells ?? getSummonerSpells();
    }

    /// <summary>
    ///     The rune list from the Data Dragon API.
    /// </summary>
    public Runes Runes
    {
        get => this._runes ?? getRunes();
    }

    /// <summary>
    ///     The profile picture list from the Data Dragon API.
    /// </summary>
    public ProfileIcons ProfilePictures
    {
        get => this._profilePictures ?? getProfilePictures();
    }

    #endregion

    #region URLs

    /// <summary>
    ///     The URL to get the current version of the game data given the user's
    ///     region.
    /// </summary>
    // ReSharper disable once MemberCanBeMadeStatic.Local
#pragma warning disable CA1822
    private string RegionVersionURL
    {
        get => $"https://ddragon.leagueoflegends.com/realms/{regionString}.json";
    }
#pragma warning restore CA1822

    /// <summary>
    ///     The URL to get the current champion list data.
    /// </summary>
    private string ChampionsDataURL
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this.Version}/data/{locale}/champion.json";
    }

    /// <summary>
    ///     The URL to get a specific champion's data.
    /// </summary>
    private string ChampionDataURL
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this.Version}/data/{locale}/champion/{{0}}.json";
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
    ///     The URL to get the current summoner spell list data.
    /// </summary>
    private string SummonerSpellDataURL
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this.Version}/data/{locale}/summoner.json";
    }

    /// <summary>
    ///     The URL to get the current rune list data.
    /// </summary>
    private string RuneDataURL
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this.Version}/data/{locale}/runesReforged.json";
    }

    /// <summary>
    ///     The URL to get profile picture list data.
    /// </summary>
    private string ProfilePictureDataURL
    {
        get =>
            "http://ddragon.leagueoflegends.com/cdn/"
            + $"{this.Version}/data/{locale}/profileicon.json";
    }

    /// <summary>
    ///     The URL to get ranked emblems.
    /// </summary>
    // ReSharper disable once MemberCanBeMadeStatic.Local
#pragma warning disable CA1822
    private string RankedEmblemsURL
    {
        get =>
            "https://static.developer.riotgames.com/docs/lol/"
            + "ranked-emblems-latest.zip";
    }
#pragma warning restore CA1822

    #endregion
}
