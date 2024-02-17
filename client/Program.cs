using Avalonia;
using Avalonia.ReactiveUI;
using Camille.RiotGames;
using client.Models.Settings;
using Projektanker.Icons.Avalonia;
using Projektanker.Icons.Avalonia.FontAwesome;

namespace client;

internal static class Program
{
    /// <summary>
    /// Global settings for the application.
    /// </summary>
    public static Settings Settings { get; } = new Settings();

    /// <summary>
    /// The settings manager for the application, which saves updated settings to disk.
    /// </summary>
#pragma warning disable CS0169 // Field is never used
    // ReSharper disable once NotAccessedField.Local, InconsistentNaming
    private static SettingsManager _settingsManager_DoNotUse;
#pragma warning restore CS0169 // Field is never used

    static Program()
    {
        _settingsManager_DoNotUse = new SettingsManager();
    }

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
        BuildAvaloniaApp().StartWithClassicDesktopLifetime(args);

    // Avalonia configuration, don't remove; also used by visual designer.
    public static AppBuilder BuildAvaloniaApp()
    {
        IconProvider.Current.Register<FontAwesomeIconProvider>();

        return AppBuilder.Configure<App>().UsePlatformDetect().LogToTrace().UseReactiveUI();
    }
}
