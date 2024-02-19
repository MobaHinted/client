// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using ReactiveUI;

namespace client.ViewModels;

public class MatchHistory : ReactiveObject, IRoutableViewModel
{
    public MatchHistory(IScreen? screen = null)
    {
        Console.WriteLine("???");

        // Save the previous screen
        this.HostScreen = screen!;

        // Resize the window
        Program.Window!.MaxWidth = 100000;
        Program.Window.MaxHeight = 100000;
        Program.Window.MinWidth = Program.Settings.windowWidth;
        Program.Window.MinHeight = Program.Settings.windowHeight;
        Program.Window.Width = Program.Settings.windowWidth;
        Program.Window.Height = Program.Settings.windowHeight;
    }

    public string? UrlPathSegment
    {
        get => "MatchHistory";
    }

    public IScreen HostScreen { get; }
}
