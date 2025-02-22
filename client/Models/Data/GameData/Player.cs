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
        ChampionHelper.GetByName(player.ChampionName);

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

    public readonly string DisplayName =
        (player.RiotIdGameName ?? player.SummonerName)
        + "#"
        + (player.RiotIdTagline ?? "");

    public readonly string Name = player.RiotIdGameName ?? player.SummonerName;

    public readonly string Tag = player.RiotIdTagline ?? "";

    #endregion

    #region KDA

    public readonly short Kills = (short)player.Kills;

    public readonly short LargestMultiKill = (short)player.LargestMultiKill;

    public readonly short LargestKillingSpree = (short)player.LargestKillingSpree;

    public readonly short TripleKills = (short)player.TripleKills;

    public readonly short QuadraKills = (short)player.QuadraKills;

    public readonly short PentaKills = (short)player.PentaKills;

    public readonly short Assists = (short)player.Assists;

    public readonly short Deaths = (short)player.Deaths;

    public readonly float KillAndAssistToDeathRatio =
        (float)(player.Kills + player.Assists) / player.Deaths;

    public readonly float KillToDeathRatio = (float)player.Kills / player.Deaths;

    #endregion

    #region Damage

    public readonly int Damage = player.TotalDamageDealt;

    public readonly float DamagePerMinute = (float)Math.Round(
            (float)player.TotalDamageDealt / duration,
            2
        );

    public readonly int DamageToChampions = player
        .TotalDamageDealtToChampions;

    public readonly float DamageToChampionsPerMinute = (float)Math.Round(
            (float)player.TotalDamageDealtToChampions / duration,
            2
        );

    public readonly int PhysicalDamage = player.PhysicalDamageDealt;

    public readonly int PhysicalDamageToChampions =
        player.PhysicalDamageDealtToChampions;

    public readonly int MagicDamage = player.MagicDamageDealt;

    public readonly int MagicDamageToChampions =
        player.MagicDamageDealtToChampions;

    public readonly int TrueDamage = player.TrueDamageDealt;

    public readonly int TrueDamageToChampions =
        player.TrueDamageDealtToChampions;

    public readonly int TurretDamage = player.DamageDealtToTurrets;

    public readonly int ObjectiveDamage = player.DamageDealtToObjectives;

    public readonly int DamageTaken = player.TotalDamageTaken;

    #endregion

    #region Vision

    public readonly short WardsPlaced = (short)player.WardsPlaced;

    public readonly short WardsDestroyed = (short)player.WardsKilled;

    public readonly short ControlWardsPurchased =
        (short)player.VisionWardsBoughtInGame;

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

    #region Heal/Shield

    public readonly int SelfHealing =
        player.TotalHeal - player.TotalHealsOnTeammates;

    public readonly int HealingDone = player.TotalHealsOnTeammates;

    public readonly int ShieldingDone = player.TotalDamageShieldedOnTeammates;

    public readonly float HealingPerMinute = (float)Math.Round(
            (float)(player.TotalHeal - player.TotalHealsOnTeammates) / duration,
            2
        );

    public readonly float ShieldingPerMinute = (float)Math.Round(
            (float)player.TotalDamageShieldedOnTeammates / duration,
            2
        );

    public readonly float HealAndShieldPerMinute = (float)Math.Round(
            (float)(player.TotalHeal
                - player.TotalHealsOnTeammates
                + player.TotalDamageShieldedOnTeammates)
            / duration,
            2
        );

    #endregion

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

    public readonly short CrowdControlScore = (short)player.TimeCCingOthers;

    public readonly short TurretTakedowns = (short)(player.TurretTakedowns ?? 0);

    /// <summary>
    ///     This is the role that is most likely to be correct.
    /// </summary>
    public readonly string RiotDetectedRole = player.IndividualPosition;

    /// <summary>
    ///     This is the probable role given that each team needs one of each role.
    /// </summary>
    public readonly string RiotDetectedRoleInTeam = player.TeamPosition;

    #endregion
}
