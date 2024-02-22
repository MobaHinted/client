// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using client.Models;
using ReactiveUI;

namespace client.ViewModels;

public class Loading : ReactiveObject, IRoutableViewModel
{
    /// <summary>
    ///     What the loading screen is currently doing.
    /// </summary>
    private string _status = string.Empty;

    /// <summary>
    ///     What the loading screen is currently doing, more specifically.
    /// </summary>
    private string _subStatus = string.Empty;

    public Loading(IScreen? screen = null)
    {
        Program.log(
                source: nameof(Loading),
                method: "ctor()",
                doing: "Loading",
                message: "Loading View",
                logLevel: LogLevel.info
            );

        // Save the previous screen
        this.HostScreen = screen!;

        // Check for updates to static data
        loadData();
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

    public IScreen HostScreen { get; }

    private async void loadData()
    {
        await Task.Run(
                () => Program.Assets.checkForUpdates(
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
                    )
            );

        // Load into Match History
        loadIn();
    }

    private void loadIn()
    {
        // Clear the status
        this.Status = string.Empty;
        this.SubStatus = string.Empty;

        // Navigate to the Match History screen
        Program.Router.Navigate.Execute(new MatchHistory(this.HostScreen));
    }
}
