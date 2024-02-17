using System.ComponentModel.DataAnnotations;
using System.Diagnostics.CodeAnalysis;
using Avalonia.Controls;
using Avalonia.Metadata;

namespace client.Models.Settings;

[SuppressMessage("ReSharper", "InconsistentNaming")]
public struct Struct
{
    /// <summary>
    /// The position of the window (on the X axis).
    /// </summary>
    [Setting(NotForManualEditing = true)]
    int windowX = 50;

    /// <summary>
    /// The position of the window (on the Y axis).
    /// </summary>
    [Setting(NotForManualEditing = true)]
    int windowY = 50;

    /// <summary>
    /// The saved width of the window.
    /// </summary>
    [Setting(NotForManualEditing = true)]
    int windowWidth = 1765;

    /// <summary>
    /// The saved height of the window.
    /// </summary>
    [Setting(NotForManualEditing = true)]
    int windowHeight = 630;

    /// <summary>
    /// Whether the Milestones Reminder overlay is enabled.
    /// </summary>
    /// <remarks>
    /// This overlay can show notifications for various game events, global champs
    /// hitting 6, hyper-scalers hitting specific breakpoints, specific item
    /// purchases (anti-heal, QSS, etc as well as specific-to-you items like Banshees
    /// vs Nocturne, etc), Smite level ups, Support item level ups, and trinket
    /// changes.
    /// </remarks>
    /// <default>false</default>
    [Setting(
        Prompt = "Game Milestones Notifications",
        Description = "Show game milestones, such as: Global Ultimate champions hit "
            + "level 6, Specific item purchases, Smite level ups and more.",
        Group = SettingGroup.Overlays,
        Type = SettingType.Overlay,
        DefaultValue = 0
    )]
    bool overlayMilestones = false;

    /// <summary>
    /// Whether the CS overlay is enabled.
    /// </summary>
    /// <remarks>
    /// This overlay can show multiple tools related to CS tracking: a graph of per
    /// minute values, current per minute value, and both can be compared to a
    /// target rank.
    /// </remarks>
    /// <default>true</default>
    [Setting(
        Prompt = "CS Tracker",
        Description = "Show CS tracker and comparison tool.",
        Group = SettingGroup.Overlays,
        Type = SettingType.Overlay,
        DefaultValue = 1
    )]
    bool overlayCSTracker = true;

    /// <summary>
    /// Whether the Objective Reminder overlay is enabled.
    /// </summary>
    /// <remarks>
    /// This overlay shows reminder notifications, and 45 second countdowns for
    /// various objective events.
    /// </remarks>
    /// <default>false</default>
    [Setting(
        Prompt = "Objective Reminders",
        Description = "Show objective reminders, such as: Turret plates, Rift/Baron "
            + "spawning, Dragon and Baron spawns, and more.",
        Group = SettingGroup.Overlays,
        Type = SettingType.Overlay,
        DefaultValue = 0
    )]
    bool overlayObjectives = false;

    /// <summary>
    /// Whether the Spell Tracker Reminder overlay is enabled.
    /// </summary>
    /// <remarks>
    /// This overlay shows a display of enemy champions and their spells, which can be
    /// clicked to start a timer for the cooldown.
    /// </remarks>
    /// <default>true</default>
    [Setting(
        Prompt = "Spell Tracker",
        Description = "Show a Spell-Cooldown tracker for enemy champions.",
        Group = SettingGroup.Overlays,
        Type = SettingType.Overlay,
        DefaultValue = 1
    )]
    bool overlaySpellTracker = true;

    /// <summary>
    /// Whether the Jungle Timers Map overlay is enabled.
    /// </summary>
    /// <remarks>
    /// This overlay shows timers for the jungle camps, if they are known to be dead.
    /// </remarks>
    /// <default>true</default>
    [Setting(
        Prompt = "Jungle Timers",
        Description = "Show Jungle Timers over the map.",
        Group = SettingGroup.Overlays,
        Type = SettingType.Overlay,
        DefaultValue = 1
    )]
    bool overlayJungleTimers = true;

    /// <summary>
    /// Whether the ARAM Health Map overlay is enabled.
    /// </summary>
    /// <remarks>
    /// This overlay shows timers for the ARAM health packs.
    /// </remarks>
    /// <default>true</default>
    [Setting(
        Prompt = "ARAM Health Pack Timers",
        Description = "Show ARAM Health Pack timers over the map.",
        Group = SettingGroup.Overlays,
        Type = SettingType.Overlay,
        DefaultValue = 1
    )]
    bool overlayARAMHealth = true;

