// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using client.Models.Data.DataDragon;

#endregion

namespace client.Models.Data.GameData.Helpers;

public static class RuneHelper
{
    public static bool IsKeystone(short runeId)
    {
        short[] keystones = [];
        Program.Assets.Runes.runetrees.ForEach(
                tree =>
                {
                    var treeKeystones = tree.slots[0].runes;
                    keystones = keystones
                        .Concat(
                            treeKeystones.Select(rune => (short)rune.id).ToArray()
                        )
                        .ToArray();
                }
            );

        return keystones.Contains(runeId);
    }

    public static bool IsKeystone(Rune rune)
    {
        return IsKeystone((short)rune.id);
    }

    public static bool TryGetById(short runeId, out Rune? rune)
    {
        Rune? foundRune = null;
        Program.Assets.Runes.runetrees.ForEach(
                tree =>
                {
                    var treeRunes = tree.slots.SelectMany(slot => slot.runes);
                    foundRune = treeRunes.First(x => x.id == runeId);
                }
            );

        rune = foundRune;
        return foundRune != null;
    }

    public static RuneTree GetTreeByRuneId(short runeId)
    {
        RuneTree? foundTree = null;
        Program.Assets.Runes.runetrees.ForEach(
                tree =>
                {
                    var treeRunes = tree.slots.SelectMany(slot => slot.runes);
                    if (treeRunes.Any(rune => rune.id == runeId))
                        foundTree = tree;
                }
            );

        if (foundTree is null)
            throw new ArgumentException("Rune not found in any tree");

        return foundTree;
    }
}
