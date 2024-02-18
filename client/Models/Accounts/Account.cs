// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using System.Text.Json;
using Camille.Enums;
using client.Models.Data;

namespace client.Models.Accounts;

public struct Account
{
    public Guid ID { get; set; }
    public string GameName { get; set; }
    public string TagLine { get; set; }
    public string RiotID { get; set; }

    public PlatformRoute Region { get; set; }
    public RegionalRoute Continent { get; set; }

    /// <summary>
    ///     Create a new Account with fresh data
    /// </summary>
    /// <param name="gameName">The GameName from the user's Riot ID</param>
    /// <param name="tagLine">The TagLine from the user's Riot ID</param>
    /// <param name="region">The region the user is in</param>
    public Account(string gameName, string tagLine, PlatformRoute region)
    {
        this.ID = Guid.NewGuid();

        this.GameName = gameName;
        this.TagLine = tagLine;
        this.RiotID = $"{this.GameName}#{this.TagLine}";

        this.Region = region;
        this.Continent = region.ToRegional();
    }

    /// <summary>
    ///     Load an existing account from file, given its ID
    /// </summary>
    /// <param name="id">The user's generated GUID</param>
    /// <exception cref="ArgumentException">
    ///     If there is no user with the given GUID or users
    ///     saved at all
    /// </exception>
    public Account(Guid id)
    {
        // Open the user file and load its data
        FileManagement.loadFromFile(
                Constants.usersFile,
                out List<Account>? accounts
            );
        // If the file does not have a list of users, add this user to it
        if (accounts is default(List<Account>))
        {
            throw new ArgumentException("No users found");
        }

        // If the file has a list of users, find the user with the given ID
        Account? account = accounts.Find(account => account.ID == id);
        // If the user is not found, throw an exception
        if (account is null)
        {
            throw new ArgumentException("No user found with given ID: " + id);
        }

        // If the user is found, set this user to the found user
        this = (Account)account;
    }

    /// <summary>
    ///     Save this user to the users file
    /// </summary>
    public void save()
    {
        // Open the user file and load its data
        FileManagement.loadFromFile(
                Constants.usersFile,
                out List<Account>? accounts
            );
        // If the file has a list of users, add this user to it
        if (accounts is not default(List<Account>))
        {
            accounts.Add(this);
            FileManagement.saveToFile(
                    Constants.usersFile,
                    accounts
                );
        }
        // If the file doesn't have a list of users, create one and add this user
        else
        {
            FileManagement.saveToFile(
                    Constants.usersFile,
                    new List<Account> { this }
                );
        }
    }

    /// <summary>
    /// </summary>
    /// <returns></returns>
    public override string ToString()
    {
        return JsonSerializer.Serialize(this);
    }
}
