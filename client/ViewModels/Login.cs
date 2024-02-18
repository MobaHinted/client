using System.ComponentModel.DataAnnotations;
using System.Diagnostics.CodeAnalysis;
using System.Reactive;
using Avalonia.Controls;
using Camille.Enums;
using client.Models.Accounts;
using client.Views;
using ReactiveUI;
using static System.Enum;

namespace client.ViewModels;

public class Login : ReactiveObject, IRoutableViewModel
{
    public string? UrlPathSegment { get; } = "Login";
    public IScreen HostScreen { get; }

    /// <summary>
    /// The list of platforms available.
    /// </summary>
    public List<string> Platforms { get; set; }

    /// <summary>
    /// The error from the last attempt to search for a riot ID, if an
    /// </summary>
    private string _errorResult = string.Empty;

    public string ErrorResult
    {
        get => this._errorResult;
        set => this.RaiseAndSetIfChanged(ref this._errorResult, value);
    }

    /// <summary>
    /// Whether the button should be disabled due to an error
    /// </summary>
    private bool _canAdd;

    /// <summary>
    /// Public version of _canAdd that is translated to "true" or "false"
    /// </summary>
    public string CanAdd
    {
        get => this._canAdd ? "true" : "false";
        set => this.RaiseAndSetIfChanged(ref this._canAdd, value == "true");
    }

    /// <summary>
    /// Whether the loading spinner should display
    /// </summary>
    private bool _isLoading;

    /// <summary>
    /// Public version of _isLoading that is translated to "true" or "false"
    /// </summary>
    public string IsLoading
    {
        get => this._isLoading ? "true" : "false";
        set => this.RaiseAndSetIfChanged(ref this._isLoading, value == "true");
    }

    /// <summary>
    /// Game Name-part of Riot ID validation
    /// </summary>
    private string _gameName = string.Empty;

    public string GameName
    {
        get => this._gameName;
        set
        {
            // Check if game name is valid
            ValidRiotIDStatus validity = ValidateRiotID.gameName(value);
            if (validity != ValidRiotIDStatus.valid)
            {
                this.CanAdd = "false";
                throw new RiotIDValidationError(validity);
            }

            // Only actually update the backer if it is
            this.RaiseAndSetIfChanged(ref this._gameName, value);

            // Check if the other half of the Riot ID is valid as well, to enable the button
            if (ValidateRiotID.wholeID(this._gameName, this._tagLine))
            {
                this.CanAdd = "true";
                this.ErrorResult = string.Empty;
            }
        }
    }

    /// <summary>
    /// Tag Line-part of Riot ID validation
    /// </summary>
    private string _tagLine = string.Empty;

    public string TagLine
    {
        get => this._tagLine;
        set
        {
            // Check if game name is valid
            ValidRiotIDStatus validity = ValidateRiotID.tagLine(value);
            if (validity != ValidRiotIDStatus.valid)
            {
                this.CanAdd = "false";
                throw new RiotIDValidationError(validity);
            }

            // Only actually update the backer if it is
            this.CanAdd = "true";
            this.RaiseAndSetIfChanged(ref this._tagLine, value);

            // Check if the other half of the Riot ID is valid as well, to enable the button
            if (ValidateRiotID.wholeID(this._gameName, this._tagLine))
            {
                this.CanAdd = "true";
                this.ErrorResult = string.Empty;
            }
        }
    }

    /// <summary>
    ///  The index of the selected platform in the Platforms list.
    /// </summary>
    public int Region { get; set; }

    public ReactiveCommand<Unit, Unit> SearchAndAddAccount { get; }

    /// <summary>
    /// Construct initial data needed for the login window.
    /// </summary>
    public Login(IScreen screen)
    {
        // Save the previous screen
        this.HostScreen = screen;

        // Fill the Platforms list with the names of the platforms.
        this.Platforms = getPlatformRoutes();
        // We list platforms instead of continents/"regions", despite the latter being
        // what is used to look up accounts, because we can extrapolate the continent
        // from the platform, and the platform is used for the majority of calls

        // Find the index of the default platform: NA.
        this.Region = this.Platforms.FindIndex(platform => platform == "North America");

        // Set up a command to handle the button click
        this.SearchAndAddAccount = ReactiveCommand.Create(searchAndAddAccount);
    }

    /// <summary>
    /// Build a list of all available platforms, except PBE.
    /// </summary>
    /// <returns>The proper name of each platform - what users and the API identify as regions</returns>
    private static List<string> getPlatformRoutes()
    {
        return GetValues<PlatformRoute>()
            .Where(value => value != PlatformRoute.PBE1)
            .Select(value =>
            {
                string? description = value
                    .GetType()
                    .GetField(value.ToString())!
                    .GetCustomAttributes(typeof(DisplayAttribute), false)
                    .Cast<DisplayAttribute>()
                    .FirstOrDefault()
                    ?.Description;

                if (description != null && description.EndsWith('.'))
                {
                    description = description[..^1];
                }

                return description;
            })
            .ToList()!;
    }

    /// <summary>
    /// Search for a Riot ID and add it to local data if it is found.
    /// </summary>
    [SuppressMessage("Performance", "CA1806:Do not ignore method results")]
    private void searchAndAddAccount()
    {
        // Disable the button until the search is complete
        this.CanAdd = "false";
        // Enable the loading spinner
        this.IsLoading = "true";

        // Find the platform from the selected region
        PlatformRoute platform = GetValues<PlatformRoute>()
            .Where(value => value != PlatformRoute.PBE1)
            .First(value =>
            {
                string? description = value
                    .GetType()
                    .GetField(value.ToString())!
                    .GetCustomAttributes(typeof(DisplayAttribute), false)
                    .Cast<DisplayAttribute>()
                    .FirstOrDefault()
                    ?.Description;

                if (description != null && description.EndsWith('.'))
                {
                    description = description[..^1];
                }

                return description == this.Platforms[this.Region];
            });

        RegionalRoute continent = platform.ToRegional();

        // Search for the account
        Console.WriteLine($"Searching for {this.GameName}#{this.TagLine}@{continent}...");
        ValidateRiotID.search(this.GameName, this.TagLine, continent, out string puuid);

        // If the search failed, set the error message and disable the button
        if (!ValidateRiotID.exists(puuid))
        {
            Console.WriteLine("Account not found");
            this.ErrorResult = "Account not found.";
            this.CanAdd = "false";
            this.IsLoading = "false";
        }
        else
        {
            Console.WriteLine("Account Found!");

            // Save the account
            var account = new Account(this.GameName, this.TagLine, platform);
            Program.Settings.activeAccount = account;

            // TODO: Save account locally
            // TODO: Open the main window
        }
    }
}
