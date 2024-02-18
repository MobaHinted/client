// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using System.Text.Json;

namespace client.Models.Data;

public static class FileManagement
{
    public static void saveToFile<T>(string path, T data)
    {
        string jsonString = JsonSerializer.Serialize(data);
        File.WriteAllText(
                path,
                jsonString
            );
    }

    public static void loadFromFile<T>(string path, out T? data)
    {
        if (!fileHasContent(path))
        {
            data = default;
            return;
        }

        string jsonString = File.ReadAllText(path);
        data = JsonSerializer.Deserialize<T>(jsonString);
    }

    public static bool fileExists(string path)
    {
        return File.Exists(path);
    }

    public static bool directoryExists(string path)
    {
        return Directory.Exists(path);
    }

    public static bool fileHasContent(string path)
    {
        return fileExists(path) && new FileInfo(path).Length > 5;
    }

    public static void createDirectory(string path)
    {
        Directory.CreateDirectory(path);
    }

    public static void createFile(string path)
    {
        File.Create(path).Close();
    }
}