    /// <summary>
    /// Whether the Duos Scoreboard overlay is enabled.
    /// </summary>
    /// <remarks>
    /// This overlay shows color-matched dots on the scoreboard to show players who
    /// are queueing together.
    /// </remarks>
    /// <default>true</default>
    [Setting(
        Prompt = "Scoreboard Duos",
        Description = "Show indicators on the scoreboard to show players who are "
            + "queueing together.",
        Group = SettingGroup.Overlays,
        Type = SettingType.Overlay,
        DefaultValue = 1
    )]
    bool overlayDuosDisplay = true;

    /// <summary>
    /// Whether the Gold Difference Scoreboard overlay is enabled.
    /// </summary>
    /// <remarks>
    /// This overlay shows the gold difference between purchased items directly
    /// across on the scoreboard.
    /// </remarks>
    /// <default>true</default>
    [Setting(
        Prompt = "Scoreboard Gold Difference",
        Description = "Show the gold difference of purchased items between "
            + "individual players and teams as a whole.",
        Group = SettingGroup.Overlays,
        Type = SettingType.Overlay,
        DefaultValue = 1
    )]
    bool overlayGoldDiff = true;

    /// <summary>
    /// Whether the Map Check Reminder overlay is enabled.
    /// </summary>
    /// <remarks>
    /// This overlay gives a reminder visually and/or audibly to check the map at a
    /// specified interval.
    /// </remarks>
    /// <default>false</default>
    [Setting(
        Prompt = "Map Check Reminder",
        Description = "Gives reminders to check the map at a specified interval.",
        Group = SettingGroup.Overlays,
        Type = SettingType.Overlay,
        DefaultValue = 0
    )]
    bool overlayMapCheck = false;

    /// <summary>
    /// Whether the Back Reminder overlay is enabled.
    /// </summary>
    /// <remarks>
    /// This overlay gives a reminder visually and/or audibly to consider backing.
    /// </remarks>
    /// <default>false</default>
    [Setting(
        Prompt = "Back Reminder",
        Description = "Gives reminders to consider backing at a specified interval.",
        Group = SettingGroup.Overlays,
        Type = SettingType.Overlay,
        DefaultValue = 0
    )]
    bool overlayBackReminder = false;

    /// <summary>
    /// Whether the Use-Trinket Reminder overlay is enabled.
    /// </summary>
    /// <remarks>
    /// This overlay gives a reminder visually to use your trinket at a specified
    /// interval.
    /// </remarks>
    /// <default>true</default>
    [Setting(
        Prompt = "Use-Trinket Reminder",
        Description = "Gives reminders to use your trinket at a specified interval.",
        Group = SettingGroup.Overlays,
        Type = SettingType.Overlay,
        DefaultValue = 1
    )]
    bool overlayUseTrinket = true;

    /// <summary>
    /// Whether the Counter Items Shop overlay is enabled.
    /// </summary>
    /// <remarks>
    /// This overlay adds a couple Counter item suggestions to the shop.
    /// </remarks>
    /// <default>true</default>
    [Setting(
        Prompt = "Counter Item Suggestions",
        Description = "Adds some Counter item suggestions to the shop.",
        Group = SettingGroup.Overlays,
        Type = SettingType.Overlay,
        DefaultValue = 1
    )]
    bool overlayCounterBuild = true;

    /// <summary>
    /// Whether the program should launch on startup.
    /// </summary>
    /// <default>false</default>
    [Setting(
        Prompt = "Launch on Startup",
        Description = "Start the program when you log in to your computer.",
        Group = SettingGroup.AppBehavior,
        Type = SettingType.Checkbox,
        DefaultValue = 0
    )]
    bool launchOnStartup = false;

    /// <summary>
    /// Whether the program should close to the system tray instead of actually
    /// closing.
    /// </summary>
    /// <default>false</default>
    [Setting(
        Prompt = "Close to System Tray",
        Description = "Close the program to the system tray instead of actually "
            + "closing - leaving the program running in the background in an even "
            + "lighter state.",
        Group = SettingGroup.AppBehavior,
        Type = SettingType.Checkbox,
        DefaultValue = 0
    )]
    bool closeToTray = false;

