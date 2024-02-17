using Avalonia;
using Avalonia.ReactiveUI;
using Camille.RiotGames;
using Projektanker.Icons.Avalonia;
using Projektanker.Icons.Avalonia.FontAwesome;

namespace client;

internal static class Program
{
  /// <summary>
  /// The configuration for the Riot Games API to use throughout the application.
  /// </summary>
  public readonly static RiotGamesApi riotAPI = RiotGamesApi.NewInstance(
    new RiotGamesApiConfig.Builder("")
    {
      MaxConcurrentRequests = 30,
      Retries = 3,
      ApiURL = "proxy.mobahinted.app",
    }.Build()
  );

  // Initialization code. Don't use any Avalonia, third-party APIs or any
  // SynchronizationContext-reliant code before AppMain is called: things aren't initialized
  // yet and stuff might break.
  [STAThread]
  public static void Main(string[] args) =>
    BuildAvaloniaApp()
      .StartWithClassicDesktopLifetime(args);

  // Avalonia configuration, don't remove; also used by visual designer.
  public static AppBuilder BuildAvaloniaApp()
  {
    IconProvider.Current.Register<FontAwesomeIconProvider>();

    return AppBuilder.Configure<App>()
      .UsePlatformDetect()
      .LogToTrace()
      .UseReactiveUI();
  }
}
