// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using System.Text.Json;
using Camille.RiotGames;
using Camille.RiotGames.MatchV5;

namespace client.Models.Data;

public class Matches
{
    private Dictionary<string, MatchData>? _matchData;
    private Action<int> _update;

    public Matches(Action<int> updateProgress)
    {
        this._update = updateProgress;
        load();
    }

    private async void load()
    {
        await Task.Run(getMatches);
    }

    private async void getMatches()
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
                            Console.WriteLine("Faulted!\n\n");
                            Console.WriteLine(task.Exception);
                            return;
                        }

                        try
                        {
                            matchList = task.Result;
                        }
                        catch (Exception e)
                        {
                            Console.WriteLine("No string[]!\n\n");
                            Console.WriteLine(JsonSerializer.Serialize(task.Result));
                            Console.WriteLine(e);
                        }
                    }
                );

        if (matchList == null)
        {
            // TODO: inspect the exception here, probably direct to error screen
            Console.WriteLine("No matches found.");
            return;
        }

        if (matchList.Contains("400-series"))
        {
            Console.WriteLine("400");
            return;
        }

        this._matchData = new Dictionary<string, MatchData>();

        // For each match string in matchList
        foreach (string matchID in matchList)
        {
            Task.Run(
                    () =>
                    {
                        // Get the match data
                        Match? match = Program
                            .riotAPI.MatchV5()
                            .GetMatch(
                                    Program.Account.Continent,
                                    matchID
                                );
                        // TODO: catch and add to misses, updating with count+misses

                        // Add the match data to the dictionary
                        this._matchData.Add(
                                matchID,
                                new MatchData()
                            );

                        // Update the progress
                        this._update(this._matchData.Count);
                    }
                );
        }
    }

    private async void getMatchData() { }
}
