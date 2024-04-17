// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

// TODO: These classes need to be generated from the Data Dragon API

#region Header

// ReSharper disable InconsistentNaming
// ReSharper disable UnusedMember.Global
// ReSharper disable IdentifierTypo
// ReSharper disable ClassNeverInstantiated.Global
// ReSharper disable CollectionNeverUpdated.Global
// ReSharper disable UnusedAutoPropertyAccessor.Global

#region

using System.Text.Json;
using System.Text.Json.Serialization;

#endregion

#pragma warning disable CS8618 // Non-nullable field must contain a non-null value when exiting constructor. Consider declaring as nullable.
namespace client.Models.Data.DataDragon;

public interface Simple;

public class Image
{
    public string full { get; set; }
    public string sprite { get; set; }
    public string group { get; set; }
    public int x { get; set; }
    public int y { get; set; }
    public int w { get; set; }
    public int h { get; set; }

    public string imageURL
    {
        get
        {
            // Rune Images
            if (this.group.Contains("rune"))
                return "http://ddragon.leagueoflegends.com/cdn/img/" + this.full;

            // All other Images
            return "http://ddragon.leagueoflegends.com/cdn/"
                + $"{Program.Assets.Version}/img/{this.group}/{this.full}";
        }
    }
}

#endregion

#region Region Version

public class RegionVersion
{
    public string Version
    {
        get => this.v;
    }

    public Dictionary<string, string> n { get; set; }
    public string v { get; set; }
    public string l { get; set; }
    public string cdn { get; set; }
    public string dd { get; set; }
    public string lg { get; set; }
    public string css { get; set; }
    public int profileiconmax { get; set; }
    public object store { get; set; }
}

#endregion

#region Versions

public class Versions : Simple
{
    public List<string> versions { get; set; }

    public string latestVersion
    {
        get => this.versions[0];
    }
}

#endregion

#region Champions

public class Champions
{
    public string type { get; set; }
    public string format { get; set; }
    public string version { get; set; }
    public Dictionary<string, ChampionsData> data { get; set; }
}

public class ChampionsData
{
    public string version { get; set; }
    public string id { get; set; }
    public string key { get; set; }
    public string name { get; set; }
    public string title { get; set; }
    public string blurb { get; set; }
    public ChampionsInfo info { get; set; }
    public Image image { get; set; }
    public List<string> tags { get; set; }
    public string partype { get; set; }
    public ChampionsStats stats { get; set; }
}

public class ChampionsInfo
{
    public int dttack { get; set; }
    public int defense { get; set; }
    public int magic { get; set; }
    public int difficulty { get; set; }
}

public class ChampionsStats
{
    public double hp { get; set; }
    public double hpperlevel { get; set; }
    public double mp { get; set; }
    public double mpperlevel { get; set; }
    public double movespeed { get; set; }
    public double armor { get; set; }
    public double armorperlevel { get; set; }
    public double spellblock { get; set; }
    public double spellblockperlevel { get; set; }
    public double attackrange { get; set; }
    public double hpregen { get; set; }
    public double hpregenperlevel { get; set; }
    public double mpregen { get; set; }
    public double mpregenperlevel { get; set; }
    public double crit { get; set; }
    public double critperlevel { get; set; }
    public double attackdamage { get; set; }
    public double attackdamageperlevel { get; set; }
    public double attackspeedperlevel { get; set; }
    public double attackspeed { get; set; }
}

#endregion

#region Champion

public class IndividualChampion
{
    public string type { get; set; }
    public string format { get; set; }
    public string version { get; set; }
    public Dictionary<string, Champion> data { get; set; }

    public Champion Champion
    {
        get => this.data.Values.First();
    }
}

public class Champion
{
    public string id { get; set; }
    public string key { get; set; }
    public string name { get; set; }
    public string title { get; set; }
    public Image image { get; set; }
    public ChampionSkin[] skins { get; set; }
    public ChampionSpell[] spells { get; set; }
    public ChampionPassive passive { get; set; }
    public ChampionRecommended[] recommended { get; set; }
}

public class ChampionSkin
{
    public string id { get; set; }
    public int num { get; set; }
    public string name { get; set; }
    public bool chromas { get; set; }
}

public class ChampionSpell
{
    public string id { get; set; }
    public string name { get; set; }
    public string description { get; set; }
    public string tooltip { get; set; }
    public ChampionLevelTip leveltip { get; set; }
    public Image image { get; set; }
}

public class ChampionPassive
{
    public string name { get; set; }
    public string description { get; set; }
    public Image image { get; set; }
}

public class ChampionRecommended
{
    public string champion { get; set; }
    public string title { get; set; }
    public string map { get; set; }
    public string mode { get; set; }
    public string type { get; set; }
    public ChampionBlock[] blocks { get; set; }
}

public class ChampionBlock
{
    public string type { get; set; }
    public bool recmath { get; set; }
    public bool recsteps { get; set; }
    public ChampionItem[] items { get; set; }
}

public class ChampionItem
{
    public string id { get; set; }
    public int count { get; set; }
    public bool hideifsummonerspell { get; set; }
}

