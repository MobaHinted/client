// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using client.Models.Data.DataDragon;

#endregion

namespace client.Models.Data.Matches.GameData;

public class Item
{
    public short ID;
    private readonly ItemData _rawItem;

    public string Name
    {
        get => this._rawItem.name;
    }

    public string Description
    {
        get => this._rawItem.description;
    }

    public Image Image
    {
        get => this._rawItem.image;
    }

    public Item(int id)
    {
        this.ID = (short)id;

        this._rawItem = Program.Assets.Items.data[id.ToString()];

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
