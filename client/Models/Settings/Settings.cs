// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using System.ComponentModel;
using System.Diagnostics.CodeAnalysis;
using System.Reflection;
using System.Runtime.CompilerServices;
using client.Models.Accounts;
using client.Models.Data;

namespace client.Models.Settings;

/// <summary>
///     An override to pass along the new value of a setting when it changes.
/// </summary>
/// <param name="propertyName">The name of the setting changing</param>
/// <param name="newValue">The new value of the changing setting</param>
public class PropertyChangedEventArgsWithValue(string propertyName, object newValue)
    : PropertyChangedEventArgs(propertyName)
{
    public object NewValue { get; } = newValue;
}

/// <summary>
///     A structure for storing settings.
/// </summary>
/// <remarks>
///     TODO: I think this should be changed to be auto-generated.
/// </remarks>
/// <seealso cref="SettingsManager" />
[SuppressMessage(
        "ReSharper",
        "InconsistentNaming"
    )]
[SuppressMessage(
        "Usage",
        "CA2211:Non-constant fields should not be visible"
    )]
public class Settings : INotifyPropertyChanged
{
    /// <summary>
    ///     Setting changed event.
    /// </summary>
    /// <seealso cref="OnPropertyChanged" />
    /// <seealso cref="SettingsManager.settingChanged" />
    public event PropertyChangedEventHandler? PropertyChanged;

    /// <summary>
    ///     Event invoker for <see cref="PropertyChanged" />.
    /// </summary>
    /// <param name="propertyName">The changed setting</param>
    /// <param name="newValue">The new value of the setting</param>
    private void OnPropertyChanged(string propertyName, object newValue)
    {
        PropertyChanged?.Invoke(
                this,
                new PropertyChangedEventArgsWithValue(
                        propertyName,
                        newValue
                    )
            );
    }

    /// <summary>
    ///     The setter for a property, which also invokes
    ///     <see cref="OnPropertyChanged" />.
    /// </summary>
    /// <param name="storage">The backing field for the given Setting</param>
    /// <param name="value">The 'new' value</param>
    /// <param name="propertyName">The name of the property to update</param>
    /// <returns>Whether the setting actually changed with the 'new' value</returns>
    private void SetProperty<T>(
        ref T storage,
        T value,
        [CallerMemberName] string propertyName = ""
    )
    {
        if (EqualityComparer<T>.Default.Equals(
                    storage,
                    value
                ))
            return;

        storage = value;
        OnPropertyChanged(
                propertyName,
                value!
            );
    }

    public void load()
    {
        // Verify the file has any content
        if (!FileManagement.fileHasContent(Constants.settingsFile))
            return;

        // Verify the file can be loaded
        FileManagement.loadFromFile(
                Constants.settingsFile,
                out Dictionary<string, string>? settings
            );
        if (settings is null)
            return;

        Console.WriteLine("Loading settings from file...");

        // Load the settings dictionary from the file
        foreach (var setting in settings)
        {
            // Get the property from this class
            FieldInfo? field = typeof(Settings).GetField(
                    setting.Key,
                    BindingFlags.NonPublic | BindingFlags.Instance
                );

            // Set the field
            if (field?.FieldType == typeof(Guid?))
            {
                this._activeAccount = Guid.Parse(setting.Value);
                Program.Account = new Account((Guid)this._activeAccount);
            }
            else
            {
                field!.SetValue(
                        this,
                        Convert.ChangeType(
                                setting.Value,
                                field.FieldType
                            )
                    );
            }

            Console.WriteLine($"...Loaded setting: {setting.Key} = {setting.Value}");
        }
    }

    #region Non-User-Editable Settings

    #region WindowX

    private int _windowX = 50;

    /// <summary>
    ///     The position of the window (on the X axis).
    /// </summary>
    [SettingDisplay(NotForManualEditing = true)]
    public int windowX
    {
        get => this._windowX;
        set =>
            SetProperty(
                    ref this._windowX,
                    value,
                    nameof(this._windowX)
                );
    }

    #endregion

    #region WindowY

    private int _windowY = 50;

