// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using System.Text.Json;
using Camille.RiotGames;
using client.Models;
using client.Models.Data;
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
                logLevel: LogLevel.info
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
        var t = new Matches(
                current => this.RaiseAndSetIfChanged(
                        ref this._currentProgressMatch,
                        current,
                        nameof(this.CurrentMatch)
                    )
            );
    }

    /// <summary>
    ///     The current view that is being displayed within Match History.
    /// </summary>
    /// <remarks>
    ///     First, <see cref="MatchHistoryLoadingView" /> then
    ///     <see cref="MatchHistoryMatchesView" />
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

    public string? UrlPathSegment
    {
        get => "MatchHistory";
    }

    public IScreen HostScreen { get; }

    private void loadMatches()
    {
        Program
            .riotAPI.MatchV5()
            .GetMatchIdsByPUUIDAsync(
                    Program.Account.Continent,
                    Program.Account.PUUID,
                    Program.Settings.matchHistoryCount
                )
            .ContinueWith(
                    task =>
                    {
                        if (task.IsFaulted)
                        {
                            Console.WriteLine(task.Exception);
                            return;
                        }

                        string[] matchList = task.Result;

                        foreach (string match in matchList)
                        {
                            Console.WriteLine(
                                    $"{match}: "
                                    + JsonSerializer.Serialize(
                                            Program
                                                .riotAPI.MatchV5()
                                                .GetMatchAsync(
                                                        Program.Account.Continent,
                                                        match
                                                    )
                                                .Result
                                        )
                                );
                        }
                    }
                );
    }
}
