// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

namespace client.Models;

public static class Constants
{
    #region Initial Paths

    private readonly static string appdata =
        Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData) + "\\";
    public readonly static string mobahinted = appdata + "mobahinted\\";


    public readonly static string assets = mobahinted + "assets\\";
    public readonly static string data = mobahinted + "data\\";
    public readonly static string logs = mobahinted + "logs\\";

    #endregion

    #region Initial Files

    public readonly static string avaloniaConfigFile = mobahinted + "avalonia.json";
    public readonly static string settingsFile = mobahinted + "settings.json";

    #endregion

    #region Data Paths

    public readonly static string cachedMatchesFolder = data + "cachedMatches\\";
    public readonly static string dataDragonFolder = data + "data_dragon\\";
    public readonly static string dataDragonChampionFolder =
        dataDragonFolder + "champions\\";

    #endregion

    #region Data Files

    public readonly static string usersFile = data + "users.json";
    public readonly static string friendsFile = data + "friends.json";
    public readonly static string championRolesDataFile =
        data + "champion_roles.json";

    #endregion

    #region Assets Paths

    public readonly static string imageCacheFolder = assets + "image_cache\\";
    public readonly static string imageCacheDataDragonFolder =
        imageCacheFolder + "data_dragon\\";

    #endregion

    #region Log Files

    public readonly static string fullLogFile = logs + "verbose.log";
    public readonly static string warningsPlusLogFile = logs + "errors.log";

    public readonly static string mainLogFile = logs + "main.log";
    public readonly static string downloadLogFile = logs + "download.log";
    public readonly static string gameFlowLogFile = logs + "game.log";
    public readonly static string automationLogFile = logs + "automation.log";
    public readonly static string overlayLogFile = logs + "overlay.log";

    #endregion
}