public class ChampionLevelTip
{
    public string[] label { get; set; }
    public string[] effect { get; set; }
}

#endregion

#region Items

public class Items
{
    public string type { get; set; }
    public string version { get; set; }
    public ItemBasic basic { get; set; }
    public Dictionary<string, ItemData> data { get; set; }
    public List<Groups> groups { get; set; }
    public List<Tree> tree { get; set; }
}

public class ItemBasic
{
    public string name { get; set; }
    public ItemRune rune { get; set; }
    public ItemGold gold { get; set; }
    public string group { get; set; }
    public string description { get; set; }
    public string colloq { get; set; }
    public string plaintext { get; set; }
    public bool consumed { get; set; }
    public int stacks { get; set; }
    public int depth { get; set; }
    public bool consumeonfull { get; set; }
    public List<string> from { get; set; }
    public List<string> into { get; set; }
    public int specialrecipe { get; set; }
    public bool instore { get; set; }
    public bool hidefromall { get; set; }
    public string requiredchampion { get; set; }
    public string requiredally { get; set; }
    public ItemStats stats { get; set; }
    public List<string> tags { get; set; }
    public ItemMaps maps { get; set; }
}

public class ItemStats
{
    public double? flathppoolmod { get; set; }
    public double? rFlatHPModPerLevel { get; set; }
    public double? flatmppoolmod { get; set; }
    public double? rFlatMPModPerLevel { get; set; }
    public double? percenthppoolmod { get; set; }
    public double? percentmppoolmod { get; set; }
    public double? flathpregenmod { get; set; }
    public double? rFlatHPRegenModPerLevel { get; set; }
    public double? percenthpregenmod { get; set; }
    public double? flatmpregenmod { get; set; }
    public double? rFlatMPRegenModPerLevel { get; set; }
    public double? percentmpregenmod { get; set; }
    public double? flatarmormod { get; set; }
    public double? rFlatArmorModPerLevel { get; set; }
    public double? percentarmormod { get; set; }
    public double? rFlatArmorPenetrationMod { get; set; }
    public double? rFlatArmorPenetrationModPerLevel { get; set; }
    public double? rPercentArmorPenetrationMod { get; set; }
    public double? rPercentArmorPenetrationModPerLevel { get; set; }
    public double? flatphysicaldamagemod { get; set; }
    public double? rFlatPhysicalDamageModPerLevel { get; set; }
    public double? percentphysicaldamagemod { get; set; }
    public double? flatmagicdamagemod { get; set; }
    public double? rFlatMagicDamageModPerLevel { get; set; }
    public double? percentmagicdamagemod { get; set; }
    public double? flatmovementspeedmod { get; set; }
    public double? rFlatMovementSpeedModPerLevel { get; set; }
    public double? percentmovementspeedmod { get; set; }
    public double? rPercentMovementSpeedModPerLevel { get; set; }
    public double? flatattackspeedmod { get; set; }
    public double? percentattackspeedmod { get; set; }
    public double? rPercentAttackSpeedModPerLevel { get; set; }
    public double? rFlatDodgeMod { get; set; }
    public double? rFlatDodgeModPerLevel { get; set; }
    public double? percentdodgemod { get; set; }
    public double? flatcritchancemod { get; set; }
    public double? rFlatCritChanceModPerLevel { get; set; }
    public double? percentcritchancemod { get; set; }
    public double? flatcritdamagemod { get; set; }
    public double? rFlatCritDamageModPerLevel { get; set; }
    public double? percentcritdamagemod { get; set; }
    public double? flatblockmod { get; set; }
    public double? percentblockmod { get; set; }
    public double? flatspellblockmod { get; set; }
    public double? rFlatSpellBlockModPerLevel { get; set; }
    public double? percentspellblockmod { get; set; }
    public double? flatexpbonus { get; set; }
    public double? percentexpbonus { get; set; }
    public double? rPercentCooldownMod { get; set; }
    public double? rPercentCooldownModPerLevel { get; set; }
    public double? rFlatTimeDeadMod { get; set; }
    public double? rFlatTimeDeadModPerLevel { get; set; }
    public double? rPercentTimeDeadMod { get; set; }
    public double? rPercentTimeDeadModPerLevel { get; set; }
    public double? rFlatGoldPer10Mod { get; set; }
    public double? rFlatMagicPenetrationMod { get; set; }
    public double? rFlatMagicPenetrationModPerLevel { get; set; }
    public double? rPercentMagicPenetrationMod { get; set; }
    public double? rPercentMagicPenetrationModPerLevel { get; set; }
    public double? flatenergyregenmod { get; set; }
    public double? rFlatEnergyRegenModPerLevel { get; set; }
    public double? flatenergypoolmod { get; set; }
    public double? rFlatEnergyModPerLevel { get; set; }
    public double? percentlifestealmod { get; set; }
    public double? percentspellvampmod { get; set; }
}

public class ItemRune
{
    public bool isrune { get; set; }
    public int tier { get; set; }
    public string type { get; set; }
}

public class ItemGold
{
    public int _base { get; set; }
    public int total { get; set; }
    public int sell { get; set; }
    public bool purchasable { get; set; }
}