    /// <summary>
    ///     The position of the window (on the Y axis).
    /// </summary>
    [SettingDisplay(NotForManualEditing = true)]
    public int windowY
    {
        get => this._windowY;
        set =>
            SetProperty(
                    ref this._windowY,
                    value,
                    nameof(this._windowY)
                );
    }

    #endregion

    #region WindowWidth

    private int _windowWidth = 1765;

    /// <summary>
    ///     The saved width of the window.
    /// </summary>
    [SettingDisplay(NotForManualEditing = true)]
    public int windowWidth
    {
        get => this._windowWidth;
        set =>
            SetProperty(
                    ref this._windowWidth,
                    value,
                    nameof(this._windowWidth)
                );
    }

    #endregion

    #region WindowHeight

    private int _windowHeight = 630;

    /// <summary>
    ///     The saved height of the window.
    /// </summary>
    [SettingDisplay(NotForManualEditing = true)]
    public int windowHeight
    {
        get => this._windowHeight;
        set =>
            SetProperty(
                    ref this._windowHeight,
                    value,
                    nameof(this._windowHeight)
                );
    }

    #endregion

    #endregion

    #region Overlay Settings

    #region OverlayMilestones

    private bool _overlayMilestones;

    /// <summary>
    ///     Whether the Milestones Reminder overlay is enabled.
    /// </summary>
    /// <remarks>
    ///     This overlay can show notifications for various game events, global champs
    ///     hitting 6, hyper-scalers hitting specific breakpoints, specific item
    ///     purchases (anti-heal, QSS, etc as well as specific-to-you items like Banshees
    ///     vs Nocturne, etc), Smite level ups, Support item level ups, and trinket
    ///     changes.
    /// </remarks>
    /// <default>false</default>
    [SettingDisplay(
            Prompt = "Game Milestones Notifications",
            Description =
                "Show game milestones, such as: Global Ultimate champions hit "
                + "level 6, Specific item purchases, Smite level ups and more.",
            Group = SettingGroup.overlays,
            Type = SettingType.overlay,
            DefaultValue = 0
        )]
    public bool overlayMilestones
    {
        get => this._overlayMilestones;
        set =>
            SetProperty(
                    ref this._overlayMilestones,
                    value,
                    nameof(this._overlayMilestones)
                );
    }

    #endregion

    #region OverlayCSTracker

    private bool _overlayCSTracker = true;

