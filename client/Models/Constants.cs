namespace client.Models;

public static class Constants
{
  private readonly static string _appdata = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
  public readonly static string Mobahinted = _appdata + "\\mobahinted\\";
  public readonly static string Assets = Mobahinted + "assets\\";
  public readonly static string Data = Mobahinted + "data\\";
  public readonly static string Image_Cache = Data + "image_cache\\";
  public readonly static string Ranked_Emblems = Assets + "ranked_emblems\\";
  public readonly static string Champion_Data = Data + "champion_roles.dat";
  public readonly static string Avalonia = Assets + "avalonia.ini";
  public readonly static string Settings = Assets + "settings.dat";
  public readonly static string Users = Data + "users.dat";
  public readonly static string Friends = Data + "friends.dat";
}
