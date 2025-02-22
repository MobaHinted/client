// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using System.ComponentModel.DataAnnotations;
using System.Diagnostics.CodeAnalysis;
using System.Reactive;
using Camille.Enums;
using client.Models;
using client.Models.Accounts;
using client.Models.Data;
using client.Models.UIHelpers;
using ReactiveUI;
using static System.Enum;

#endregion

namespace client.ViewModels;

public class Login : ReactiveObject, IRoutableViewModel
{
    /// <summary>
    ///     Whether the button should be disabled due to an error
    /// </summary>
    private bool _canAdd;

    /// <summary>
    ///     The error from the last attempt to search for a riot ID, if an
    /// </summary>
    private string _errorResult = string.Empty;

    /// <summary>
    ///     Game Name-part of Riot ID validation
    /// </summary>
    private string _gameName = string.Empty;

    /// <summary>
    ///     Whether the loading spinner should display
    /// </summary>
    private bool _isLoading;

    /// <summary>
    ///     Tag Line-part of Riot ID validation
    /// </summary>
    private string _tagLine = string.Empty;

    /// <summary>
    ///     Construct initial data needed for the login window.
    /// </summary>
    public Login(IScreen screen)
    {
        Program.Log(
                source: nameof(Login),
                method: "ctor()",
                doing: "Loading",
                message: "Login View",
                logLevel: LogLevel.info,
                logLocation: LogLocation.main
            );

        // Save the previous screen
        this.HostScreen = screen;

        // Fill the Platforms list with the names of the platforms.
        this.Platforms = GetPlatformRoutes();
        // We list platforms instead of continents/"regions", despite the latter being
        // what is used to look up accounts, because we can extrapolate the continent
        // from the platform, and the platform is used for the majority of calls

        // Find the index of the default platform: NA.
        this.Region =
            this.Platforms.FindIndex(platform => platform == "North America");

        // Set up a command to handle the button click
        this.SearchAndAddAccountCommand =
            ReactiveCommand.Create(SearchAndAddAccount);
    }

    /// <summary>
    ///     The list of platforms available.
    /// </summary>
    public List<string> Platforms { get; set; }

    public string ErrorResult
    {
        get => this._errorResult;
        set =>
            this.RaiseAndSetIfChanged(
                    ref this._errorResult,
                    value
                );
    }

    /// <summary>
    ///     Public version of _canAdd that is translated to "true" or "false"
    /// </summary>
    public string CanAdd
    {
        get => this._canAdd ? "true" : "false";
        set =>
            this.RaiseAndSetIfChanged(
                    ref this._canAdd,
                    value == "true"
                );
    }

    /// <summary>
    ///     Public version of _isLoading that is translated to "true" or "false"
    /// </summary>
    public string IsLoading
    {
        get => this._isLoading ? "true" : "false";
        set =>
            this.RaiseAndSetIfChanged(
                    ref this._isLoading,
                    value == "true"
                );
    }

    /// <summary>
    ///     Game Name-part of Riot ID validation
    /// </summary>
    public string GameName
    {
        get => this._gameName;
        set
        {
            // Check if game name is valid
            ValidRiotIDStatus validity = ValidateRiotID.GameName(value);
            if (validity != ValidRiotIDStatus.valid)
            {
                this.CanAdd = "false";
                throw new RiotIDValidationError(validity);
            }

            // Only actually update the backer if it is
            this.RaiseAndSetIfChanged(
                    ref this._gameName,
                    value
                );

            // Check if the other half of the Riot ID is valid as well, to enable the button
            if (ValidateRiotID.WholeID(
                        this._gameName,
                        this._tagLine
                    ))
            {
                this.CanAdd = "true";
                this.ErrorResult = string.Empty;
            }
        }
    }

    /// <summary>
    ///     Tag Line-part of Riot ID validation
    /// </summary>
    public string TagLine
    {
        get => this._tagLine;
        set
        {
            // Check if game name is valid
            ValidRiotIDStatus validity = ValidateRiotID.TagLine(value);
            if (validity != ValidRiotIDStatus.valid)
            {
                this.CanAdd = "false";
                throw new RiotIDValidationError(validity);
            }

            // Only actually update the backer if it is
            this.CanAdd = "true";
            this.RaiseAndSetIfChanged(
                    ref this._tagLine,
                    value
                );

            // Check if the other half of the Riot ID is valid as well, to enable the button
            if (ValidateRiotID.WholeID(
                        this._gameName,
                        this._tagLine
                    ))
            {
                this.CanAdd = "true";
                this.ErrorResult = string.Empty;
            }
        }
    }

    /// <summary>
    ///     The index of the selected platform in the Platforms list.
    /// </summary>
    public int Region { get; set; }

    public ReactiveCommand<Unit, Unit> SearchAndAddAccountCommand { get; }

    public string UrlPathSegment
    {
        get => "Login";
    }

    public IScreen HostScreen { get; }

    /// <summary>
    ///     Build a list of all available platforms, except PBE.
    /// </summary>
    /// <returns>
    ///     The proper name of each platform - what users and the API identify as
    ///     regions
    /// </returns>
    private static List<string> GetPlatformRoutes()
    {
        return GetValues<PlatformRoute>()
            .Where(value => value != PlatformRoute.PBE1)
            .Select(
                value =>
                {
                    string? description = value.GetType().GetField(value.ToString())!
                        .GetCustomAttributes(
                                typeof(DisplayAttribute),
                                false
                            )
                        .Cast<DisplayAttribute>()
                        .FirstOrDefault()
                        ?.Description;

                    if (description != null && description.EndsWith('.'))
                    {
                        description = description[..^1];
                    }

                    return description;
                }
                )
            .ToList()!;
    }

