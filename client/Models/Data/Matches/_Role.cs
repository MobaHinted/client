// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using Camille.Enums;

namespace client.Models.Data.Matches;

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
