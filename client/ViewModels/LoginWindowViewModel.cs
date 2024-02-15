using System.ComponentModel.DataAnnotations;
using System.Linq;
using Camille.Enums;
using Camille.RiotGames;
using Camille.RiotGames.AccountV1;
using Camille.RiotGames.ChampionMasteryV4;

namespace client.ViewModels;

public class LoginWindowViewModel : ViewModelBase
{
  /// <summary>
  /// The list of platforms available.
  /// </summary>
  public List<string> Platforms { get; set; }

  /// <summary>
  ///  The index of the default platform, North America.
  /// </summary>
  public int DefaultPlatformIndex { get; set; }

  /// <summary>
  /// Construct initial data needed for the login window.
  /// </summary>
  public LoginWindowViewModel()
  {
    // Fill the Platforms list with the names of the platforms.
    this.Platforms = getPlatformRoutes();
    // We list platforms instead of continents/"regions", despite the latter being what is used to
    // look up accounts, because we can extrapolate the continent from the platform, and the
    // platform is used for the majority of calls

    // Find the index of the default platform: NA.
    this.DefaultPlatformIndex = this.Platforms.FindIndex(platform => platform == "North America");
  }

  /// <summary>
  /// Build a list of all available platforms, except PBE.
  /// </summary>
  /// <returns>The proper name of each platform - what users and the API identify as regions</returns>
  private static List<string> getPlatformRoutes()
  {
    return Enum.GetValues<PlatformRoute>()
      .Where(value => value != PlatformRoute.PBE1)
      .Select(
        value =>
        {
          string? description = value.GetType()
            .GetField(value.ToString())!.GetCustomAttributes(
              typeof(DisplayAttribute),
              false
            )
            .Cast<DisplayAttribute>()
            .FirstOrDefault()
            ?.Description;

          if (description != null && description.EndsWith('.'))
          {
            description = description.Substring(
              0,
              description.Length - 1
            );
          }

          return description;
        }
      )
      .ToList()!;
  }

  public string test_api()
  {
    string resultString = "\n";

    try
    {
      Console.WriteLine("Testing wrapper...");
      Console.WriteLine("Building wrapper...");

      var riotApi = RiotGamesApi.NewInstance(
        new RiotGamesApiConfig.Builder("")
        {
          MaxConcurrentRequests = 30,
          Retries = 3,
          ApiURL = "proxy.mobahinted.app",
        }.Build()
      );

      Console.WriteLine("Wrapper built.");

      Console.WriteLine("Testing wrapper calls...");

      var accounts = new[]
      {
        riotApi.AccountV1()
          .GetByRiotId(
            RegionalRoute.AMERICAS,
            "zbee",
            "7777"
          ),
        riotApi.AccountV1()
          .GetByRiotId(
            RegionalRoute.AMERICAS,
            "peace",
            "chill"
          ),
        riotApi.AccountV1()
          .GetByRiotId(
            RegionalRoute.AMERICAS,
            "weeb o clock",
            "anime"
          ),
        riotApi.AccountV1()
          .GetByRiotId(
            RegionalRoute.AMERICAS,
            "cdog44",
            "na1"
          ),
      };

      foreach (Account? account in accounts)
      {
        if (account == null)
        {
          Console.WriteLine("Account not found:\n" + account);
          continue;
        }

        resultString += $"{account.GameName}'s Top Champs:\n";

        var mastery = riotApi.ChampionMasteryV4()
          .GetAllChampionMasteriesByPUUID(
            PlatformRoute.NA1,
            account.Puuid
          );

        for (int i = 0; i < 3; i++)
        {
          ChampionMastery championMastery = mastery[i];
          // Get champion for this mastery.
          var champ = (Champion) championMastery.ChampionId;
          // print i, champ id, champ mastery points, and champ level
          resultString
            += $"{i + 1}) {champ.ToString()} {championMastery.ChampionPoints:N0} ({championMastery.ChampionLevel})\n";
        }

        Console.WriteLine();
      }

      Console.WriteLine("Wrapper calls successful.");
    }
    catch (Exception e)
    {
      Console.WriteLine("Caught an error:");
      Console.WriteLine(e.Message);
    }

    return resultString;
  }
}