    /// <summary>
    ///     Search for a Riot ID and add it to local data if it is found.
    /// </summary>
    [SuppressMessage(
            "Performance",
            "CA1806:Do not ignore method results"
        )]
    private void SearchAndAddAccount()
    {
        // Disable the button until the search is complete
        this.CanAdd = "false";
        // Enable the loading spinner
        this.IsLoading = "true";

        // Find the platform from the selected region
        PlatformRoute platform = GetValues<PlatformRoute>()
            .Where(value => value != PlatformRoute.PBE1)
            .First(
                value =>
                {
                    string? description = value.GetType().GetField(value.ToString())!
                        .GetCustomAttributes(
                                typeof(DisplayAttribute),
                                false
                            )
                        .Cast<DisplayAttribute>()
                        .FirstOrDefault()
                        ?.Description;

                    if (description != null && description.EndsWith('.'))
                        description = description[..^1];

                    return description == this.Platforms[this.Region];
                }
                );
        RegionalRoute continent = platform.ToRegional();

        string puuid = string.Empty;
        bool error = false;

        // Search for the account
        Program.Log(
                source: nameof(Login),
                method: "searchAndAddAccount()",
                doing: "Login",
                message: "Searching for...",
                debugSymbols:
                [
                    $"{this.GameName}#{this.TagLine}@{continent}",
                ],
                logLevel: LogLevel.debug,
                logLocation: LogLocation.verbose
            );
        try
        {
            ValidateRiotID.Search(
                    this.GameName,
                    this.TagLine,
                    continent,
                    out puuid
                );
        }
        catch (AggregateException e)
        {
            error = true;
            Program.Log(
                    source: nameof(Login),
                    method: "searchAndAddAccount()",
                    doing: "Login",
                    message: "Search failed",
                    debugSymbols:
                    [
                        "likely a URI issue",
                        e.GetType().FullName!,
                        e.Message,
                        e.StackTrace!,
                    ],
                    logLevel: LogLevel.fatal,
                    logLocation: LogLocation.main
                );
        }
        catch (Exception e)
        {
            error = true;
            Program.Log(
                    source: nameof(Login),
                    method: "searchAndAddAccount()",
                    doing: "Login",
                    message: "Search failed",
                    debugSymbols:
                    [
                        "Unknown Issue",
                        e.GetType().FullName!,
                        e.Message,
                    ],
                    logLevel: LogLevel.error,
                    logLocation: LogLocation.main
                );
        }

        // If the search failed outright, set an error message
        if (error)
        {
            this.ErrorResult = "Search failed";
            this.CanAdd = "false";
            this.IsLoading = "false";
        }
        // If the search did not return a result, set the error message
        else if (!ValidateRiotID.Exists(puuid))
        {
            Program.Log(
                    source: nameof(Login),
                    method: "searchAndAddAccount()",
                    doing: "Login",
                    message: "Account not found",
                    debugSymbols:
                    [
                        $"{this.GameName}#{this.TagLine}@{continent}",
                    ],
                    logLevel: LogLevel.info,
                    logLocation: LogLocation.warningsPlus
                );
            this.ErrorResult = "Account not found on Riot";
            this.CanAdd = "false";
            this.IsLoading = "false";
        }
        else
        {
            Program.Log(
                    source: nameof(Login),
                    method: "searchAndAddAccount()",
                    doing: "Login",
                    message: "Account found on Riot",
                    debugSymbols:
                    [
                        $"{this.GameName}#{this.TagLine}@{continent}",
                    ],
                    logLevel: LogLevel.debug,
                    logLocation: LogLocation.verbose
                );

            // Try to save the account
            try
            {
                // Create the account
                var account = new Account(
                        this.GameName,
                        this.TagLine,
                        platform,
                        puuid
                    );
                // Save the account
                account.Save();

                Program.Log(
                        source: nameof(Login),
                        method: "searchAndAddAccount()",
                        doing: "Login",
                        message: "Added account locally",
                        debugSymbols:
                        [
                            $"{this.GameName}#{this.TagLine}@{continent}",
                        ],
                        logLevel: LogLevel.debug,
                        logLocation: LogLocation.main
                    );

                // Set the active account to the new account
                Program.Settings.activeAccount = account.ID;
                Program.Account = account;
            }
            // If the account already exists, set the active account to the existing
            // account
            catch (DataValidationError)
            {
                Program.Log(
                        source: nameof(Launch),
                        method: "ctor()",
                        doing: "Login",
                        message: "Account already exists locally",
                        debugSymbols:
                        [
                            $"{this.GameName}#{this.TagLine}@{continent}",
                        ],
                        logLevel: LogLevel.debug,
                        logLocation: LogLocation.warningsPlus
                    );

                // Load the accounts from disk
                FileManagement.LoadFromFile(
                        Constants.usersFile,
                        out List<Account>? accounts
                    );
                // Search for the account
                Account account = accounts!.Find(
                        account => account.GameName == this.GameName
                            && account.TagLine == this._tagLine
                            && account.Region == platform
                    );
                // Set the active account to the existing account
                Program.Settings.activeAccount = account.ID;
                Program.Account = account;
            }

            // Navigate back to the loading screen
            Program.Router.Navigate.Execute(new Loading(this.HostScreen));
        }
    }
}
