namespace client.Models.Settings;

public enum SettingType
{
  // Generics

  Checkbox,
  Slider,
  Custom,

  // Specifics

  Overlay,
  Account,
}

public enum SettingGroup
{
  Overlays,
  AppBehavior,
  AccountManagement,
  Privacy,
}

public class Setting: Attribute
{
  public bool NotForManualEditing { get; set; } = false;

  public string? Prompt { get; set; }
  public string? Description { get; set; }
  public SettingGroup Group { get; set; }

  public SettingType Type { get; set; }

  public string? DependsOn { get; set; }

  public int DefaultValue { get; set; } = -1;

  public int SliderMin { get; set; } = -1;
  public int SliderMax { get; set; } = -1;
  public int SliderStep { get; set; } = -1;
}
