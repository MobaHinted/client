// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using ReactiveUI;

namespace client.ViewModels;

public class Loading : ReactiveObject, IScreen
{
    public Loading()
    {
        if (Program.Settings.activeAccount == null)
        {
            this.Router.Navigate.Execute(new Login(this));
        }
    }

    public static string Greeting
    {
        get => "Loading...";
    }

    public RoutingState Router { get; } = new RoutingState();
}
