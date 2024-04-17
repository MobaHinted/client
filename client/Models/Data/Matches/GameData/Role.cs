// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using Camille.Enums;

#endregion

namespace client.Models.Data.Matches.GameData;

public enum Role
{
    top,
    jungle,
    middle,
    bottom,
    support,
}

public class Roles
{
    public static Role determine(
        Champion champion,
        Item[] items,
        Spells spells,
        Runes runes,
        string supposedLane,
        string supposedRole,
        byte level,
        short jungleMinionsKilled,
        short minionsKilled,
        short visionScore,
        bool isBot = false
    )
    {
        return Role.middle;
    }
}
