// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

namespace client.Models.Data.Matches.GameData;

public class Item
{
    public short Id;

    public Item(int id)
    {
        this.Id = (short)id;
    }
}