    /// <summary>
    /// Whether the program should always be on top of other windows.
    /// </summary>
    /// <default>false</default>
    [Setting(
        Prompt = "Always on Top",
        Description = "When the program opens new windows, they will always be on top "
            + "of other windows.",
        Group = SettingGroup.AppBehavior,
        Type = SettingType.Checkbox,
        DefaultValue = 0
    )]
    bool bringToFront = false;

    /// <summary>
    /// Whether the program should save the position of the window.
    /// </summary>
    /// <default>true</default>
    [Setting(
        Prompt = "Save Window Position",
        Description = "When the program closes, it will remember the position of the "
            + "window and open in the same position next time.",
        Group = SettingGroup.AppBehavior,
        Type = SettingType.Checkbox,
        DefaultValue = 1
    )]
    bool saveWindowPosition = true;

    /// <summary>
    /// How many matches should be loaded and shown on the match history screen.
    /// </summary>
    /// <default>30</default>
    [Setting(
        Prompt = "Match History Count",
        Description = "How many matches should be loaded and shown on the match "
            + "history screen.",
        Group = SettingGroup.AppBehavior,
        Type = SettingType.Slider,
        DefaultValue = 30
    )]
    int matchHistoryCount = 30;

    /// <summary>
    /// How many matches should be maintained in the background.
    /// </summary>
    /// <remarks>
    /// This controls how many matches are downloaded in the background (when not in
    /// a game and not actively using the app), an th maximum to keep downloaded.
    /// These games won't be shown in Match History, but they will be cached for if
    /// you navigate to them in another way (eg, a less-active friend has your 31st
    /// game as their most recent), and the data from these matches will also be used
    /// for Players Played With statistics and similar.
    /// </remarks>
    /// <default>150</default>
    [Setting(
        Prompt = "Background Match Count",
        Description = "How many matches should be maintained in the background as "
            + "fully cached matches.",
        Group = SettingGroup.AppBehavior,
        Type = SettingType.Slider,
        DefaultValue = 150
    )]
    int backgroundMatchesToLoad = 150;

    /// <summary>
    /// Similar to <see cref="backgroundMatchesToLoad"/>, but it is only rough match
    /// data (e.g. win/loss and champion played), for Champion Pool data.
    /// </summary>
    /// <default>250</default>
    [Setting(
        Prompt = "Background Rough Match Count",
        Description = "How many matches should be maintained in the background, but "
            + "it's only rough match data (e.g. win/loss and champion played).",
        Group = SettingGroup.AppBehavior,
        Type = SettingType.Slider,
        DefaultValue = 250
    )]
    int backgroundRoughMatchesToLoad = 250;

    /// <summary>
    /// The threshold to initially distinguish between a player that happened to be
    /// in multiple games with you and a friend in a row.
    /// </summary>
    /// <default>3</default>
    [Setting(
        Prompt = "Number of Games in a Row to consider a Player a Friend",
        Description = "The threshold of games in a row to initially distinguish "
            + "between a player that happened to be in multiple games with "
            + "you and a friend.",
        Group = SettingGroup.AppBehavior,
        Type = SettingType.Slider,
        DefaultValue = 3
    )]
    int thresholdInARowForPlayerFriend = 3;

    /// <summary>
    /// Similar to <see cref="thresholdInARowForPlayerFriend"/>, but for the total
    /// games in history, included background history, to count a plyer as a friend.
    /// </summary>
    /// <default>7</default>
    [Setting(
        Prompt = "Total Number of Games in history to consider a Player a Friend",
        Description = "The threshold of total games in history, included background "
            + "history, to count a player as a friend.",
        Group = SettingGroup.AppBehavior,
        Type = SettingType.Slider,
        DefaultValue = 7
    )]
    int thresholdForPlayerFriend = 7;

    bool showMyRank = true;
    bool showAllyRank = true;
    bool showEnemyRank = true;
    bool showGameRanks = true;

    bool showCurrentSession = false;
    bool showPreGameSeparate = false;
    bool autoClosePreGame = false;

    /// <summary>
    /// Whether new League accounts should automatically be detected from the League
    /// client and be added to the program and switch to them.
    /// </summary>
    /// <default>true</default>
    [Setting(
        Prompt = "Detect New Accounts",
        Description = "Automatically detect new League accounts from the League client "
            + "and add them to the program and switch to them.",
        Group = SettingGroup.AccountManagement,
        Type = SettingType.Checkbox,
        DefaultValue = 1
    )]
    bool detectNewAccounts = true;

    public Struct() { }
}
