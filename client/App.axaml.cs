// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Markup.Xaml;
using client.Models;
using client.ViewModels;
using client.Views;

#endregion

namespace client;

public class App : Application
{
    public override void Initialize()
    {
        AvaloniaXamlLoader.Load(this);
    }

    public override void OnFrameworkInitializationCompleted()
    {
        if (this.ApplicationLifetime is IClassicDesktopStyleApplicationLifetime
            desktop)
        {
            desktop.MainWindow = new LaunchView()
            {
                DataContext = new Launch(),
            };
            desktop.Exit += OnExit;
        }

        base.OnFrameworkInitializationCompleted();
    }

    private void OnExit(object sender, ControlledApplicationLifetimeExitEventArgs e)
    {
        // TODO: Save settings like window size here

        Program.log(
                source: nameof(App),
                method: "OnExit()",
                doing: "Exiting",
                message: "Exiting the application...",
                debugSymbols:
                [
                    "Exit Code: " + e.ApplicationExitCode,
                ],
                logLevel: LogLevel.info,
                logLocation: LogLocation.all
            );

        // TODO: Save a most-recent-run-only verbose log separately, and only keep 1 month worth of logs
    }
}
