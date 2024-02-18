// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using ReactiveUI;

namespace client.ViewModels;

public class Loading : ReactiveObject, IRoutableViewModel
{
    public Loading(IScreen? screen = null)
    {
        this.HostScreen = screen;

        Console.WriteLine("Loading the application...");
    }

    public string? UrlPathSegment
    {
        get => "Loading";
    }

    public IScreen? HostScreen { get; }
}
