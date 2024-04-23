// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using Camille.RiotGames.MatchV5;

#endregion

namespace client.Models.Data.Matches;

#region

using CamilleMatch = Camille.RiotGames.MatchV5.Match;
using CamilleTeam = Team;
using TeamData = GameData.Team;

#endregion

/// <summary>
///     The parsed data for a match.
/// </summary>
public class MatchData
{
    /// <summary>
    ///     The match in question to work from.
    /// </summary>
    private readonly CamilleMatch _match;

    /// <summary>
    ///     A list of all the teams in the match.
    /// </summary>
    /// <remarks>
    ///     Typically two teams, but could be more in special game modes, such as
    ///     Arena.
    ///     <br /><br />
    ///     <b>Key</b> - The team's ID. See the
    ///     <see cref="Camille.RiotGames.Enums.Team">Teams enum</see>.
    ///     <br />
    ///     <b>Value</b> - The parsed data for the team.
    /// </remarks>
    /// <param name="100">Blue Team</param>
    /// <param name="200">Red Team</param>
    /// <param name="300">Baron</param>
    /// <!--TODO: Add Arena Team IDs-->
    private readonly Dictionary<Camille.RiotGames.Enums.Team, TeamData> _teams = [];

    /// <summary>
    ///     Creates a new instance of parsed <see cref="MatchData" />.
    /// </summary>
    /// <param name="match">
    ///     A <see cref="CamilleMatch" /> from
    ///     <see cref="Camille.RiotGames.MatchV5Endpoints.GetMatch">
    ///         Camille.MatchV5.GetMatch()
    ///     </see>
    /// </param>
    public MatchData(CamilleMatch match)
    {
        Program.log(
                source: nameof(MatchData),
                method: "MatchData()",
                doing: "Parsing Match Data",
                message: match.Metadata.MatchId
                + " in patch "
                + match.Info.GameVersion,
                logLevel: LogLevel.debug,
                logLocation: LogLocation.verbose,
                logTo: LogTo.file
            );

        this._match = match;
        parseTeams();
    }

    /// <summary>
    ///     The ID of the match.
    /// </summary>
    public string MatchId
    {
        get => this._match.Metadata.MatchId;
    }

    /// <summary>
    ///     Parsing of the teams and their players in the match.
    /// </summary>
    private void parseTeams()
    {
        // Parse each team, and their players
        foreach (CamilleTeam team in this._match.Info.Teams)
        {
            // Add the team to the list
            this._teams.Add(
                    team.TeamId, // The team, e.g. red or blue
                    new TeamData(
                            team, // The team's data
                            this
                                ._match.Info.Participants //The players in the match
                                .Where(
                                        p => p.TeamId == team.TeamId
                                    ) // Filtered to the same team
                                .ToArray() // Converted to an array
                        )
                );
        }
    }

    #region Version

    /// <summary>
    ///     The simple version of the game that the match was played on.
    /// </summary>
    /// <remarks>
    ///     A backing field.
    /// </remarks>
    private float? _gameVersion;

    /// <summary>
    ///     The simple version of the game that the match was played on.
    /// </summary>
    public float GameVersion
    {
        get
        {
            // Use the backing field if populated.
            if (this._gameVersion is not null)
            {
                return (float)this._gameVersion;
            }

            // Parse the version number to get just the major and minor
            string gameVersion = this._match.Info.GameVersion;
            string[] parts = gameVersion.Split('.');
            float version = float.Parse(parts[0] + "." + parts[1]);

            // Populate the backing field and return the version
            this._gameVersion = version;
            return version;
        }
    }

    /// <summary>
    ///     The full version of the game that the match was played on.
    /// </summary>
    private string FullGameVersion
    {
        get => this._match.Info.GameVersion;
    }

    #endregion

    #region Time

    /// <summary>
    ///     How many minutes the match lasted.
    /// </summary>
    public int Duration
    {
        // ReSharper disable once PossibleLossOfFraction
        get => (int)Math.Round((double)(this._match.Info.GameDuration / 60));
    }

    /// <summary>
    ///     The time the game started.
    /// </summary>
    private DateTime GameStart
    {
        get =>
            DateTimeOffset
                .FromUnixTimeMilliseconds(this._match.Info.GameStartTimestamp)
                .DateTime;
    }

    /// <summary>
    ///     The time the game ended.
    /// </summary>
    /// <remarks>
    ///     A backing field.
    /// </remarks>
    private DateTime? _gameEnd;

    /// <summary>
    ///     The time the game ended.
    /// </summary>
    private DateTime GameEnd
    {
        get
        {
            if (this._gameEnd is not null)
            {
                return (DateTime)this._gameEnd;
            }

            // Handle games without an end timestamp
            if (this._match.Info.GameEndTimestamp is null)
            {
                DateTime endTime = this.GameStart.AddMinutes(this.Duration);
                this._gameEnd = endTime;
                return endTime;
            }

            // Return the precise end time
            DateTime preciseEndTime = DateTimeOffset
                .FromUnixTimeMilliseconds((long)this._match.Info.GameEndTimestamp!)
                .DateTime;
            this._gameEnd = preciseEndTime;
            return preciseEndTime;
        }
    }

    #endregion
}
