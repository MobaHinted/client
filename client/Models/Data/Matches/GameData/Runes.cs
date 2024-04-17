// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using Camille.RiotGames.MatchV5;

#endregion

namespace client.Models.Data.Matches.GameData;

public class Runes
{
    private readonly Perks _perks;

    public Runes(Perks perks)
    {
        this._perks = perks;
    }
}
