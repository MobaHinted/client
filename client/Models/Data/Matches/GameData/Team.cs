// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using Camille.RiotGames.MatchV5;
using CamilleTeam = Camille.RiotGames.MatchV5.Team;

#endregion

namespace client.Models.Data.Matches.GameData;

/// <summary>
///     A class to hold the data for each <see cref="Player">Player</see> for a
///     team in a <see cref="MatchData">Match</see>, as well as the team's combined
///     stats.
/// </summary>
public class Team
{
    /// <summary>
    ///     A dictionary of the players on the team.
    /// </summary>
    /// <remarks>
    ///     Key is converted to the player's <see cref="Role">Role</see> on
    ///     Summoner's Rift.
    /// </remarks>
    public Dictionary<byte, Player> Players = new Dictionary<byte, Player>();

    /// <summary>
    ///     Creates a new instance of <see cref="Team" />.
    /// </summary>
    /// <param name="team">
    ///     A <see cref="Camille.RiotGames.MatchV5.Team" /> from a
    ///     <see cref="Camille.RiotGames.MatchV5.Match.Info">Match's Info</see>.
    /// </param>
    /// <param name="players">
    ///     A sub-array of
    ///     <see cref="Camille.RiotGames.MatchV5.Participant">
    ///         Players
    ///     </see>
    ///     from a
    ///     <see cref="Camille.RiotGames.MatchV5.Match.Info">Match's Info</see>.
    /// </param>
    public Team(CamilleTeam team, IReadOnlyCollection<Participant> players)
    {
        Program.log(
                source: nameof(Team),
                method: "TeamData()",
                doing: "Parsing Team Data",
                message: "Team: " + team.TeamId,
                debugSymbols:
                [
                    "Players: " + players.Count,
                ],
                logLevel: LogLevel.debug,
                logLocation: LogLocation.verbose,
                logTo: LogTo.file
            );

        byte counter = 0;
        // Parse each player
        foreach (Participant player in players)
        {
            counter++;
            // Parse the player data
            var playerData = new Player(player);
            // TODO: Only parse the role in summoner's rift
            // Parse the player's role
            byte role = (byte)Roles.determine(
                    player.ChampionId,
                    playerData.Items,
                    playerData.Spells,
                    playerData.Runes,
                    player.Lane,
                    player.Role,
                    (byte)player.ChampLevel,
                    (short)(player.TotalAllyJungleMinionsKilled ?? 0),
                    (short)player.TotalMinionsKilled,
                    (short)player.VisionScore
                );

            // Add the player to the dictionary
            this.Players.Add(
                    //role, // TODO: Switch to using this once role checking is implemented
                    counter,
                    playerData
                );
        }
    }
}
