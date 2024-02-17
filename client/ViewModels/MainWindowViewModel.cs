namespace client.ViewModels;

using Camille.Enums;
using Camille.RiotGames;
using Camille.RiotGames.AccountV1;
using Camille.RiotGames.ChampionMasteryV4;

public class MainWindowViewModel : ViewModelBase
{
  public string Greeting => "Welcome to Avalonia!" + this.test_api();

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
