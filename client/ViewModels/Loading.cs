// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using client.Models.Data;
using ReactiveUI;

namespace client.ViewModels;

public class Loading : ReactiveObject, IScreen, IRoutableViewModel
{
    public Loading(IScreen? screen = null)
    {
        this.HostScreen = screen;
        Program.Router = this.Router;

        // Load the settings from disk
        Program.Settings.load();

        // Check if the user is logged in
        if (Program.Settings.activeAccount == null)
            this.Router.Navigate.Execute(new Login(this));

        // Create all the necessary files and directories
        if (!Setup.allContentExists())
            Setup.createAllContent();
    }

    public string? UrlPathSegment
    {
        get => "Loading";
    }

    public IScreen? HostScreen { get; }

    public RoutingState Router { get; } = new RoutingState();
}
