// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Markup.Xaml;
using client.Models;
using client.ViewModels;
using client.Views;

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
    }
}
