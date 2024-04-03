// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using client.Models;
using client.Models.Data.Matches;
using client.Views;
using client.Views.MatchHistory;
using ReactiveUI;

namespace client.ViewModels;

public class MatchHistory : ReactiveObject, IRoutableViewModel
{
    /// <summary>
    ///     The match that was most recently loaded.
    /// </summary>
    /// <remarks>
    ///     Used to get the next set of matches, if there are more than the limit.
    /// </remarks>
    private int _currentProgressMatch;

    /// <summary>
    ///     The current view that is being displayed within Match History.
    /// </summary>
    /// <remarks>
    ///     First, <see cref="client.Views.MatchHistory.LoadingSubView" /> then
    ///     <see cref="client.Views.MatchHistory.HistorySubView" />
    /// </remarks>
    private IsubView _currentView = new LoadingSubView();

    public MatchHistory(IScreen? screen = null)
    {
        Program.log(
                source: nameof(MatchHistory),
                method: "ctor()",
                doing: "Loading",
                message: "Match History View",
                logLevel: LogLevel.info,
                logLocation: LogLocation.main
            );

        // Save the previous screen
        this.HostScreen = screen!;

        // Resize the window
        Program.Window!.MaxWidth = 100000;
        Program.Window.MaxHeight = 100000;
        Program.Window.MinWidth = Program.Settings.windowWidth;
        Program.Window.MinHeight = Program.Settings.windowHeight;
        Program.Window.Width = Program.Settings.windowWidth;
        Program.Window.Height = Program.Settings.windowHeight;

        // Load the matches
        loadMatches();
    }

    /// <summary>
    ///     The current view that is being displayed within Match History.
    /// </summary>
    /// <remarks>
    ///     First, <see cref="client.Views.MatchHistory.LoadingSubView" /> then
    ///     <see cref="client.Views.MatchHistory.HistorySubView" />
    /// </remarks>
    public IsubView CurrentView
    {
        get => this._currentView;
        set =>
            this.RaiseAndSetIfChanged(
                    ref this._currentView,
                    value
                );
    }

    /// <summary>
    ///     How many matches to load.
    /// </summary>
    public static int MatchHistoryCount
    {
        get => Program.Settings.matchHistoryCount;
    }

    /// <summary>
    ///     The match that was most recently loaded.
    /// </summary>
    /// <remarks>
    ///     Used to get the next set of matches, if there are more than the limit.
    /// </remarks>
    public int CurrentMatch
    {
        get => this._currentProgressMatch;
        set =>
            this.RaiseAndSetIfChanged(
                    ref this._currentProgressMatch,
                    value
                );
    }

    /// <summary>
    ///     The URL path segment for the view.
    /// </summary>
    public string? UrlPathSegment
    {
        get => "MatchHistory";
    }

    /// <summary>
    ///     The screen that is hosting the view.
    /// </summary>
    public IScreen HostScreen { get; }

    private void loadMatches()
    {
        var matches = new Matches(
                current => this.RaiseAndSetIfChanged(
                        ref this._currentProgressMatch,
                        current,
                        nameof(this.CurrentMatch)
                    )
            );
    }
}
