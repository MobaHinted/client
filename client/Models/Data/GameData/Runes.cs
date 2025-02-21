// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using Camille.RiotGames.MatchV5;

#endregion

namespace client.Models.Data.GameData;

public class Runes(Perks perks)
{
    private readonly Perks _perks = perks;
}
