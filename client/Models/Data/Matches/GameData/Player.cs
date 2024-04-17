// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using Camille.RiotGames.MatchV5;

#endregion

namespace client.Models.Data.Matches.GameData;

/// <summary>
///     A class to hold the data for each player in a
///     <see cref="MatchData">Match</see>.
/// </summary>
public class Player(Participant player)
{
    public readonly Item[] Items =
    [
        new Item(player.Item0),
        new Item(player.Item1),
        new Item(player.Item2),
        new Item(player.Item3),
        new Item(player.Item4),
        new Item(player.Item5),
        new Item(player.Item6),
    ];

    public readonly Spells Spells = new Spells(
            player.Summoner1Id,
            player.Summoner2Id
        );
    public readonly Runes Runes = new Runes(player.Perks);
}
