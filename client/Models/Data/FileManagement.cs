// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using System.Diagnostics.CodeAnalysis;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.IO.Compression;
using System.Text.Json;

#endregion

namespace client.Models.Data;

public static class FileManagement
{
    #region Writing

    public static void SaveToFile<T>(string path, T data)
    {
        string jsonString = JsonSerializer.Serialize(data);
        File.WriteAllText(
                path,
                jsonString
            );
    }

    public static void AppendToFile(string path, string data)
    {
        File.AppendAllText(
                path,
                data
            );
    }

    #endregion

    #region Reading

    public static void LoadFromFile<T>(string path, out T? data)
    {
        if (!FileHasContent(path))
        {
            data = default;
            return;
        }

        string jsonString = File.ReadAllText(path);
        data = JsonSerializer.Deserialize<T>(jsonString);
    }

    #endregion

    #region Compressed File Manipulation

    public static void UnpackFile(string path, string destination)
    {
        ZipFile.ExtractToDirectory(
                path,
                destination
            );
    }

    #endregion

    #region Validation

    public static bool FileExists(string path)
    {
        return File.Exists(path);
    }

    public static bool DirectoryExists(string path)
    {
        return Directory.Exists(path);
    }

    public static bool FileHasContent(string path)
    {
        return FileExists(path) && new FileInfo(path).Length > 5;
    }

    #endregion

    #region Creating

    public static void CreateDirectory(string path)
    {
        Directory.CreateDirectory(path);
    }

    public static void CreateFile(string path)
    {
        File.Create(path).Close();
    }

    #endregion

    #region Deleting

    public static void DeleteFile(string path)
    {
        File.Delete(path);
    }

    public static void DeleteDirectory(string path)
    {
        Directory.Delete(
                path,
                true
            );
    }

    public static void EmptyDirectory(string path)
    {
        var directory = new DirectoryInfo(path);

        foreach (FileInfo file in directory.GetFiles())
        {
            file.Delete();
        }

        foreach (DirectoryInfo subDirectory in directory.GetDirectories())
        {
            subDirectory.Delete(true);
        }
    }

    #endregion

    #region Downloading

    public static void DownloadFile(string url, string path)
    {
        var client = new HttpClient();
        byte[] file = client.GetByteArrayAsync(url).Result;
        File.WriteAllBytes(
                path,
                file
            );
    }

    /// <summary>
    ///     Downloads an image from the internet and saves it to the specified path.
    /// </summary>
    /// <remarks>
    ///     If the image is larger than the specified size, it will be resized.
    /// </remarks>
    /// <!--TODO: Add cross-platform support for image resizing.-->
    /// <param name="url">The image URL to download</param>
    /// <param name="path">The path to save the image to</param>
    /// <param name="size">The size to resize the image to. Defaults to 128(x128)</param>
    [SuppressMessage(
            "Interoperability",
            "CA1416:Validate platform compatibility"
        )]
    public static void DownloadImage(string url, string path, int size = 128)
    {
        string debugPath = path.Split("mobahinted").Length > 1
            ? path.Split("mobahinted")[1]
            : path;
        Program.Log(
                source: nameof(FileManagement),
                method: "downloadImage()",
                doing: "Downloading",
                message: "Image",
                debugSymbols:
                [
                    $"path: {debugPath}",
                    $"size: {size}",
                ],
                url: url,
                logLevel: LogLevel.debug,
                logLocation: LogLocation.download
            );

        // Download the image
        var client = new HttpClient();
        byte[] image = client.GetByteArrayAsync(url).Result;

        using var ms = new MemoryStream(image);
        var originalImage = new Bitmap(ms);

        // If the image dimensions are over 128x128 (or the specified size), resize it
        if (originalImage.Width > size || originalImage.Height > size)
        {
            ResizeImage(
                    ms,
                    path,
                    size
                );
            return;
        }

        // Save the original image
        originalImage.Save(
                path,
                ImageFormat.Png
            );
    }

    #endregion

    #region Image Manipulation

    [SuppressMessage(
            "Interoperability",
            "CA1416:Validate platform compatibility"
        )]
    private static Bitmap ActualResize(Image image, int size)
    {
        var resizedImage = new Bitmap(
                size,
                size
            );

        using Graphics graphics = Graphics.FromImage(resizedImage);
        graphics.InterpolationMode = InterpolationMode.HighQualityBicubic;
        graphics.DrawImage(
                image,
                0,
                0,
                size,
                size
            );

        return resizedImage;
    }

    [SuppressMessage(
            "Interoperability",
            "CA1416:Validate platform compatibility"
        )]
    public static void ResizeImage(string path, int size = 128)
    {
        // Read filepath image into a MemoryStream
        var ms = new MemoryStream(File.ReadAllBytes(path));

        // Resize the image
        ResizeImage(
                ms,
                path,
                size
            );
    }

    [SuppressMessage(
            "Interoperability",
            "CA1416:Validate platform compatibility"
        )]
    public static void ResizeImage(MemoryStream stream, string path, int size = 128)
    {
        // Load the Stream into a Bitmap
        using var originalImage = new Bitmap(stream);
        // Resize the image
        Bitmap resizedImage = ActualResize(
                originalImage,
                size
            );

        // Save the resized image over itself
        resizedImage.Save(
                path,
                ImageFormat.Png
            );
    }

    #endregion
}
