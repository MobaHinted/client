using Camille.Enums;
using Camille.RiotGames;
using Camille.RiotGames.Util;

try
{
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

  var summoners = new[]
  {
    riotApi.SummonerV4().GetBySummonerName(PlatformRoute.NA1, "jAnna kendrick"),
    riotApi.SummonerV4().GetBySummonerName(PlatformRoute.NA1, "lug nuts k")
  };

  foreach (var summoner in summoners)
  {
    Console.WriteLine($"{summoner.Name}'s Top 10 Champs:");

    var masteries =
      riotApi.ChampionMasteryV4().GetAllChampionMasteriesByPUUID(PlatformRoute.NA1, summoner.Puuid);

    for (var i = 0; i < 10; i++)
    {
      var mastery = masteries[i];
      // Get champion for this mastery.
      var champ = (Champion) mastery.ChampionId;
      // print i, champ id, champ mastery points, and champ level
      Console.WriteLine("{0,3}) {1,-16} {2,10:N0} ({3})", i + 1, champ.ToString(),
        mastery.ChampionPoints, mastery.ChampionLevel);
    }
    Console.WriteLine();
  }

  Console.WriteLine("Wrapper calls successful.");
}
catch (Exception e)
{
  Console.WriteLine("Caught an error");
  Console.WriteLine(e.Message);
}
