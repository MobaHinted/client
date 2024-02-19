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
            && FileManagement.fileExists(Constants.avaloniaConfigFile)
            && FileManagement.fileExists(Constants.settingsFile);
    }

    private static bool allDirectoriesExist()
    {
        return FileManagement.directoryExists(Constants.mobahinted)
            && FileManagement.directoryExists(Constants.assets)
            && FileManagement.directoryExists(Constants.data)
            && FileManagement.directoryExists(Constants.imageCacheFolder)
            && FileManagement.directoryExists(Constants.imageCacheDataDragonFolder)
            && FileManagement.directoryExists(Constants.dataDragonFolder)
            && FileManagement.directoryExists(Constants.dataDragonChampionFolder)
            && FileManagement.directoryExists(Constants.rankedEmblemsFolder);
    }

    public static bool allContentExists()
    {
        return allFilesExist() && allDirectoriesExist();
    }

    private static void createAllFiles()
    {
        FileManagement.createFile(Constants.usersFile);
        FileManagement.createFile(Constants.friendsFile);
        FileManagement.createFile(Constants.championRolesDataFile);
        FileManagement.createFile(Constants.avaloniaConfigFile);
        FileManagement.createFile(Constants.settingsFile);
    }

    private static void createAllDirectories()
    {
        FileManagement.createDirectory(Constants.mobahinted);
        FileManagement.createDirectory(Constants.assets);
        FileManagement.createDirectory(Constants.data);
        FileManagement.createDirectory(Constants.imageCacheFolder);
        FileManagement.createDirectory(Constants.imageCacheDataDragonFolder);
        FileManagement.createDirectory(Constants.dataDragonFolder);
        FileManagement.createDirectory(Constants.dataDragonChampionFolder);
        FileManagement.createDirectory(Constants.rankedEmblemsFolder);
    }

    public static void createAllContent()
    {
        createAllDirectories();
        createAllFiles();
    }
}
