using System.ComponentModel;
using System.Text.Json;

namespace client.Models.Settings;

public class SettingsManager
{
    public SettingsManager()
    {
        Program.Settings.PropertyChanged += settingChanged!;
    }

    private void settingChanged(object sender, PropertyChangedEventArgs e)
    {
        // Just ensuring the value is being passed along correctly
        if (e is not PropertyChangedEventArgsWithValue args)
            throw new ArgumentException("The new Value of the Setting must be provided.");

        // Save the values I need from the event
        string setting = args.PropertyName!;
        object value = args.NewValue;

        Console.WriteLine("Setting changed: " + setting + " to:");
        string jsonString = JsonSerializer.Serialize(setting);
        Console.WriteLine(jsonString);
        jsonString = JsonSerializer.Serialize(value);
        Console.WriteLine(jsonString);

        // TODO: Save the setting to disk
    }
}
