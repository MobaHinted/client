// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using client.Models.Data;
using ReactiveUI;

namespace client.ViewModels;

public class Launch : ReactiveObject, IScreen
{
    public Launch()
    {
        Console.WriteLine("Launching the application...");

        // Set the program router to this instance
        Program.Router = this.Router;

        // Load the settings from disk
        Program.Settings.load();

        // Check if the user is logged in
        if (Program.Settings.activeAccount == null)
        {
            this.Router.Navigate.Execute(new Login(this));
            return;
        }

        // Create all the necessary files and directories
        if (!Setup.allContentExists())
            Setup.createAllContent();

        // If all checks pass, navigate to the loading screen
        this.Router.Navigate.Execute(new Loading(this));
    }

    public RoutingState Router { get; } = new RoutingState();
}
