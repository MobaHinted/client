namespace client.Models.Settings;

/// <summary>
/// Data Pipeline to use for requests.
/// </summary>
/// <seealso cref="Struct.dataPipeline"/>
public enum DataPipeline
{
    /// <summary>
    /// A private pipeline that is not proxied but does require a developer key.
    /// </summary>
    Private = 0,

    /// <summary>
    /// The default: a proxied pipeline that does not require a developer key.
    /// Requests are sent through the Mobahinted proxy.
    /// </summary>
    Proxied = 1,
}

/// <summary>
/// Types of controls that Settings can have.
/// </summary>
/// <seealso cref="Setting"/>
/// <seealso cref="client.Models.Settings.Struct"/>
public enum SettingType
{
    #region Generic Types

    /// <summary>
    /// A simple true/false checkbox.
    /// </summary>
    checkbox,

    /// <summary>
    /// A number slider input.
    /// </summary>
    slider,

    /// <summary>
    /// A custom input that will have logic depending on the setting.
    /// </summary>
    custom,

    #endregion

    #region Group-Specific Types

    /// <summary>
    /// A checkbox control, but with a settings button if enable.
    /// </summary>
    overlay,

    /// <summary>
    /// An account selection and management control.
    /// </summary>
    account,

    #endregion
}

/// <summary>
/// Different categories of Settings.
/// </summary>
/// <seealso cref="Setting"/>
/// <seealso cref="client.Models.Settings.Struct"/>
public enum SettingGroup
{
    overlays,
    appBehavior,
    accountManagement,
    privacy,
}

/// <summary>
/// The custom attribute that will be used to fully define Settings and how they
/// should be displayed in the settings window.
/// </summary>
/// <seealso cref="client.Models.Settings.Struct"/>
public class Setting : Attribute
{
    #region Required Attributes

    /// <summary>
    /// The settings as will be displayed in the settings window.
    /// </summary>
    public string Prompt { get; set; } = string.Empty;

    /// <summary>
    /// The description that will be shown if the user hovers over the setting.
    /// </summary>
    public string Description { get; set; } = string.Empty;

    /// <summary>
    /// The group that this setting belongs to.
    /// </summary>
    /// <seealso cref="SettingGroup"/>
    public SettingGroup Group { get; set; }

    /// <summary>
    /// The type of setting control that will be used to display this setting.
    /// </summary>
    /// <seealso cref="SettingType"/>
    public SettingType Type { get; set; }

    #endregion

    #region Optional Attributes

    /// <summary>
    /// If true, this setting is not meant to be manually edited and will not be
    /// displayed in the settings window.
    /// </summary>
    public bool NotForManualEditing { get; set; } = false;

    /// <summary>
    /// The Settings.Struct Field that this setting requires to be enabled.
    /// </summary>
    /// <seealso cref="client.Models.Settings.Struct"/>
    public string? DependsOn { get; set; }

    /// <summary>
    /// The default value of this setting.
    /// </summary>
    public int DefaultValue { get; set; } = -1;

    #endregion

    #region Slider Conrol-specific Attributes

    /// <summary>
    /// The minimum value of a Slider control.
    /// </summary>
    /// <seealso cref="Type"/>
    /// <seealso cref="SettingType.slider"/>
    public int SliderMin { get; set; } = -1;

    /// <summary>
    /// The minimum value of a Slider control.
    /// </summary>
    /// <seealso cref="Type"/>
    /// <seealso cref="SettingType.slider"/>
    public int SliderMax { get; set; } = -1;

    /// <summary>
    /// The step value of a Slider control.
    /// </summary>
    /// <seealso cref="Type"/>
    /// <seealso cref="SettingType.slider"/>
    public int SliderStep { get; set; } = -1;

    #endregion
}
