using Camille.Enums;
using Camille.RiotGames;
using Camille.RiotGames.AccountV1;
using Camille.RiotGames.ChampionMasteryV4;
using ImGuiNET;
using Veldrid;
using Veldrid.Sdl2;
using Veldrid.StartupUtilities;

namespace MobaHinted
{
  internal class Client
  {
    static void Main(string[] args)
    {
      test_calls();
      test_ui();
    }

    public static bool Show = true;
    private static Sdl2Window _window;
    private static GraphicsDevice _gd;
    private static CommandList _cl;

    private static void test_ui()
    {
      // Create window, GraphicsDevice, and all resources necessary for the demo.
      VeldridStartup.CreateWindowAndGraphicsDevice(
        new WindowCreateInfo(
          50,
          50,
          1780,
          670,
          WindowState.Normal,
          "MobaHinted"
        ),
        out _window,
        out _gd
      );

      ImGuiRenderer imGuiRenderer = new ImGuiRenderer(
        _gd,
        _gd.SwapchainFramebuffer.OutputDescription,
        _window.Width,
        _window.Height
      );

      _cl = _gd.ResourceFactory.CreateCommandList();

      while (_window.Exists)
      {
        var input = _window.PumpEvents();
        if (!_window.Exists) { break; }
        imGuiRenderer.Update(1f / 60f, input); // Compute actual value for deltaSeconds.

        // Draw stuff
        ImGui.Text("Hello World");

        _cl.Begin();
        _cl.SetFramebuffer(_gd.MainSwapchain.Framebuffer);
        _cl.ClearColorTarget(0, RgbaFloat.Black);
        imGuiRenderer.Render(_gd, _cl);
        _cl.End();
        _gd.SubmitCommands(_cl);
        _gd.SwapBuffers(_gd.MainSwapchain);
      }
    }

    private static void test_calls()
    {
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

        var accounts = new[]
        {
          riotApi.AccountV1().GetByRiotId(
            RegionalRoute.AMERICAS,
            "zbee",
            "7777"
          ),
          riotApi.AccountV1().GetByRiotId(
            RegionalRoute.AMERICAS,
            "peace",
            "chill"
          ),
          riotApi.AccountV1().GetByRiotId(
            RegionalRoute.AMERICAS,
            "weeb o clock",
            "anime"
          ),
          riotApi.AccountV1().GetByRiotId(
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

          Console.WriteLine($"{account.GameName}'s Top Champs:");

          var mastery = riotApi.ChampionMasteryV4().GetAllChampionMasteriesByPUUID(
            PlatformRoute.NA1,
            account.Puuid
          );

          for (int i = 0; i < 3; i++)
          {
            ChampionMastery championMastery = mastery[i];
            // Get champion for this mastery.
            var champ = (Champion) championMastery.ChampionId;
            // print i, champ id, champ mastery points, and champ level
            Console.WriteLine(
              "{0,3}) {1,-16} {2,10:N0} ({3})",
              i + 1,
              champ.ToString(),
              championMastery.ChampionPoints,
              championMastery.ChampionLevel
            );
          }

          Console.WriteLine();
        }

        Console.WriteLine("Wrapper calls successful.");

        Console.ReadLine();
      }
      catch (Exception e)
      {
        Console.WriteLine("Caught an error:");
        Console.WriteLine(e.Message);
      }
    }
  }
}
