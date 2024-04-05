// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using System.Text.Json;
using Camille.RiotGames;
using CamilleMatch = Camille.RiotGames.MatchV5.Match;

namespace client.Models.Data.Matches;

public class Matches
{
    /// <summary>
    ///     The action to update the progress bar.
    /// </summary>
    private readonly Action<int> _update;

    /// <summary>
    ///     The number of matches that have been loaded successfully.
    /// </summary>
    private int _loadedMatches;

    /// <summary>
    ///     The match data that has been loaded successfully.
    /// </summary>
    // ReSharper disable once FieldCanBeMadeReadOnly.Local
    private Dictionary<string, MatchData> _matchData =
        new Dictionary<string, MatchData>();

    /// <summary>
    ///     Any matches that failed to load, and will be retried.
    /// </summary>
    // ReSharper disable once FieldCanBeMadeReadOnly.Local
    private List<string> _matchesToRetry = [];

    /// <summary>
    ///     The number of matches that have failed to load, and will be retried once.
    /// </summary>
    private int _missedMatches;

    public Matches(Action<int> updateProgress)
    {
        this._update = updateProgress;
        load();
    }

    private async void load()
    {
        // Calculate how many steps to take, rounded up
        int steps = (int)Math.Ceiling(Program.Settings.matchHistoryCount / 25.0);

        // Get steps of 25 games
        for (int i = 0; i < steps; i++)
        {
            await Task.Run(() => { getMatches(i * 25); });

            // If on the last step, but we are missing matches, get more
            if (i == steps - 1
                && (this._missedMatches != 0
                    || this._matchData.Count < Program.Settings.matchHistoryCount))
                await Task.Run(() => { getMatches((i + 1) * 25); });
        }
    }

    private async void getMatches(int startIndex, int count = 25)
    {
        string[]? matchList = null;
        await Program
            .riotAPI.MatchV5()
            .GetMatchIdsByPUUIDAsync(
                    Program.Account.Continent,
                    Program.Account.PUUID,
                    count,
                    start: startIndex
                )
            .ContinueWith(
                    task =>
                    {
                        #region Task Error

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
                                    logLevel: LogLevel.error,
                                    logTo: LogTo.file
                                    | LogTo.console
                                    | LogTo.errorScreen,
                                    logLocation: LogLocation.download
                                );
                            return;
                        }

                        #endregion

                        try
                        {
                            matchList = task.Result;
                        }

                        #region Result Error

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
                                    logLevel: LogLevel.error,
                                    logTo: LogTo.file
                                    | LogTo.console
                                    | LogTo.errorScreen,
                                    logLocation: LogLocation.download
                                );
                        }

                        #endregion
                    }
                );

        #region API Error

        if (matchList == null)
        {
            // TODO: inspect the exception here, probably direct to error screen
            Program.log(
                    source: nameof(Matches),
                    method: "getMatches()",
                    doing: "Loading Matches",
                    message: "Received no usable data from Riot. Possible API error",
                    logLevel: LogLevel.error,
                    logTo: LogTo.file | LogTo.console | LogTo.retryPopup,
                    logLocation: LogLocation.download
                );
            return;
        }

        #endregion

        #region API 400 Error

        if (matchList.Contains("400-series"))
        {
            Program.log(
                    source: nameof(Matches),
                    method: "getMatches()",
                    doing: "Loading Matches",
                    message: "Received a 400-series error from Riot."
                    + "API key issue? Invalid request?",
                    logLevel: LogLevel.warning,
                    logTo: LogTo.file | LogTo.console | LogTo.errorScreen,
                    logLocation: LogLocation.download
                );
            return;
        }

        #endregion

#pragma warning disable CS4014
        // For each match string in matchList
        foreach (string matchID in matchList)
            // Get the match data, and update the list
        {
            Task.Run(() => { getMatchData(matchID); });
        }

        // Retry any matches that failed to load
        var matchesToRetryCopy = new List<string>(this._matchesToRetry);
        foreach (string matchID in matchesToRetryCopy)
        {
            Task.Run(
                    () =>
                    {
                        getMatchData(
                                matchID,
                                true
                            );
                    }
                );
        }
