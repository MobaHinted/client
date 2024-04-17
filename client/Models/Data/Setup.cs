// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

namespace client.Models.Data;

public static class Setup
{
    private static bool allFilesExist()
    {
        return FileManagement.fileExists(Constants.usersFile)
            && FileManagement.fileExists(Constants.friendsFile)
            && FileManagement.fileExists(Constants.championRolesDataFile)
            && FileManagement.fileExists(Constants.fullLogFile)
            && FileManagement.fileExists(Constants.warningsPlusLogFile)
            && FileManagement.fileExists(Constants.mainLogFile)
            && FileManagement.fileExists(Constants.downloadLogFile)
            && FileManagement.fileExists(Constants.downloadLogFile)
            && FileManagement.fileExists(Constants.gameFlowLogFile)
            && FileManagement.fileExists(Constants.automationLogFile)
            && FileManagement.fileExists(Constants.overlayLogFile)
            && FileManagement.fileExists(Constants.avaloniaConfigFile)
            && FileManagement.fileExists(Constants.settingsFile);
    }

    private static bool allDirectoriesExist()
    {
        return FileManagement.directoryExists(Constants.mobahinted)
            && FileManagement.directoryExists(Constants.assets)
            && FileManagement.directoryExists(Constants.data)
            && FileManagement.directoryExists(Constants.logs)
            && FileManagement.directoryExists(Constants.cachedMatchesFolder)
            && FileManagement.directoryExists(Constants.imageCacheFolder)
            && FileManagement.directoryExists(Constants.imageCacheDataDragonFolder)
            && FileManagement.directoryExists(Constants.imageCacheProfileIconFolder)
            && FileManagement.directoryExists(Constants.dataDragonFolder)
            && FileManagement.directoryExists(Constants.dataDragonChampionFolder);
    }

    public static bool allContentExists()
    {
        bool filesExist = allFilesExist();
        bool directoriesExist = allDirectoriesExist();

        Program.log(
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

    private static void createAllFiles()
    {
        FileManagement.createFile(Constants.usersFile);
        FileManagement.createFile(Constants.friendsFile);
        FileManagement.createFile(Constants.championRolesDataFile);
        FileManagement.createFile(Constants.fullLogFile);
        FileManagement.createFile(Constants.warningsPlusLogFile);
        FileManagement.createFile(Constants.mainLogFile);
        FileManagement.createFile(Constants.downloadLogFile);
        FileManagement.createFile(Constants.gameFlowLogFile);
        FileManagement.createFile(Constants.automationLogFile);
        FileManagement.createFile(Constants.overlayLogFile);
        FileManagement.createFile(Constants.avaloniaConfigFile);
        FileManagement.createFile(Constants.settingsFile);
    }

    private static void createAllDirectories()
    {
        FileManagement.createDirectory(Constants.mobahinted);
        FileManagement.createDirectory(Constants.assets);
        FileManagement.createDirectory(Constants.data);
        FileManagement.createDirectory(Constants.logs);
        FileManagement.createDirectory(Constants.cachedMatchesFolder);
        FileManagement.createDirectory(Constants.imageCacheFolder);
        FileManagement.createDirectory(Constants.imageCacheDataDragonFolder);
        FileManagement.createDirectory(Constants.imageCacheProfileIconFolder);
        FileManagement.createDirectory(Constants.dataDragonFolder);
        FileManagement.createDirectory(Constants.dataDragonChampionFolder);
    }

    public static void createAllContent()
    {
        Program.log(
                source: nameof(Setup),
                method: "createAllContent()",
                message: "Creating all necessary files and directories...",
                logLevel: LogLevel.info,
                logLocation: LogLocation.main
            );

        createAllDirectories();
        createAllFiles();
    }
}
