// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using Camille.Enums;

#endregion

namespace client.Models.Data.GameData.Helpers;

public static class ChampionHelper
{
    /// <summary>
    ///     Converts a string Display name of a champion to the
    ///     <see cref="Champion">Camille Champion enum</see> value.
    /// </summary>
    /// <param name="championName">
    ///     The display name of the champion.
    /// </param>
    /// <returns>
    ///     The <see cref="Champion">Camille Champion enum</see> value.
    /// </returns>
    /// <exception cref="ArgumentException">
    ///     Thrown when no champion is found with the given name.
    /// </exception>
    /// <remarks>
    ///     This is considered safer than handling the Champion ID, as the field was
    ///     unreliable before season 11.
    /// </remarks>
    public static Champion getByName(string championName)
    {
        string upperDescription = championName.ToUpper();
        if (Enum.TryParse(
                    typeof(Champion),
                    upperDescription,
                    out object? result
                ))
            return (Champion)result;

        throw new ArgumentException("No champion found with that name.");
    }
}
