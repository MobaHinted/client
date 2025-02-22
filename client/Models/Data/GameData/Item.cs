// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using client.Models.Data.DataDragon;

#endregion

namespace client.Models.Data.GameData;

public class Item
{
    public string Description;

    public int Id;

    public Image Image;

    public string Name;

    public Item(int id)
    {
        this.Id = id;

        if (!Program.Assets.Items.data.TryGetValue(
                    id.ToString(),
                    out ItemData? item
                ))
            throw new ArgumentException("Item not found with ID " + id);

        this.Name = item.name;
        this.Description = item.description;
        this.Image = item.image;

        Program.Log(
                source: nameof(Item),
                method: "Item()",
                doing: "Parsed Item Data",
                message: "ID: " + this.Id,
                logLevel: LogLevel.debug,
                logLocation: LogLocation.verbose,
                logTo: LogTo.file
            );
    }
}
