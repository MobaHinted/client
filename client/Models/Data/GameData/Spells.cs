// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

namespace client.Models.Data.GameData;

public class Spells(int summoner1, int summoner2)
{
    public short Summoner1 = (short)summoner1;
    public short Summoner2 = (short)summoner2;
}
