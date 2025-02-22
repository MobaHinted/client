// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using client.Models.Data.DataDragon;
using Champion = client.Models.Data.DataDragon.Champion;

#endregion

namespace client.Models.Data;

public class ProgramAssets
{
    /// <summary>
    ///     Run the download of all current game data, and some images.
    /// </summary>
    /// <param name="updateStatus">The action to update the status text</param>
    private async Task Setup(Action<string, string> updateStatus)
    {
        updateStatus(
                "Downloading...",
                "Version data"
            );
        GetVersion();
        GetVersions();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Champion data"
            );
        GetChampions();
        GetEachChampion();
        await Task.Delay(200);

        // Wait until is champion is downloaded
        while (this._champions!.data.Values.Count != this._champion!.Count)
        {
            await Task.Delay(100);
        }

        updateStatus(
                "Downloading...",
                "Champion images"
            );
        GetChampionImages();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Item data"
            );
        GetItems();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Item images"
            );
        GetItemImages();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Runes data"
            );
        GetRunes();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Runes images"
            );
        GetRuneImages();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Summoner Spell data"
            );
        GetSummonerSpells();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Summoner Spell images"
            );
        GetSummonerSpellImages();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Rank images"
            );
        GetRankImages();
        await Task.Delay(200);

        updateStatus(
                "Downloading...",
                "Profile Picture data"
            );
        GetProfilePictures();
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
    /// <seealso cref="Setup" />
    public async Task CheckForUpdates(Action<string, string> updateStatus)
    {
        updateStatus(
                "Checking for updates...",
                ""
            );

        bool haveFiles = NoMissingFiles();
        bool versionUp = VersionUpToDate();

        Program.Log(
                source: nameof(ProgramAssets),
                method: "checkForUpdates()",
                message: "Checking if update is necessary...",
                debugSymbols:
                [
                    $"files all available: {haveFiles}",
                    $"version up to date: {versionUp}",
                    $"update necessary: {!haveFiles || !versionUp}",
                ],
                logLevel: LogLevel.info,
                logLocation: LogLocation.verbose
            );

        // Check if all files are accessible and the version is up-to-date
        if (haveFiles && versionUp)
        {
            Program.Log(
                    source: nameof(ProgramAssets),
                    method: "checkForUpdates()",
                    message: $"Already on {this.Version}",
                    logLevel: LogLevel.info,
                    logLocation: LogLocation.main
                );
            await Task.Delay(600);
            return;
        }

        // Re-download the data dragon files if not up to date
        Program.Log(
                source: nameof(ProgramAssets),
                method: "checkForUpdates()",
                message: $"Updating to {this.Version}...",
                logLevel: LogLevel.info,
                logLocation: LogLocation.download | LogLocation.main
            );
        FileManagement.EmptyDirectory(Constants.dataDragonFolder);
        FileManagement.CreateDirectory(Constants.dataDragonChampionFolder);
        FileManagement.EmptyDirectory(Constants.imageCacheFolder);
        FileManagement.CreateDirectory(Constants.imageCacheDataDragonFolder);
        FileManagement.CreateDirectory(Constants.imageCacheProfileIconFolder);
        FileManagement.EmptyDirectory(Constants.imageCacheDataDragonFolder);

        // Try to update the files
        try
        {
            this._dataDragonURLs = new DataDragonURLs(
                    this.Version,
                    this._locale
                );
            await Setup(updateStatus);
        }
        catch (HttpRequestException e)
        {
            // TODO: this should log to an LogTo.retryPopup, so that needs set up
            Program.Log(
                    source: nameof(ProgramAssets),
                    method: "checkForUpdates()",
                    message: "Error updating, timeout encountered",
                    debugSymbols: [e.Message],
                    logLevel: LogLevel.error,
                    logLocation: LogLocation.download
                );
            // TODO: This should not be here once a retry screen is added
            throw new Exception();
        }
        catch (ArgumentException e)
        {
            // TODO: this should log to an LogTo.errorScreen, so that needs set up
            Program.Log(
                    source: nameof(ProgramAssets),
                    method: "checkForUpdates()",
                    message: "Error updating\n" + e.Message,
                    logLevel: LogLevel.fatal,
                    logLocation: LogLocation.download
                );
            // TODO: This should be program.exit(), that needs to be setup
            throw new Exception();
        }

        // Succeed
        Program.Log(
                source: nameof(ProgramAssets),
                method: "checkForUpdates()",
                message: "Updated",
                logLevel: LogLevel.info,
                logLocation: LogLocation.download | LogLocation.main
            );
    }

    /// <summary>
    ///     Check if the game data is missing from the user's computer.
    /// </summary>
    /// <returns>If all downloaded files are present</returns>
    private static bool NoMissingFiles()
    {
        return FileManagement.FileHasContent(
                    Constants.dataDragonFolder + "champions.json"
                )
            && FileManagement.FileHasContent(
                    Constants.dataDragonChampionFolder + "Aatrox.json"
                )
            && FileManagement.FileHasContent(
                    Constants.dataDragonFolder + "versions.json"
                )
            && FileManagement.FileHasContent(
                    Constants.dataDragonFolder + "items.json"
                )
            && FileManagement.FileHasContent(
                    Constants.dataDragonFolder + "summonerSpells.json"
                )
            && FileManagement.FileHasContent(
                    Constants.dataDragonFolder + "runes.json"
                )
            && FileManagement.FileHasContent(
                    Constants.dataDragonFolder + "profilePictures.json"
                )
            && FileManagement.FileHasContent(
                    Constants.imageCacheDataDragonFolder + "spell.Flash.png"
                )
            && FileManagement.FileHasContent(
                    Constants.imageCacheDataDragonFolder + "rank.Emerald.png"
                )
            && FileManagement.FileHasContent(
                    Constants.imageCacheFolder + "item.1001.png"
                );
    }

    /// <summary>
    ///     Check if the latest version data is out of date.
    /// </summary>
    /// <returns>
    ///     If the latest downloaded version matches the latest game version
    /// </returns>
    private bool VersionUpToDate()
    {
        // If the versions file does exist, check it
        FileManagement.LoadFromFile(
                Constants.dataDragonFolder + "versions.json",
                out Versions? versions
            );

        // Bail if no versions were loaded
        if (versions is null)
            return false;

        // If the latest version is the same as the current version
        return versions.latestVersion == this.Version;
    }

    // TODO: Move all of these methods to DataDragon.Calls.getAs where it checks the type or something

    /// <summary>
    ///     Get the current version of the game data for the user's region from the
    ///     Data Dragon API.
    /// </summary>
    /// <returns>A League Version</returns>
    private string GetVersion()
    {
        var response =
            DataDragonCall.GetAs<RegionVersion>(DataDragonURLs.RegionVersionURL);
        string version = response.Version;

        this._version = version;
        return version;
    }

    /// <summary>
    ///     Get the versions list from the Data Dragon API.
    /// </summary>
    /// <returns>A list of League Versions</returns>
    private Versions GetVersions()
    {
        Versions versions;
        string file = Constants.dataDragonFolder + "versions.json";

        // Load the versions list if it exists
        if (FileManagement.FileHasContent(file))
        {
            FileManagement.LoadFromFile(
                    file,
                    out versions!
                );
        }
        // Download and save the versions list
        else
        {
            versions = DataDragonCall.GetAs<Versions>(DataDragonURLs.VERSIONS_URL);

            FileManagement.SaveToFile(
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
    private Champions GetChampions()
    {
        Champions champions;
        string file = Constants.dataDragonFolder + "champions.json";

        // Load the versions list if it exists
        if (FileManagement.FileHasContent(file))
        {
            FileManagement.LoadFromFile(
                    file,
                    out champions!
                );
        }
        // Download and save the versions list
        else
        {
            champions = DataDragonCall.GetAs<Champions>(
                        this._dataDragonURLs.ChampionsDataURL
                    );

            FileManagement.SaveToFile(
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
    private List<IndividualChampion> GetEachChampion()
    {
        List<IndividualChampion> champions = [];
        string folder = Constants.dataDragonChampionFolder;

        // Iterate over each champion from the champion list
        var tasks = new List<Task>();
        foreach (string championName in this.Champions.data.Select(
                         champion => champion.Value.id
                     ))
        {
            IndividualChampion individualChampion;
            string file = folder + championName + ".json";

            // Load the individual champion if it exists
            if (FileManagement.FileHasContent(file))
            {
                FileManagement.LoadFromFile(
                        file,
                        out individualChampion!
                    );
                champions.Add(individualChampion);
            }
            // Download and save the individual champion
            else
            {
                tasks.Add(
                        Task.Run(
                                () =>
                                {
                                    individualChampion = DataDragonCall
                                        .GetAs<IndividualChampion>(
                                                string.Format(
                                                        this._dataDragonURLs
                                                            .ChampionDataURL,
                                                        championName
                                                    )
                                            );

                                    FileManagement.SaveToFile(
                                            file,
                                            individualChampion
                                        );
                                    champions.Add(individualChampion);
                                }
                            )
                    );
            }
        }

        // Wait for all champions to complete
        while (tasks.Any(t => !t.IsCompleted))
            Thread.Sleep(50);

        this._champion = champions;
        return champions;
    }

    /// <summary>
    ///     Get the images for each champion and their abilities from the Data Dragon
    ///     API.
    /// </summary>
    private void GetChampionImages()
    {
        string folder = Constants.imageCacheDataDragonFolder;

        // Iterate over each champion where the image does not already exist
        var tasks = new List<Task>();
        foreach (Champion champion in this
                     .Champion
                     .Select(individualChampion => individualChampion.Champion)
                     .Where(
                             champion => !FileManagement.FileHasContent(
                                     folder + "champion." + champion.image.full
                                 )
                         ))
        {
            // Download the champion's image if not
            tasks.Add(
                    Task.Run(
                            () => FileManagement.DownloadImage(
                                    champion.image.imageURL,
                                    folder + "champion." + champion.image.full
                                )
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
                // TODO: use some sort of templating to avoid this big block
                // TODO: use some sort of templating to keep names consistent
                // TODO: add a period after the champion name
                // TODO: add things like "champion_ability" to constants
                tasks.Add(
                        Task.Run(
                                () => FileManagement.DownloadImage(
                                        ability.image.imageURL,
                                        folder
                                        + "champion_ability."
                                        + champion.id
                                        + abilityLabels[counterForTask]
                                        + ability.image.full[
                                            ability.image.full.LastIndexOf('.')..]
                                    )
                            )
                    );
                counter++;
            }

            // Download the passive's image
            tasks.Add(
                    Task.Run(
                            () => FileManagement.DownloadImage(
                                    champion.passive.image.imageURL,
                                    folder
                                    + "champion_ability."
                                    + champion.id
                                    + "P"
                                    + champion.passive.image.full[
                                        champion.passive.image.full
                                            .LastIndexOf('.')..]
                                )
                        )
                );

            #endregion
        }

        // Wait for all images to complete
        while (tasks.Any(t => !t.IsCompleted))
            Thread.Sleep(50);
    }

    /// <summary>
    ///     Get the item list from the Data Dragon API.
    /// </summary>
    /// <returns>A list of League Items</returns>
    private Items GetItems()
    {
        Items items;
        string file = Constants.dataDragonFolder + "items.json";

        // Load the items list if it exists
        if (FileManagement.FileHasContent(file))
        {
            FileManagement.LoadFromFile(
                    file,
                    out items!
                );
        }
        // Download and save the items list
        else
        {
            items = DataDragonCall.GetAs<Items>(this._dataDragonURLs.ItemDataURL);

            FileManagement.SaveToFile(
                    file,
                    items
                );
        }

        // Make a placeholder item
        items.data.Add(
                "0",
                new ItemData
                {
                    name = "No Item",
                    description = "No Item",
                    image = new Image
                    {
                        full = "filler.png",
                        sprite = "filler.png",
                        group = "item",
                        x = 0,
                        y = 0,
                        w = 64,
                        h = 64,
                    },
                }
            );

        this._items = items;
        return items;
    }

    /// <summary>
    ///     Get the images for each item from the Data Dragon API.
    /// </summary>
    private void GetItemImages()
    {
        string folder = Constants.imageCacheFolder;

        // Iterate over each item where the image does not already exist
        var tasks = new List<Task>();
        foreach (ItemData item in this.Items.data.Values.Where(
                         item => !FileManagement.FileHasContent(
                                 folder
                                 + "item."
                                 + item.image.full[
                                     ..item.image.full.LastIndexOf('.')]
                                 + ".png"
                             )
                     ))
        {
            // Download the item's image
            tasks.Add(
                    Task.Run(
                            () => FileManagement.DownloadImage(
                                    item.image.imageURL,
                                    folder
                                    + "item."
                                    + item.image.full[
                                        ..item.image.full.LastIndexOf('.')]
                                    + ".png"
                                )
                        )
                );
        }

        // Wait for all images to complete
        while (tasks.Any(t => !t.IsCompleted))
            Thread.Sleep(50);
    }

    /// <summary>
    ///     Get the rune list from the Data Dragon API.
    /// </summary>
    /// <returns>A list of League Runes</returns>
    private Runes GetRunes()
    {
        Runes runes;
        string file = Constants.dataDragonFolder + "runes.json";

        // Load the versions list if it exists
        if (FileManagement.FileHasContent(file))
        {
            FileManagement.LoadFromFile(
                    file,
                    out runes!
                );
        }
        // Download and save the versions list
        else
        {
            runes = DataDragonCall.GetAs<Runes>(this._dataDragonURLs.RuneDataURL);

            FileManagement.SaveToFile(
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
    private void GetRuneImages()
    {
        string folder = Constants.imageCacheDataDragonFolder;

        // Iterate over each rune where the image does not already exist
        var tasks = new List<Task>();
        foreach (RuneTree runeTree in this.Runes.runetrees.Where(
                         rune => !FileManagement.FileHasContent(
                                 folder + "rune_tree." + rune.image.sprite
                             )
                     ))
        {
            // Download the tree's image
            tasks.Add(
                    Task.Run(
                            () => FileManagement.DownloadImage(
                                    runeTree.image.imageURL,
                                    folder
                                    + "rune_tree."
                                    + runeTree.image.sprite
                                    + runeTree.image.full[
                                        runeTree.image.full.LastIndexOf('.')..],
                                    32
                                )
                        )
                );

            // Iterate over each rune in the tree
            foreach (Rune rune in runeTree.slots.SelectMany(slot => slot.runes))
            {
                // Download the rune's image
                tasks.Add(
                        Task.Run(
                                () => FileManagement.DownloadImage(
                                        rune.image.imageURL,
                                        folder
                                        + "rune."
                                        + rune.image.sprite
                                        + rune.image.full[
                                            rune.image.full.LastIndexOf('.')..],
                                        32
                                    )
                            )
                    );
            }
        }

        // Wait for all images to complete
        while (tasks.Any(t => !t.IsCompleted))
            Thread.Sleep(50);
    }

    /// <summary>
    ///     Get the summoner spell list from the Data Dragon API.
    /// </summary>
    /// <returns>A list of League Summoner Spells</returns>
    private SummonerSpells GetSummonerSpells()
    {
        SummonerSpells summonerSpells;
        string file = Constants.dataDragonFolder + "summonerSpells.json";

        // Load the versions list if it exists
        if (FileManagement.FileHasContent(file))
        {
            FileManagement.LoadFromFile(
                    file,
                    out summonerSpells!
                );
        }
        // Download and save the versions list
        else
        {
            summonerSpells = DataDragonCall.GetAs<SummonerSpells>(
                        this._dataDragonURLs.SummonerSpellDataURL
                    );

            FileManagement.SaveToFile(
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
    private void GetSummonerSpellImages()
    {
        string folder = Constants.imageCacheDataDragonFolder;

        // Iterate over each summoner spell where the image does not already exist
        var tasks = new List<Task>();
        foreach (SummonerSpell summonerSpell in
                 this.SummonerSpells.data.Values.Where(
                         spell => !FileManagement.FileHasContent(
                                 folder
                                 + "spell."
                                 + spell.name
                                 + spell.image.full[
                                     spell.image.full.LastIndexOf('.')..]
                             )
                     ))
        {
            // Download the spell's image
            tasks.Add(
                    Task.Run(
                            () => FileManagement.DownloadImage(
                                    summonerSpell.image.imageURL,
                                    folder
                                    + "spell."
                                    + summonerSpell.name
                                    + summonerSpell.image.full[
                                        summonerSpell.image.full.LastIndexOf('.')..]
                                )
                        )
                );
        }

        // Wait for all images to complete
        while (tasks.Any(t => !t.IsCompleted))
            Thread.Sleep(50);
    }

    /// <summary>
    ///     Get the profile picture list from the Data Dragon API.
    /// </summary>
    /// <returns>A list of League Profile Pictures</returns>
    private ProfileIcons GetProfilePictures()
    {
        ProfileIcons profilePictures;
        string file = Constants.dataDragonFolder + "profilePictures.json";

        // Load the versions list if it exists
        if (FileManagement.FileHasContent(file))
        {
            FileManagement.LoadFromFile(
                    file,
                    out profilePictures!
                );
        }
        // Download and save the versions list
        else
        {
            profilePictures = DataDragonCall.GetAs<ProfileIcons>(
                        this._dataDragonURLs.ProfilePictureDataURL
                    );

            FileManagement.SaveToFile(
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
    private void GetRankImages()
    {
        string folder = Constants.imageCacheDataDragonFolder;

        Program.Log(
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
                logLevel: LogLevel.debug,
                logLocation: LogLocation.download
            );

        // Skip downloading if the images already exist
        if (FileManagement.FileHasContent(folder + "rank.Emerald.png"))
            return;

        // Download the ranked emblems and unpack them
        FileManagement.DownloadFile(
                this.RankedEmblemsURL,
                folder + "ranked_emblems.zip"
            );
        FileManagement.UnpackFile(
                folder + "ranked_emblems.zip",
                folder
            );

        // Delete the zip file
        FileManagement.DeleteFile(folder + "ranked_emblems.zip");

        // Go into the folder
        string tempFolder = folder + "Ranked Emblems Latest\\";

        // Delete the folders we don't need
        FileManagement.DeleteDirectory(tempFolder + "Wings\\");
        FileManagement.DeleteDirectory(tempFolder + "Tier Wings\\");

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
            FileManagement.ResizeImage(
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
        FileManagement.DeleteDirectory(tempFolder);
    }

    #region URLs

    /// <summary>
    ///     The URLs for the Data Dragon API.
    /// </summary>
    private DataDragonURLs _dataDragonURLs = null!;

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

    #region Variables and their Backers

    /// <summary>
    ///     The locale used for the game data downloads.
    /// </summary>
    /// <!--TODO: This should be an option on Login and in settings once app is
    ///     localized.-->
    // ReSharper disable once ConvertToConstant.Local
    private readonly string _locale = "en_US";

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
        get => this._version ?? GetVersion();
    }

    /// <summary>
    ///     The versions list from the Data Dragon API.
    /// </summary>
    public Versions Versions
    {
        get => this._versions ?? GetVersions();
    }

    /// <summary>
    ///     The champion list from the Data Dragon API.
    /// </summary>
    public Champions Champions
    {
        get => this._champions ?? GetChampions();
    }

    /// <summary>
    ///     Each champion from the Data Dragon API.
    /// </summary>
    public IEnumerable<IndividualChampion> Champion
    {
        get => this._champion ?? GetEachChampion();
    }

    /// <summary>
    ///     The item list from the Data Dragon API.
    /// </summary>
    public Items Items
    {
        get => this._items ?? GetItems();
    }

    /// <summary>
    ///     The summoner spell list from the Data Dragon API.
    /// </summary>
    public SummonerSpells SummonerSpells
    {
        get => this._summonerSpells ?? GetSummonerSpells();
    }

    /// <summary>
    ///     The rune list from the Data Dragon API.
    /// </summary>
    public Runes Runes
    {
        get => this._runes ?? GetRunes();
    }

    /// <summary>
    ///     The profile picture list from the Data Dragon API.
    /// </summary>
    public ProfileIcons ProfilePictures
    {
        get => this._profilePictures ?? GetProfilePictures();
    }

    #endregion
}
