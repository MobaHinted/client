// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using client.Models.Data.DataDragon;

#endregion

namespace client.Models.Data.GameData;

public class Item
{
    public string Description;

    public short ID;

    public Image Image;

    public string Name;

    public Item(int id)
    {
        this.ID = (short)id;

        ItemData item = Program.Assets.Items.data[id.ToString()];

        this.Name = item.name;
        this.Description = item.description;
        this.Image = item.image;

        Program.log(
                source: nameof(Item),
                method: "Item()",
                doing: "Parsing Item Data",
                message: "ID: " + this.ID,
                logLevel: LogLevel.debug,
                logLocation: LogLocation.verbose,
                logTo: LogTo.file
            );
    }
}
