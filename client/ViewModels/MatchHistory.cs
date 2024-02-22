// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using System.Text.Json;
using Camille.RiotGames;
using client.Models;
using client.Models.Data;
using ReactiveUI;

namespace client.ViewModels;

public class MatchHistory : ReactiveObject, IRoutableViewModel
{
    private int _currentMatch;

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

        var t = new Matches(
                current => this.RaiseAndSetIfChanged(
                        ref this._currentMatch,
                        current,
                        nameof(this.CurrentMatch)
                    )
            );
    }

    public static int MatchHistoryCount
    {
        get => Program.Settings.matchHistoryCount;
    }

    /// <summary>
    ///     What step of match history loading we are on.
    /// </summary>
    public int CurrentMatch
    {
        get => this._currentMatch;
        set =>
            this.RaiseAndSetIfChanged(
                    ref this._currentMatch,
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