public class ItemMaps
{
    public bool? _1 { get; set; }
    public bool? _2 { get; set; }
    public bool? _3 { get; set; }
    public bool? _4 { get; set; }
    public bool? _5 { get; set; }
    public bool? _6 { get; set; }
    public bool? _7 { get; set; }
    public bool? _8 { get; set; }
    public bool? _9 { get; set; }
    public bool? _10 { get; set; }
    public bool? _11 { get; set; }
    public bool? _12 { get; set; }
    public bool? _13 { get; set; }
    public bool? _14 { get; set; }
    public bool? _15 { get; set; }
    public bool? _16 { get; set; }
    public bool? _17 { get; set; }
    public bool? _18 { get; set; }
    public bool? _19 { get; set; }
    public bool? _20 { get; set; }
    public bool? _21 { get; set; }
    public bool? _22 { get; set; }
    public bool? _23 { get; set; }
    public bool? _24 { get; set; }
    public bool? _25 { get; set; }
    public bool? _26 { get; set; }
    public bool? _27 { get; set; }
    public bool? _28 { get; set; }
    public bool? _29 { get; set; }
    public bool? _30 { get; set; }
}

public class ItemData
{
    public string name { get; set; }
    public string description { get; set; }
    public string colloq { get; set; }
    public string plaintext { get; set; }
    public List<string> into { get; set; }
    public Image image { get; set; }
    public ItemGold gold { get; set; }
    public List<string> tags { get; set; }
    public ItemMaps maps { get; set; }
    public ItemStats stats { get; set; }
}

public class Groups
{
    public string id { get; set; }
    public string MaxGroupOwnable { get; set; }
}

public class Tree
{
    public List<Header> tree { get; set; }
}

public class Header
{
    public string header { get; set; }
    public List<string> tags { get; set; }
}

#endregion

#region SummonerSpells

public class SummonerSpells
{
    public string type { get; set; }
    public string version { get; set; }
    public Dictionary<string, SummonerSpell> data { get; set; }
}

public class SummonerSpell
{
    public string id { get; set; }
    public string name { get; set; }
    public string description { get; set; }
    public string tooltip { get; set; }
    public int maxrank { get; set; }
    public List<float> cooldown { get; set; }
    public string cooldownburn { get; set; }
    public List<int> cost { get; set; }
    public string costburn { get; set; }
    public SpellDataValues datavalues { get; set; }
    public List<List<float>?> effect { get; set; }
    public List<string?> effectburn { get; set; }
    public List<object> vars { get; set; }
    public string key { get; set; }
    public int summonerlevel { get; set; }
    public List<string> modes { get; set; }
    public string costtype { get; set; }
    public string maxammo { get; set; }
    public List<int> range { get; set; }
    public string rangeburn { get; set; }
    public Image image { get; set; }
    public string resource { get; set; }
}

public class SpellDataValues
{
    // This class is currently empty as the provided JSON does not contain any data values.
    // If the JSON can contain data values, you should add properties here to represent them.
}

#endregion

#region Runes

public class Runes : Simple
{
    public List<RuneTree> runetrees { get; set; }
}

public class RuneTree
{
    public int id { get; set; }
    public string key { get; set; }
    public string icon { get; set; }
    public string name { get; set; }
    public List<Slot> slots { get; set; }

    public Image image
    {
        get =>
            new Image
            {
                full = this.icon,
                sprite = this.key,
                group = "rune-trees",
                x = 0,
                y = 0,
                w = 32,
                h = 32,
            };
    }
}

public class Slot
{
    public List<Rune> runes { get; set; }
}

public class Rune
{
    public int id { get; set; }
    public string key { get; set; }
    public string icon { get; set; }
    public string name { get; set; }
    public string shortdesc { get; set; }
    public string longdesc { get; set; }

    public Image image
    {
        get =>
            new Image
            {
                full = this.icon,
                sprite = this.key,
                group = "runes",
                x = 0,
                y = 0,
                w = 256,
                h = 256,
            };
    }
}

#endregion

#region ProfileIcons

public class ProfileIcons
{
    public string type { get; set; }
    public string version { get; set; }
    public Dictionary<string, ProfileIcon> data { get; set; }
}

public class ProfileIcon
{
    private JsonElement _idElement;

    [JsonIgnore]
    public int id
    {
        get
        {
            return this._idElement.ValueKind switch
            {
                JsonValueKind.String => int.Parse(this._idElement.GetString()!),
                JsonValueKind.Number => this._idElement.GetInt32(),
                _ => throw new InvalidOperationException("'id' must be a number"),
            };
        }
    }

    [JsonPropertyName("id")]
    public object idForSerialization
    {
        get
        {
            return this._idElement.ValueKind switch
            {
                JsonValueKind.String => this._idElement.GetString()!,
                JsonValueKind.Number => this._idElement.GetInt32(),
                _ => throw new InvalidOperationException("'id' must be a number"),
            };
        }
        set => this._idElement = (JsonElement)value;
    }

    public Image image { get; set; }
}

#endregion
