// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using ReactiveUI;

namespace client.ViewModels;

public class Loading : ReactiveObject, IRoutableViewModel
{
    /// <summary>
    ///     What the loading screen is currently doing.
    /// </summary>
    private string _status;
    /// <summary>
    ///     What the loading screen is currently doing, more specifically.
    /// </summary>
    private string _subStatus;

    public Loading(IScreen? screen = null)
    {
        Console.WriteLine("Loading the application...");

        // Save the previous screen
        this.HostScreen = screen;

        Program.Assets.checkForUpdates(
                (status, subStatus) =>
                {
                    this.RaiseAndSetIfChanged(
                            ref this._status!,
                            status,
                            nameof(this.Status)
                        );

                    this.RaiseAndSetIfChanged(
                            ref this._subStatus!,
                            subStatus,
                            nameof(this.SubStatus)
                        );
                }
            );
    }

    /// <summary>
    ///     What the loading screen is currently doing.
    /// </summary>
    public string Status
    {
        get => this._status;
        set =>
            this.RaiseAndSetIfChanged(
                    ref this._status,
                    value
                );
    }

    /// <summary>
    ///     What the loading screen is currently doing, more specifically.
    /// </summary>
    public string SubStatus
    {
        get => this._subStatus;
        set =>
            this.RaiseAndSetIfChanged(
                    ref this._subStatus,
                    value
                );
    }

    public string? UrlPathSegment
    {
        get => "Loading";
    }

    public IScreen? HostScreen { get; }
}
