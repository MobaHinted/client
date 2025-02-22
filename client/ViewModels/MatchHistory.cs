// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using client.Models;
using client.Models.Data.Matches;
using client.Views;
using client.Views.MatchHistory;
using ReactiveUI;

#endregion

namespace client.ViewModels;

public class MatchHistory : ReactiveObject, IRoutableViewModel
{
    public MatchHistory(IScreen? screen = null)
    {
        Program.Log(
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
        this.CurrentView = new LoadingSubView();
        LoadMatches();

        // Display the matches
        this.CurrentView = new HistorySubView();
    }

    private async void LoadMatches()
    {
        var matches = new Matches(loadingPercentageUpdater);

        while (!this.DoneLoading)
        {
            await Task.Delay(100);
        }

        await Task.Delay(100);

        this._matchData = matches.MatchData;
        return;

        void loadingPercentageUpdater(int currentPercentage)
        {
            this.RaiseAndSetIfChanged(
                    ref this._currentProgressMatch,
                    currentPercentage,
                    nameof(this.CurrentMatch)
                );

            // Navigate back to the loading screen
            if (currentPercentage == 100)
                this.DoneLoading = true;
        }
    }

    #region Current View

    /// <summary>
    ///     The current view that is being displayed within Match History.
    /// </summary>
    /// <remarks>
    ///     First, <see cref="client.Views.MatchHistory.LoadingSubView" /> then
    ///     <see cref="client.Views.MatchHistory.HistorySubView" />
    /// </remarks>
    private ISubView _currentView = null!;

    /// <summary>
    ///     The current view that is being displayed within Match History.
    /// </summary>
    /// <remarks>
    ///     First, <see cref="client.Views.MatchHistory.LoadingSubView" /> then
    ///     <see cref="client.Views.MatchHistory.HistorySubView" />
    /// </remarks>
    public ISubView CurrentView
    {
        get => this._currentView;
        set =>
            this.RaiseAndSetIfChanged(
                    ref this._currentView,
                    value
                );
    }

    #endregion

    #region Boilerplate Screen Variables

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

    #endregion

    #region Variables for sub-views

    #region Loading

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
    private int _currentProgressMatch;

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
    ///     Flag indicating loading has finished.
    /// </summary>
    private bool DoneLoading { get; set; }

    #endregion

    #region Display

    /// <summary>
    ///     The match data that was loaded, from
    ///     <see cref="client.Models.Data.Matches.Matches" />.
    /// </summary>
    private Dictionary<string, MatchData>? _matchData;

    #endregion

    #endregion
}
