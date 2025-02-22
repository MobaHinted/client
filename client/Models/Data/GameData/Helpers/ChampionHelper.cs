// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using client.Models.Data.DataDragon;

#endregion

namespace client.Models.Data.GameData.Helpers;

public static class ChampionHelper
{
    /// <summary>
    ///     Converts a string Display name of a champion to the
    ///     <see cref="ChampionData" /> value.
    /// </summary>
    /// <param name="championName">
    ///     The display name of the champion.
    /// </param>
    /// <returns>
    ///     The <see cref="ChampionData" /> value.
    /// </returns>
    /// <exception cref="ArgumentException">
    ///     Thrown when no champion is found with the given name.
    /// </exception>
    /// <remarks>
    ///     This is considered safer than handling the Champion ID, as the field was
    ///     unreliable before season 11.
    /// </remarks>
    public static ChampionData GetByName(string championName)
    {
        ChampionData? championData = Program.Assets.Champions.data.FirstOrDefault(
                    kvp => kvp.Key.Equals(
                            championName,
                            StringComparison.CurrentCultureIgnoreCase
                        )
                )
            .Value;

        if (championData is null)
            throw new ArgumentException(
                    "Champion not found with name " + championName
                );

        return championData;
    }
}