    /// <summary>
    ///     Whether the CS overlay is enabled.
    /// </summary>
    /// <remarks>
    ///     This overlay can show multiple tools related to CS tracking: a graph of per
    ///     minute values, current per minute value, and both can be compared to a
    ///     target rank.
    /// </remarks>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "CS Tracker",
            Description = "Show CS tracker and comparison tool.",
            Group = SettingGroup.overlays,
            Type = SettingType.overlay,
            DefaultValue = 1
        )]
    public bool overlayCSTracker
    {
        get => this._overlayCSTracker;
        set =>
            SetProperty(
                    ref this._overlayCSTracker,
                    value,
                    nameof(this._overlayCSTracker)
                );
    }

    #endregion

    #region OverlayObjectives

    private bool _overlayObjectives;

    /// <summary>
    ///     Whether the Objective Reminder overlay is enabled.
    /// </summary>
    /// <remarks>
    ///     This overlay shows reminder notifications, and 45 second countdowns for
    ///     various objective events.
    /// </remarks>
    /// <default>false</default>
    [SettingDisplay(
            Prompt = "Objective Reminders",
            Description =
                "Show objective reminders, such as: Turret plates, Rift/Baron "
                + "spawning, Dragon and Baron spawns, and more.",
            Group = SettingGroup.overlays,
            Type = SettingType.overlay,
            DefaultValue = 0
        )]
    public bool overlayObjectives
    {
        get => this._overlayObjectives;
        set =>
            SetProperty(
                    ref this._overlayObjectives,
                    value,
                    nameof(this._overlayObjectives)
                );
    }

    #endregion

    #region OverlaySpellTracker

    private bool _overlaySpellTracker = true;

    /// <summary>
    ///     Whether the Spell Tracker Reminder overlay is enabled.
    /// </summary>
    /// <remarks>
    ///     This overlay shows a display of enemy champions and their spells, which can be
    ///     clicked to start a timer for the cooldown.
    /// </remarks>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "Spell Tracker",
            Description = "Show a Spell-Cooldown tracker for enemy champions.",
            Group = SettingGroup.overlays,
            Type = SettingType.overlay,
            DefaultValue = 1
        )]
    public bool overlaySpellTracker
    {
        get => this._overlaySpellTracker;
        set =>
            SetProperty(
                    ref this._overlaySpellTracker,
                    value,
                    nameof(this._overlaySpellTracker)
                );
    }

    #endregion

    #region OverlayJungleTimers

    private bool _overlayJungleTimers = true;

    /// <summary>
    ///     Whether the Jungle Timers Map overlay is enabled.
    /// </summary>
    /// <remarks>
    ///     This overlay shows timers for the jungle camps, if they are known to be dead.
    /// </remarks>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "Jungle Timers",
            Description = "Show Jungle Timers over the map.",
            Group = SettingGroup.overlays,
            Type = SettingType.overlay,
            DefaultValue = 1
        )]
    public bool overlayJungleTimers
    {
        get => this._overlayJungleTimers;
        set =>
            SetProperty(
                    ref this._overlayJungleTimers,
                    value,
                    nameof(this._overlayJungleTimers)
                );
    }

    #endregion

    #region OverlayARAMHealth

    private bool _overlayARAMHealth = true;

    /// <summary>
    ///     Whether the ARAM Health Map overlay is enabled.
    /// </summary>
    /// <remarks>
    ///     This overlay shows timers for the ARAM health packs.
    /// </remarks>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "ARAM Health Pack Timers",
            Description = "Show ARAM Health Pack timers over the map.",
            Group = SettingGroup.overlays,
            Type = SettingType.overlay,
            DefaultValue = 1
        )]
    public bool overlayARAMHealth
    {
        get => this._overlayARAMHealth;
        set =>
            SetProperty(
                    ref this._overlayARAMHealth,
                    value,
                    nameof(this._overlayARAMHealth)
                );
    }

    #endregion

    #region OverlayDuosDisplay

    private bool _overlayDuosDisplay = true;

    /// <summary>
    ///     Whether the Duos Scoreboard overlay is enabled.
    /// </summary>
    /// <remarks>
    ///     This overlay shows color-matched dots on the scoreboard to show players who
    ///     are queueing together.
    /// </remarks>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "Scoreboard Duos",
            Description =
                "Show indicators on the scoreboard to show players who are "
                + "queueing together.",
            Group = SettingGroup.overlays,
            Type = SettingType.overlay,
            DefaultValue = 1
        )]
    public bool overlayDuosDisplay
    {
        get => this._overlayDuosDisplay;
        set =>
            SetProperty(
                    ref this._overlayDuosDisplay,
                    value,
                    nameof(this._overlayDuosDisplay)
                );
    }

    #endregion

    #region OverlayGoldDiff

    private bool _overlayGoldDiff = true;

    /// <summary>
    ///     Whether the Gold Difference Scoreboard overlay is enabled.
    /// </summary>
    /// <remarks>
    ///     This overlay shows the gold difference between purchased items directly
    ///     across on the scoreboard.
    /// </remarks>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "Scoreboard Gold Difference",
            Description =
                "Show the gold difference of purchased items between "
                + "individual players and teams as a whole.",
            Group = SettingGroup.overlays,
            Type = SettingType.overlay,
            DefaultValue = 1
        )]
    public bool overlayGoldDiff
    {
        get => this._overlayGoldDiff;
        set =>
            SetProperty(
                    ref this._overlayGoldDiff,
                    value,
                    nameof(this._overlayGoldDiff)
                );
    }

    #endregion

    #region OverlayMapCheck

    private bool _overlayMapCheck;

    /// <summary>
    ///     Whether the Map Check Reminder overlay is enabled.
    /// </summary>
    /// <remarks>
    ///     This overlay gives a reminder visually and/or audibly to check the map at a
    ///     specified interval.
    /// </remarks>
    /// <default>false</default>
    [SettingDisplay(
            Prompt = "Map Check Reminder",
            Description =
                "Gives reminders to check the map at a specified interval.",
            Group = SettingGroup.overlays,
            Type = SettingType.overlay,
            DefaultValue = 0
        )]
    public bool overlayMapCheck
    {
        get => this._overlayMapCheck;
        set =>
            SetProperty(
                    ref this._overlayMapCheck,
                    value,
                    nameof(this._overlayMapCheck)
                );
    }

    #endregion

    #region OverlayBackReminder

    private bool _overlayBackReminder;

    /// <summary>
    ///     Whether the Back Reminder overlay is enabled.
    /// </summary>
    /// <remarks>
    ///     This overlay gives a reminder visually and/or audibly to consider backing.
    /// </remarks>
    /// <default>false</default>
    [SettingDisplay(
            Prompt = "Back Reminder",
            Description =
                "Gives reminders to consider backing at a specified interval.",
            Group = SettingGroup.overlays,
            Type = SettingType.overlay,
            DefaultValue = 0
        )]
    public bool overlayBackReminder
    {
        get => this._overlayBackReminder;
        set =>
            SetProperty(
                    ref this._overlayBackReminder,
                    value,
                    nameof(this._overlayBackReminder)
                );
    }

    #endregion

    #region OverlayUseTrinket

    private bool _overlayUseTrinket = true;

    /// <summary>
    ///     Whether the Use-Trinket Reminder overlay is enabled.
    /// </summary>
    /// <remarks>
    ///     This overlay gives a reminder visually to use your trinket at a specified
    ///     interval.
    /// </remarks>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "Use-Trinket Reminder",
            Description =
                "Gives reminders to use your trinket at a specified interval.",
            Group = SettingGroup.overlays,
            Type = SettingType.overlay,
            DefaultValue = 1
        )]
    public bool overlayUseTrinket
    {
        get => this._overlayUseTrinket;
        set =>
            SetProperty(
                    ref this._overlayUseTrinket,
                    value,
                    nameof(this._overlayUseTrinket)
                );
    }

    #endregion

    #region OverlayCounterBuild

    private bool _overlayCounterBuild = true;

    /// <summary>
    ///     Whether the Counter Items Shop overlay is enabled.
    /// </summary>
    /// <remarks>
    ///     This overlay adds a couple Counter item suggestions to the shop.
    /// </remarks>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "Counter Item Suggestions",
            Description = "Adds some Counter item suggestions to the shop.",
            Group = SettingGroup.overlays,
            Type = SettingType.overlay,
            DefaultValue = 1
        )]
    public bool overlayCounterBuild
    {
        get => this._overlayCounterBuild;
        set =>
            SetProperty(
                    ref this._overlayCounterBuild,
                    value,
                    nameof(this._overlayCounterBuild)
                );
    }

    #endregion

    #endregion

    #region App Behavior Settings

    #region LaunchOnStartup

    private bool _launchOnStartup;

    /// <summary>
    ///     Whether the program should launch on startup.
    /// </summary>
    /// <default>false</default>
    [SettingDisplay(
            Prompt = "Launch on Startup",
            Description = "Start the program when you log in to your computer.",
            Group = SettingGroup.appBehavior,
            Type = SettingType.checkbox,
            DefaultValue = 0
        )]
    public bool launchOnStartup
    {
        get => this._launchOnStartup;
        set =>
            SetProperty(
                    ref this._launchOnStartup,
                    value,
                    nameof(this._launchOnStartup)
                );
    }

    #endregion

    #region CloseToTray

    private bool _closeToTray = true;

    /// <summary>
    ///     Whether the program should close to the system tray instead of actually
    ///     closing.
    /// </summary>
    /// <default>false</default>
    [SettingDisplay(
            Prompt = "Close to System Tray",
            Description = "Close the program to the system tray instead of actually "
                + "closing - leaving the program running in the background in an even "
                + "lighter state.",
            Group = SettingGroup.appBehavior,
            Type = SettingType.checkbox,
            DefaultValue = 0
        )]
    public bool closeToTray
    {
        get => this._closeToTray;
        set =>
            SetProperty(
                    ref this._closeToTray,
                    value,
                    nameof(this._closeToTray)
                );
    }

    #endregion

    #region BringToFront

    private bool _bringToFront;

    /// <summary>
    ///     Whether the program should always be on top of other windows.
    /// </summary>
    /// <default>false</default>
    [SettingDisplay(
            Prompt = "Bring Windows to Front",
            Description =
                "When the program opens new windows, they will open on top of "
                + "other programs.",
            Group = SettingGroup.appBehavior,
            Type = SettingType.checkbox,
            DefaultValue = 0
        )]
    public bool bringToFront
    {
        get => this._bringToFront;
        set =>
            SetProperty(
                    ref this._bringToFront,
                    value,
                    nameof(this._bringToFront)
                );
    }

    #endregion

    #region SaveWindowPosition

    private bool _saveWindowPosition = true;

    /// <summary>
    ///     Whether the program should save the position of the window.
    /// </summary>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "Save Window Position",
            Description =
                "When the program closes, it will remember the position of the "
                + "window and open in the same position next time.",
            Group = SettingGroup.appBehavior,
            Type = SettingType.checkbox,
            DefaultValue = 1
        )]
    public bool saveWindowPosition
    {
        get => this._saveWindowPosition;
        set =>
            SetProperty(
                    ref this._saveWindowPosition,
                    value,
                    nameof(this._saveWindowPosition)
                );
    }

    #endregion

    #region MatchHistoryCount

    private int _matchHistoryCount = 30;

    /// <summary>
    ///     How many matches should be loaded and shown on the match history screen.
    /// </summary>
    /// <default>30</default>
    [SettingDisplay(
            Prompt = "Match History Count",
            Description =
                "How many matches should be loaded and shown on the match "
                + "history screen.",
            Group = SettingGroup.appBehavior,
            Type = SettingType.slider,
            DefaultValue = 30,
            SliderMin = 10,
            SliderMax = 300,
            SliderStep = 10
        )]
    public int matchHistoryCount
    {
        get => this._matchHistoryCount;
        set =>
            SetProperty(
                    ref this._matchHistoryCount,
                    value,
                    nameof(this._matchHistoryCount)
                );
    }

    #endregion

    #region BackgroundMatchesToLoad

    private int _backgroundMatchesToLoad = 150;

    /// <summary>
    ///     How many matches should be maintained in the background.
    /// </summary>
    /// <remarks>
    ///     This controls how many matches are downloaded in the background (when not in
    ///     a game and not actively using the app), an th maximum to keep downloaded.
    ///     These games won't be shown in Match History, but they will be cached for if
    ///     you navigate to them in another way (eg, a less-active friend has your 31st
    ///     game as their most recent), and the data from these matches will also be used
    ///     for Players Played With statistics and similar.
    /// </remarks>
    /// <default>150</default>
    [SettingDisplay(
            Prompt = "Background Match Count",
            Description =
                "How many matches should be maintained in the background as "
                + "fully cached matches.",
            Group = SettingGroup.appBehavior,
            Type = SettingType.slider,
            DefaultValue = 150,
            SliderMin = 50,
            SliderMax = 500,
            SliderStep = 50
        )]
    public int backgroundMatchesToLoad
    {
        get => this._backgroundMatchesToLoad;
        set =>
            SetProperty(
                    ref this._backgroundMatchesToLoad,
                    value,
                    nameof(this._backgroundMatchesToLoad)
                );
    }

    #endregion

    #region BackgroundRoughMatchesToLoad

    private int _backgroundRoughMatchesToLoad = 300;

    /// <summary>
    ///     Similar to <see cref="backgroundMatchesToLoad" />, but it is only rough match
    ///     data (e.g. win/loss and champion played), for Champion Pool data.
    /// </summary>
    /// <default>250</default>
    [SettingDisplay(
            Prompt = "Background Rough Match Count",
            Description =
                "How many matches should be maintained in the background, but "
                + "it's only rough match data (e.g. win/loss and champion "
                + "played).",
            Group = SettingGroup.appBehavior,
            Type = SettingType.slider,
            DefaultValue = 250,
            SliderMin = 100,
            SliderMax = 1000,
            SliderStep = 100
        )]
    public int backgroundRoughMatchesToLoad
    {
        get => this._backgroundRoughMatchesToLoad;
        set =>
            SetProperty(
                    ref this._backgroundRoughMatchesToLoad,
                    value,
                    nameof(this._backgroundRoughMatchesToLoad)
                );
    }

    #endregion

    #region ThresholdInARowForPlayerFriend

    private int _thresholdInARowForPlayerFriend = 3;

    /// <summary>
    ///     The threshold to initially distinguish between a player that happened to be
    ///     in multiple games with you and a friend in a row.
    /// </summary>
    /// <default>3</default>
    [SettingDisplay(
            Prompt = "Number of Games in a Row to consider a Player a Friend",
            Description = "The threshold of games in a row to initially distinguish "
                + "between a player that happened to be in multiple games with "
                + "you and a friend.",
            Group = SettingGroup.appBehavior,
            Type = SettingType.slider,
            DefaultValue = 3
        )]
    public int thresholdInARowForPlayerFriend
    {
        get => this._thresholdInARowForPlayerFriend;
        set =>
            SetProperty(
                    ref this._thresholdInARowForPlayerFriend,
                    value,
                    nameof(this._thresholdInARowForPlayerFriend)
                );
    }

    #endregion

    #region ThresholdForPlayerFriend

    private int _thresholdForPlayerFriend = 7;

    /// <summary>
    ///     Similar to <see cref="thresholdInARowForPlayerFriend" />, but for the total
    ///     games in history, included background history, to count a plyer as a friend.
    /// </summary>
    /// <default>7</default>
    [SettingDisplay(
            Prompt =
                "Total Number of Games in history to consider a Player a Friend",
            Description =
                "The threshold of total games in history, included background "
                + "history, to count a player as a friend.",
            Group = SettingGroup.appBehavior,
            Type = SettingType.slider,
            DefaultValue = 7
        )]
    public int thresholdForPlayerFriend
    {
        get => this._thresholdForPlayerFriend;
        set =>
            SetProperty(
                    ref this._thresholdForPlayerFriend,
                    value,
                    nameof(this._thresholdForPlayerFriend)
                );
    }

    #endregion

    #region ShowMyRank

    private bool _showMyRank = true;

    /// <summary>
    ///     Whether the user's rank should be shown anywhere in the program.
    /// </summary>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "Show My Rank to Me",
            Description =
                "Show your rank in the program, on match history, your profile"
                + " and pre and post game screens.",
            Group = SettingGroup.privacy,
            Type = SettingType.checkbox,
            DefaultValue = 1
        )]
    public bool showMyRank
    {
        get => this._showMyRank;
        set =>
            SetProperty(
                    ref this._showMyRank,
                    value,
                    nameof(this._showMyRank)
                );
    }

    #endregion

    #region ShowAllyRank

    private bool _showAllyRank = true;

    /// <summary>
    ///     Whether allied player ranks should be shown in the program.
    /// </summary>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "Show Ally Ranks",
            Description =
                "Show the ranks of your allies in the program, on pre and post "
                + "game screens. ",
            Group = SettingGroup.privacy,
            Type = SettingType.checkbox,
            DefaultValue = 1
        )]
    public bool showAllyRank
    {
        get => this._showAllyRank;
        set =>
            SetProperty(
                    ref this._showAllyRank,
                    value,
                    nameof(this._showAllyRank)
                );
    }

    #endregion

    #region ShowEnemyRank

    private bool _showEnemyRank = true;

    /// <summary>
    ///     Whether enemy player ranks should be shown in the program.
    /// </summary>
    /// <remarks>
    ///     Similar to <see cref="showAllyRank" />, but for enemies.
    /// </remarks>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "Show Enemy Ranks",
            Description =
                "Show the ranks of your enemies in the program, on pre and post "
                + "game screens.",
            Group = SettingGroup.privacy,
            Type = SettingType.checkbox,
            DefaultValue = 1
        )]
    public bool showEnemyRank
    {
        get => this._showEnemyRank;
        set =>
            SetProperty(
                    ref this._showEnemyRank,
                    value,
                    nameof(this._showEnemyRank)
                );
    }

    #endregion

    #region ShowGameRanks

    private bool _showGameRanks = true;

    /// <summary>
    ///     Whether Game average ranks will be shown in the program.
    /// </summary>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "Show Game Ranks",
            Description =
                "Show the average ranks of the game in the program, on match "
                + "history, and post game screens.",
            Group = SettingGroup.privacy,
            Type = SettingType.checkbox,
            DefaultValue = 1
        )]
    public bool showGameRanks
    {
        get => this._showGameRanks;
        set =>
            SetProperty(
                    ref this._showGameRanks,
                    value,
                    nameof(this._showGameRanks)
                );
    }

    #endregion

    #region ShowCurrentSession

    private bool _showCurrentSession = true;

    /// <summary>
    ///     Whether the Current Session screen should open automatically, always as a
    ///     separate window, after the first game.
    /// </summary>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "Show the Current Session Window",
            Description =
                "Will open the Current Session window as a this-session match "
                + "history and performance screen, after the first game. Always"
                + " as a separate window.",
            Group = SettingGroup.appBehavior,
            Type = SettingType.checkbox,
            DefaultValue = 1
        )]
    public bool showCurrentSession
    {
        get => this._showCurrentSession;
        set =>
            SetProperty(
                    ref this._showCurrentSession,
                    value,
                    nameof(this._showCurrentSession)
                );
    }

    #endregion

    #region ShowInGameScreen

    private bool _showInGameScreen;

    /// <summary>
    ///     Whether the In-Game screen should open, always as a separate window.
    /// </summary>
    /// <default>false</default>
    [SettingDisplay(
            Prompt = "Show the In-Game Window",
            Description =
                "Will open the In-Game window after the Pre-Game screen, always"
                + " as a separate window, displaying information that overlays"
                + " contain (such as gold differences, but at all times), and "
                + "more",
            Group = SettingGroup.appBehavior,
            Type = SettingType.checkbox,
            DefaultValue = 0
        )]
    public bool showInGameScreen
    {
        get => this._showInGameScreen;
        set =>
            SetProperty(
                    ref this._showInGameScreen,
                    value,
                    nameof(this._showInGameScreen)
                );
    }

    #endregion

    #region AutoCloseInGame

    private bool _autoCloseInGame = true;

    /// <summary>
    ///     Whether the In-Game screen should automatically close once you're out of
    ///     game.
    /// </summary>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "Auto-Close In-Game Window",
            Description =
                "Will automatically close the In-Game window once you're out of"
                + " game.",
            Group = SettingGroup.appBehavior,
            Type = SettingType.checkbox,
            DefaultValue = 1,
            DependsOn = "showInGameScreen"
        )]
    public bool autoCloseInGame
    {
        get => this._autoCloseInGame;
        set =>
            SetProperty(
                    ref this._autoCloseInGame,
                    value,
                    nameof(this._autoCloseInGame)
                );
    }

    #endregion

    #region ShowPreGameSeparate

    private bool _showPreGameSeparate;

    /// <summary>
    ///     Whether the Pre-Game screen should open as a separate window.
    /// </summary>
    /// <default>false</default>
    [SettingDisplay(
            Prompt = "Show the Pre-Game Window",
            Description =
                "Will open the Pre-Game window as a pre-game screen, always as a "
                + "separate window.",
            Group = SettingGroup.appBehavior,
            Type = SettingType.checkbox,
            DefaultValue = 0
        )]
    public bool showPreGameSeparate
    {
        get => this._showPreGameSeparate;
        set =>
            SetProperty(
                    ref this._showPreGameSeparate,
                    value,
                    nameof(this._showPreGameSeparate)
                );
    }

    #endregion

    #region AutoClosePreGame

    private bool _autoClosePreGame = true;

    /// <summary>
    ///     Whether the Pre-Game window should automatically close once you're in game.
    /// </summary>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "Auto-Close Pre-Game Window",
            Description =
                "Will automatically close the Pre-Game window once you're in "
                + "game.",
            Group = SettingGroup.appBehavior,
            Type = SettingType.checkbox,
            DefaultValue = 1,
            DependsOn = "showPreGameSeparate"
        )]
    public bool autoClosePreGame
    {
        get => this._autoClosePreGame;
        set =>
            SetProperty(
                    ref this._autoClosePreGame,
                    value,
                    nameof(this._autoClosePreGame)
                );
    }

    #endregion

    #region ShowBuildsSeparate

    private bool _showBuildsSeparate;

    /// <summary>
    ///     Whether the Build Suggestions element of the Pre-Game screen should be shown
    ///     in a separate window, which auto-closes once you're in game.
    /// </summary>
    /// <default>false</default>
    [SettingDisplay(
            Prompt = "Show Build Suggestions Separately",
            Description =
                "Will show the Build Suggestions element of the Pre-Game window "
                + "in a separate window, which auto-closes once you're in game.",
            Group = SettingGroup.appBehavior,
            Type = SettingType.checkbox,
            DefaultValue = 0,
            DependsOn = "showPreGameSeparate"
        )]
    public bool showBuildsSeparate
    {
        get => this._showBuildsSeparate;
        set =>
            SetProperty(
                    ref this._showBuildsSeparate,
                    value,
                    nameof(this._showBuildsSeparate)
                );
    }

    #endregion

    #endregion

    #region Account Management Settings

    #region DetectNewAccounts

    private bool _detectNewAccounts = true;

    /// <summary>
    ///     Whether Accounts should be detected automatically from the League Client,
    ///     and added to the program and switched to as the active account.
    /// </summary>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "Detect New Accounts",
            Description =
                "Automatically detect new accounts from the League Client, and "
                + "add them to the program and switch to them as the active "
                + "account.",
            Group = SettingGroup.accountManagement,
            Type = SettingType.checkbox,
            DefaultValue = 1
        )]
    public bool detectNewAccounts
    {
        get => this._detectNewAccounts;
        set =>
            SetProperty(
                    ref this._detectNewAccounts,
                    value,
                    nameof(this._detectNewAccounts)
                );
    }

    #endregion

    #region ActiveAccount

    private Guid? _activeAccount;

    /// <summary>
    ///     The active account.
    /// </summary>
    /// <default>null</default>
    [SettingDisplay(
            Prompt = "Active Account",
            Description = "The active account.",
            Group = SettingGroup.accountManagement,
            Type = SettingType.account
        )]
    public Guid? activeAccount
    {
        get => this._activeAccount;
        set =>
            SetProperty(
                    ref this._activeAccount,
                    value,
                    nameof(this._activeAccount)
                );
    }

    #endregion

    #endregion

    #region Privacy Settings

    #region DataPipeline

    private int _dataPipeline = (int)DataPipeline.Proxied;

    /// <summary>
    ///     Which pipeline to use for data.
    /// </summary>
    /// <default>
    ///     <see cref="DataPipeline.Proxied" />
    /// </default>
    /// <seealso cref="DataPipeline" />
    [SettingDisplay(
            Prompt = "Data Pipeline",
            Description = "Which pipeline to use for data.",
            Group = SettingGroup.privacy,
            Type = SettingType.custom,
            DefaultValue = 1
        )]
    public int dataPipeline
    {
        get => this._dataPipeline;
        set =>
            SetProperty(
                    ref this._dataPipeline,
                    value,
                    nameof(this._dataPipeline)
                );
    }

    #endregion

    #region ShareTelemetry

    private bool _shareTelemetry = true;

    /// <summary>
    ///     Whether basic usage data should be shared with the developer.
    /// </summary>
    /// <default>true</default>
    [SettingDisplay(
            Prompt = "Share Telemetry Data",
            Description = "Share basic program usage data with the developer.",
            Group = SettingGroup.privacy,
            Type = SettingType.custom,
            DefaultValue = 1
        )]
    public bool shareTelemetry
    {
        get => this._shareTelemetry;
        set =>
            SetProperty(
                    ref this._shareTelemetry,
                    value,
                    nameof(this._shareTelemetry)
                );
    }

    #endregion

    #endregion
}
