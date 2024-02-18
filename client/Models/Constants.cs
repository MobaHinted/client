namespace client.Models;

public static class Constants
{
    private static readonly string _appdata = Environment.GetFolderPath(
        Environment.SpecialFolder.ApplicationData
    );
    public static readonly string Mobahinted = _appdata + "\\mobahinted\\";
    public static readonly string Assets = Mobahinted + "assets\\";
    public static readonly string Data = Mobahinted + "data\\";
    public static readonly string Image_Cache = Data + "image_cache\\";
    public static readonly string Ranked_Emblems = Assets + "ranked_emblems\\";
    public static readonly string Champion_Data = Data + "champion_roles.dat";
    public static readonly string Avalonia = Assets + "avalonia.ini";
    public static readonly string Settings = Assets + "settings.dat";
    public static readonly string Users = Data + "users.dat";
    public static readonly string Friends = Data + "friends.dat";
}
