// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

namespace client.Models.Data.Matches.GameData;

public class Spells
{
    public short Summoner1;
    public short Summoner2;

    public Spells(int summoner1, int summoner2)
    {
        this.Summoner1 = (short)summoner1;
        this.Summoner2 = (short)summoner2;
    }
}
