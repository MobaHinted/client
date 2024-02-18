namespace client.Models;

public static class Constants
{
    private static readonly string appdata =
        Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData) + "\\";

    public static readonly string mobahinted = appdata + "mobahinted\\";
    public static readonly string assets = mobahinted + "assets\\";
    public static readonly string data = mobahinted + "data\\";

    public static readonly string imageCacheFolder = data + "image_cache\\";
    public static readonly string usersFile = data + "users.json";
    public static readonly string friendsFile = data + "friends.json";
    public static readonly string championRolesDataFile = data + "champion_roles.json";

    public static readonly string rankedEmblemsFolder = assets + "ranked_emblems\\";
    public static readonly string avaloniaConfigFile = assets + "avalonia.json";
    public static readonly string settingsFile = assets + "settings.json";
}
