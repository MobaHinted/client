﻿// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using client.Models;
using client.Models.Data;
using ReactiveUI;

namespace client.ViewModels;

public class Launch : ReactiveObject, IScreen
{
    public Launch()
    {
        Program.log(
                source: nameof(Launch),
                method: "ctor()",
                doing: "Loading",
                message: "Launch View",
                logLevel: LogLevel.info
            );

        // Set the program router to this instance
        Program.Router = this.Router;

        // Load the settings from disk
        Program.Settings.load();

        // Create all the necessary files and directories
        if (!Setup.allContentExists())
            Setup.createAllContent();

        // Check if the user is logged in
        if (Program.Settings.activeAccount == null)
        {
            this.Router.Navigate.Execute(new Login(this));
            return;
        }

        // If all checks pass, navigate to the loading screen
        this.Router.Navigate.Execute(new Loading(this));
    }

    public RoutingState Router { get; } = new RoutingState();
}
