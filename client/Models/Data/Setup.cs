// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

namespace client.Models.Data;

public static class Setup
{
    private static bool AllFilesExist()
    {
        return FileManagement.FileExists(Constants.usersFile)
            && FileManagement.FileExists(Constants.friendsFile)
            && FileManagement.FileExists(Constants.championRolesDataFile)
            && FileManagement.FileExists(Constants.fullLogFile)
            && FileManagement.FileExists(Constants.warningsPlusLogFile)
            && FileManagement.FileExists(Constants.mainLogFile)
            && FileManagement.FileExists(Constants.downloadLogFile)
            && FileManagement.FileExists(Constants.downloadLogFile)
            && FileManagement.FileExists(Constants.gameFlowLogFile)
            && FileManagement.FileExists(Constants.automationLogFile)
            && FileManagement.FileExists(Constants.overlayLogFile)
            && FileManagement.FileExists(Constants.avaloniaConfigFile)
            && FileManagement.FileExists(Constants.settingsFile);
    }

    private static bool AllDirectoriesExist()
    {
        return FileManagement.DirectoryExists(Constants.mobahinted)
            && FileManagement.DirectoryExists(Constants.assets)
            && FileManagement.DirectoryExists(Constants.data)
            && FileManagement.DirectoryExists(Constants.logs)
            && FileManagement.DirectoryExists(Constants.cachedMatchesFolder)
            && FileManagement.DirectoryExists(Constants.imageCacheFolder)
            && FileManagement.DirectoryExists(Constants.imageCacheDataDragonFolder)
            && FileManagement.DirectoryExists(Constants.imageCacheProfileIconFolder)
            && FileManagement.DirectoryExists(Constants.dataDragonFolder)
            && FileManagement.DirectoryExists(Constants.dataDragonChampionFolder);
    }

    public static bool AllContentExists()
    {
        bool filesExist = AllFilesExist();
        bool directoriesExist = AllDirectoriesExist();

        Program.Log(
                source: nameof(Setup),
                method: "allContentExists()",
                message: "Checking if all necessary files and directories exist...",
                debugSymbols:
                [
                    $"files: {filesExist}",
                    $"directories: {directoriesExist}",
                ],
                logLevel: LogLevel.debug,
                logLocation: LogLocation.verbose
            );

        return filesExist && directoriesExist;
    }

    private static void CreateAllFiles()
    {
        FileManagement.CreateFile(Constants.usersFile);
        FileManagement.CreateFile(Constants.friendsFile);
        FileManagement.CreateFile(Constants.championRolesDataFile);
        FileManagement.CreateFile(Constants.fullLogFile);
        FileManagement.CreateFile(Constants.warningsPlusLogFile);
        FileManagement.CreateFile(Constants.mainLogFile);
        FileManagement.CreateFile(Constants.downloadLogFile);
        FileManagement.CreateFile(Constants.gameFlowLogFile);
        FileManagement.CreateFile(Constants.automationLogFile);
        FileManagement.CreateFile(Constants.overlayLogFile);
        FileManagement.CreateFile(Constants.avaloniaConfigFile);
        FileManagement.CreateFile(Constants.settingsFile);
    }

    private static void CreateAllDirectories()
    {
        FileManagement.CreateDirectory(Constants.mobahinted);
        FileManagement.CreateDirectory(Constants.assets);
        FileManagement.CreateDirectory(Constants.data);
        FileManagement.CreateDirectory(Constants.logs);
        FileManagement.CreateDirectory(Constants.cachedMatchesFolder);
        FileManagement.CreateDirectory(Constants.imageCacheFolder);
        FileManagement.CreateDirectory(Constants.imageCacheDataDragonFolder);
        FileManagement.CreateDirectory(Constants.imageCacheProfileIconFolder);
        FileManagement.CreateDirectory(Constants.dataDragonFolder);
        FileManagement.CreateDirectory(Constants.dataDragonChampionFolder);
    }

    public static void CreateAllContent()
    {
        Program.Log(
                source: nameof(Setup),
                method: "createAllContent()",
                message: "Creating all necessary files and directories...",
                logLevel: LogLevel.info,
                logLocation: LogLocation.main
            );

        CreateAllDirectories();
        CreateAllFiles();
    }
}
