﻿// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

namespace client.Models;

public static class Constants
{
    private readonly static string appdata =
        Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData) + "\\";
    public readonly static string mobahinted = appdata + "mobahinted\\";

    public readonly static string assets = mobahinted + "assets\\";
    public readonly static string data = mobahinted + "data\\";

    public readonly static string imageCacheFolder = data + "image_cache\\";
    public readonly static string usersFile = data + "users.json";
    public readonly static string friendsFile = data + "friends.json";
    public readonly static string championRolesDataFile =
        data + "champion_roles.json";

    public readonly static string rankedEmblemsFolder = assets + "ranked_emblems\\";
    public readonly static string avaloniaConfigFile = assets + "avalonia.json";
    public readonly static string settingsFile = assets + "settings.json";
}
