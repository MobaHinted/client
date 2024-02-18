// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using System.ComponentModel;
using client.Models.Data;

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
        {
            throw new ArgumentException(
                    "The new Value of the Setting must be provided."
                );
        }

        // Save the values I need from the event
        string setting = args.PropertyName!;
        object value = args.NewValue;

        Dictionary<string, string>? settings;

        // Load the settings dictionary from the disk
        if (FileManagement.fileHasContent(Constants.settingsFile))
        {
            FileManagement.loadFromFile(
                    Constants.settingsFile,
                    out settings
                );
        }
        else
        {
            // If the file does not exist, create the dictionary
            settings = new Dictionary<string, string>();
        }

        // Update the dictionary with the new value
        settings![setting] = value.ToString()!;

        // Save the dictionary to the disk
        FileManagement.saveToFile(
                Constants.settingsFile,
                settings
            );
    }
}