#pragma warning restore CS4014

        if (this._missedMatches != 0)
        {
            Program.log(
                    source: nameof(Matches),
                    method: "getMatches()",
                    doing: "Loading Matches",
                    message: "Finished Loading matches, but had misses",
                    debugSymbols:
                    [
                        $"Missed: {this._missedMatches} ({this._matchesToRetry.Count})",
                        "Misses: " + JsonSerializer.Serialize(this._matchesToRetry),
                    ],
                    logLevel: LogLevel.warning,
                    logLocation: LogLocation.main
                );
        }

        // Update the progress
        this._update(this._loadedMatches + this._missedMatches);
    }

    private void getMatchData(string matchID, bool retry = false)
    {
        // Remove the match from the retry list to avoid infinite retries
        if (retry)
            this._matchesToRetry.Remove(matchID);

        try
        {
            string cacheFile = $"{Constants.cachedMatchesFolder}{matchID}.json";
            CamilleMatch? match;

            // If the match is already cached, use that instead
            if (FileManagement.fileExists(cacheFile))
            {
                // TODO: Load MatchData instead of CamilleMatch
                // Load the match from the cache
                FileManagement.loadFromFile(
                        cacheFile,
                        out match
                    );

                // Log the success
                Program.log(
                        source: nameof(Matches),
                        method: "getMatches()",
                        doing: "Loading Matches",
                        message: "Loaded match data from cache",
                        debugSymbols:
                        [
                            matchID,
                            this._matchData.Count
                            + "/"
                            + Program.Settings.matchHistoryCount,
                        ],
                        logLevel: LogLevel.debug,
                        logTo: LogTo.file,
                        logLocation: LogLocation.download
                    );
            }
            // Otherwise download the data
            else
            {
                // Get the match data
                match = Program
                    .riotAPI.MatchV5()
                    // ReSharper disable once MethodHasAsyncOverload
                    .GetMatch(
                            Program.Account.Continent,
                            matchID
                        );

                // TODO: Save MatchData instead of CamilleMatch
                // Cache the match data
                FileManagement.saveToFile(
                        cacheFile,
                        match
                    );

                // Log the success
                Program.log(
                        source: nameof(Matches),
                        method: "getMatches()",
                        doing: "Loading Matches",
                        message: "Loaded match data",
                        debugSymbols:
                        [
                            matchID,
                            this._matchData.Count
                            + "/"
                            + Program.Settings.matchHistoryCount,
                        ],
                        logLevel: LogLevel.debug,
                        logTo: LogTo.file,
                        logLocation: LogLocation.download
                    );
            }

            // Add the match data to the dictionary
            this._matchData.Add(
                    matchID,
                    new MatchData(match!)
                );

            // Handle a retry
            if (retry)
            {
                this._missedMatches--;
            }

            // Update the progress
            this._loadedMatches++;
            this._update(this._loadedMatches + this._missedMatches);
        }

        #region Load Match Error

        catch (Exception e)
        {
            // Log the error
            Program.log(
                    source: nameof(Matches),
                    method: "getMatches()",
                    doing: "Loading Matches",
                    message: "Failed to load Match\n" + e.Message,
                    debugSymbols:
                    [
                        matchID,
                    ],
                    logLevel: LogLevel.warning,
                    logTo: LogTo.file | LogTo.console,
                    logLocation: LogLocation.download
                );

            // Only add to these variables if it's not a retry
            if (!retry)
            {
                this._missedMatches++;

                // Add the match to the retry list
                this._matchesToRetry.Add(matchID);
            }

            // Update the progress
            this._update(this._loadedMatches + this._missedMatches);
        }

        #endregion
    }
}
