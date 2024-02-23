// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using System.Text.Json;
using Camille.RiotGames;
using CamilleMatch = Camille.RiotGames.MatchV5.Match;

namespace client.Models.Data.Matches;

public class Matches
{
    private Dictionary<string, MatchData>? _matchData;

    /// <summary>
    ///     The action to update the progress bar.
    /// </summary>
    private Action<int> _update;

    public Matches(Action<int> updateProgress)
    {
        this._update = updateProgress;
        load();
    }

    private async void load()
    {
        await Task.Run(() => { getMatches(); });
    }

    private async void getMatches(float? endDate = null)
    {
        // If match history count is >100, throw an exception
        // TODO: Loop for >100 matches
        if (Program.Settings.matchHistoryCount > 100)
        {
            throw new ArgumentOutOfRangeException(
                    nameof(Program.Settings.matchHistoryCount),
                    "Match history count cannot exceed 100"
                );
        }

        string[]? matchList = null;
        await Program
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
                            Program.log(
                                    source: nameof(Matches),
                                    method: "getMatches()",
                                    doing: "Loading Matches",
                                    message: "Task to retrieve match faulted \n"
                                    + task.Exception.Message,
                                    debugSymbols:
                                    [
                                        JsonSerializer.Serialize(task.Result),
                                    ],
                                    logLevel: LogLevel.error
                                );
                            return;
                        }

                        try
                        {
                            matchList = task.Result;
                        }
                        catch (Exception e)
                        {
                            Program.log(
                                    source: nameof(Matches),
                                    method: "getMatches()",
                                    doing: "Loading Matches",
                                    message: "Received no string[] data from Riot;"
                                    + "API error status\n"
                                    + e.Message,
                                    debugSymbols:
                                    [
                                        JsonSerializer.Serialize(task.Result),
                                    ],
                                    logLevel: LogLevel.error
                                );
                        }
                    }
                );

        if (matchList == null)
        {
            // TODO: inspect the exception here, probably direct to error screen
            Program.log(
                    source: nameof(Matches),
                    method: "getMatches()",
                    doing: "Loading Matches",
                    message: "Received no usable data from Riot. Possible API error",
                    logLevel: LogLevel.error
                );
            return;
        }

        if (matchList.Contains("400-series"))
        {
            Program.log(
                    source: nameof(Matches),
                    method: "getMatches()",
                    doing: "Loading Matches",
                    message: "Received a 400-series error from Riot."
                    + "API key issue? Invalid request?",
                    logLevel: LogLevel.warning
                );
            return;
        }

        this._matchData = new Dictionary<string, MatchData>();

        // For each match string in matchList
        foreach (string matchID in matchList)
        {
            Task.Run(
                    () =>
                    {
                        try
                        {
                            // Get the match data
                            CamilleMatch? match = Program
                                .riotAPI.MatchV5()
                                .GetMatch(
                                        Program.Account.Continent,
                                        matchID
                                    );
                        }
                        catch (Exception e)
                        {
                            Program.log(
                                    source: nameof(Matches),
                                    method: "getMatches()",
                                    doing: "Loading Matches",
                                    message: "Failed to load Match\n" + e.Message,
                                    debugSymbols:
                                    [
                                        matchID,
                                    ],
                                    logLevel: LogLevel.warning
                                );
                        }
                        // TODO: catch and add to misses, updating with count+misses

                        // Add the match data to the dictionary
                        this._matchData.Add(
                                matchID,
                                new MatchData()
                            );
                        Program.log(
                                source: nameof(Matches),
                                method: "getMatches()",
                                doing: "Loading Matches",
                                message: "Loaded match data",
                                //+ JsonSerializer.Serialize(match),
                                debugSymbols:
                                [
                                    matchID,
                                    $"{this._matchData.Count.ToString()}/{Program.Settings.matchHistoryCount}",
                                ],
                                logLevel: LogLevel.debug
                            );

                        // Update the progress
                        this._update(this._matchData.Count);
                    }
                );
        }
    }

    private async void getMatchData() { }
}
