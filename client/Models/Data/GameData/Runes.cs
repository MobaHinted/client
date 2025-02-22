// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using System.Text.Json;
using Camille.RiotGames.MatchV5;
using client.Models.Data.DataDragon;
using client.Models.Data.GameData.Helpers;

#endregion

namespace client.Models.Data.GameData;

public class Runes
{
    public Rune Keystone = null!;

    public List<Rune> PrimaryRunes = [];

    public RuneTree? PrimaryTree;

    public List<Rune> SecondaryRunes = [];

    public RuneTree? SecondaryTree;

    public Runes(Perks perks)
    {
        // TODO: implement `perks.StatPerks`: it's the three minor buffs you choose

        var runes = perks.Styles;

        var primaryRunes = runes[0].Selections;
        var secondaryRunes = runes[1].Selections;

        primaryRunes
            .Concat(secondaryRunes)
            .ToList()
            .ForEach(
                    x =>
                    {
                        short id = (short)x.Perk;

                        // Load Rune
                        Rune rune = RuneHelper.GetById(id);

                        // Set Keystone
                        if (RuneHelper.IsKeystone(rune))
                            this.Keystone = rune;

                        // Set Trees
                        RuneTree tree = RuneHelper.GetTreeByRuneId(id);
                        if (this.PrimaryTree is null)
                            this.PrimaryTree = tree;
                        if (this.SecondaryTree is null && tree != this.PrimaryTree)
                            this.SecondaryTree = tree;

                        // Save Rune
                        if (tree == this.PrimaryTree)
                            this.PrimaryRunes.Add(rune!);
                        else
                            this.SecondaryRunes.Add(rune!);
                    }
                );

        string runeIds = string.Join(
                ",",
                this.PrimaryRunes.Concat(this.SecondaryRunes).Select(r => r.id)
            );

        Program.Log(
                source: nameof(Runes),
                method: "Runes()",
                doing: "Parsed Runes Data",
                message: "Runes: " + runeIds,
                debugSymbols:
                [
                    JsonSerializer.Serialize(runes),
                ],
                logLevel: LogLevel.debug,
                logLocation: LogLocation.verbose,
                logTo: LogTo.file
            );
    }
}
