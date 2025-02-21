// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using Camille.RiotGames.MatchV5;
using client.Models.Data.DataDragon;
using client.Models.Data.GameData.Helpers;

#endregion

namespace client.Models.Data.GameData;

/// <summary>
///     A class to hold the data for each player in a
///     <see cref="MatchData">Match</see>.
/// </summary>
public class Player(Participant player, short duration)
{
    public readonly ChampionData Champion =
        ChampionHelper.getByName(player.ChampionName);

    public readonly Item[] Items =
    [
        new Item(player.Item0),
        new Item(player.Item1),
        new Item(player.Item2),
        new Item(player.Item3),
        new Item(player.Item4),
        new Item(player.Item5),
        new Item(player.Item6),
    ];

    public readonly Runes Runes = new Runes(player.Perks);

    public readonly Spells Spells = new Spells(
            player.Summoner1Id,
            player.Summoner2Id
        );

    #region Name

    public readonly string DisplayName = player.RiotIdGameName
        ?? player.SummonerName + "#" + player.RiotIdTagline ?? "";

    public readonly string Name = player.RiotIdGameName ?? player.SummonerName;

    public readonly string Tag = player.RiotIdTagline ?? "";

    #endregion

    #region KDA

    public readonly short Kills = (short)player.Kills;

    public readonly short LargestMultiKill = (short)player.LargestMultiKill;

    public readonly short LargestKillingSpree = (short)player.LargestKillingSpree;

    public readonly short Triplekills = (short)player.TripleKills;

    public readonly short Quadrakills = (short)player.QuadraKills;

    public readonly short Pentakills = (short)player.PentaKills;

    public readonly short Assists = (short)player.Assists;

    public readonly short Deaths = (short)player.Deaths;

    public readonly float KillAndAssistToDeathRatio =
        (float)(player.Kills + player.Assists) / player.Deaths;

    public readonly float KillToDeathRatio = (float)player.Kills / player.Deaths;

    #endregion

    #region Damage

    public readonly int TotalDamageDealt = player.TotalDamageDealt;

    public readonly float DamagePerMinute = (float)Math.Round(
            (float)player.TotalDamageDealt / duration,
            2
        );

    public readonly int TotalDamageDealtToChampions = player
        .TotalDamageDealtToChampions;

    public readonly float DamageToChampionsPerMinute = (float)Math.Round(
            (float)player.TotalDamageDealtToChampions / duration,
            2
        );

    public readonly int PhysicalDamageDealt = player.PhysicalDamageDealt;

    public readonly int PhysicalDamageDealtToChampions =
        player.PhysicalDamageDealtToChampions;

    public readonly int MagicDamageDealt = player.MagicDamageDealt;

    public readonly int MagicDamageDealtToChampions =
        player.MagicDamageDealtToChampions;

    public readonly int TrueDamageDealt = player.TrueDamageDealt;

    public readonly int TrueDamageDealtToChampions =
        player.TrueDamageDealtToChampions;

    public readonly int TurretDamage = player.DamageDealtToTurrets;

    public readonly int ObjectiveDamage = player.DamageDealtToObjectives;

    #endregion

    #region Vision

    public readonly short WardsPlaced = (short)player.WardsPlaced;

    public readonly short WardsDestroyed = (short)player.WardsKilled;

    public readonly short ControlWardsBought = (short)player.VisionWardsBoughtInGame;

    public readonly short VisionScore = (short)player.VisionScore;

    public readonly float VisionScorePerMinute = (float)Math.Round(
            (float)player.VisionScore / duration,
            2
        );

    #endregion

    #region CS

    public readonly short MinionsKilled = (short)player.TotalMinionsKilled;

    public readonly short JungleMinionsKilled = (short)player.NeutralMinionsKilled;

    public readonly short CreepScore =
        (short)(player.TotalMinionsKilled + player.NeutralMinionsKilled);

    public readonly float CreepScorePerMinute = (float)Math.Round(
            (float)(player.TotalMinionsKilled + player.NeutralMinionsKilled)
            / duration,
            2
        );

    #endregion

    // TODO: Heal/Shield data

    // TODO: CC data

    #region Misc

    public readonly byte Level = (byte)player.ChampLevel;

    public readonly int GoldEarned = player.GoldEarned;

    public readonly short HelpfulPings = (short)((player.RetreatPings ?? 0)
        + (player.AssistMePings ?? 0)
        + (player.EnemyVisionPings ?? 0)
        + (player.OnMyWayPings ?? 0)
        + (player.AllInPings ?? 0));

    public readonly float HelpfulPingsPerMinute = (float)Math.Round(
            (float)((player.RetreatPings ?? 0)
                + (player.AssistMePings ?? 0)
                + (player.EnemyVisionPings ?? 0)
                + (player.OnMyWayPings ?? 0)
                + (player.AllInPings ?? 0))
            / duration,
            2
        );

    public readonly short TurretTakedowns = (short)(player.TurretTakedowns ?? 0);

    #endregion
}
