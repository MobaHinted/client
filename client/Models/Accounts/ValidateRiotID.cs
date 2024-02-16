using client.Models.UIHelpers;
using System.ComponentModel;
using System.Diagnostics.CodeAnalysis;
using System.Reflection;
using System.Text.RegularExpressions;

namespace client.Models.Accounts;


/// <summary>
/// Turn a ValidRiotIDStatus into a DataValidationErrorz
/// </summary>
public class RiotIDValidationError : DataValidationError
{
  /// <summary>
  /// Turn a ValidRiotIDStatus into a DataValidationError
  /// </summary>
  /// <param name="specifiedError">The resulting RiotID status</param>
  public RiotIDValidationError(ValidRiotIDStatus specifiedError) : base(
    specifiedError.getDescription()
  )
  {
  }
}

/// <summary>
/// Returns for various results of Riot ID validation attempts
/// </summary>
public enum ValidRiotIDStatus
{
  /// <summary>
  /// The Riot ID is valid
  /// </summary>
  [Description("Valid")]
  valid,
  /// <summary>
  /// The Riot ID is too short
  /// </summary>
  [Description("Too Short")]
  tooShort,
  /// <summary>
  /// The Game Name is too long
  /// </summary>
  [Description("Too long; 16 max")]
  gameNameTooLong,
  /// <summary>
  /// The Tag Line is too long (5 max)
  /// </summary>
  [Description("Too long")]
  tagLineTooLong,
  /// <summary>
  /// The Riot ID contains invalid characters
  /// </summary>
  [Description("Invalid")]
  invalidCharacters,
  /// <summary>
  /// The Riot ID contains invalid phrases
  /// </summary>
  [Description("Invalid phrase")]
  invalidPhrases,
  /// <summary>
  /// The Riot ID was not found (on this region)
  /// </summary>
  [Description("Riot ID not found")]
  notFound,
  /// <summary>
  /// The Riot ID was found
  /// </summary>
  [Description("Found!")]
  found,
}

/// <summary>
/// Get the descriptor of a Riot ID status
/// </summary>
public static class EnumExtensions
{
  public static string getDescription(this Enum value)
  {
    // Search for the ValidRiotIDStatus
    FieldInfo? field = value.GetType().GetField(value.ToString());

    // Get the Description attribute
    var attribute = Attribute.GetCustomAttribute(
        field!, typeof(DescriptionAttribute)
      ) as DescriptionAttribute;

    // Return the description, or the value itself if there is none
    return attribute?.Description ?? value.ToString();
  }
}

/// <summary>
/// Class for verifying the validity of a Riot ID, its parts, and finding it
/// </summary>
public static class ValidateRiotID
{
  /// <summary>
  /// The Regular Expression for known-invalid Riot ID characters
  /// </summary>
  /// <returns>Ready Regular Expression</returns>
  [SuppressMessage("Performance","SYSLIB1045:Convert to \'GeneratedRegexAttribute\'.")]
  private static Regex invalidIDCharacters()
  {
    return new Regex(@"[#*\/\\?!%]| {2,}");
  }

  /// <summary>
  /// Minimum length for a GameName
  /// </summary>
  private const int MIN_GAME_NAME_LENGTH = 3;

  /// <summary>
  /// Maximum length for a GameName
  /// </summary>
  private const int MAX_GAME_NAME_LENGTH = 16;

  /// <summary>
  /// Minimum length for a TagLine
  /// </summary>
  private const int MIN_TAG_LINE_LENGTH = 3;

  /// <summary>
  /// Maximum length for a TagLine
  /// </summary>
  private const int MAX_TAG_LINE_LENGTH = 5;

  /// <summary>
  /// Whether a given GameName for a Riot ID is valid.
  /// Checks for length and known-invalid characters.
  /// </summary>
  /// <param name="gameName">The given GameName</param>
  /// <returns>Riot ID Validity Status enum</returns>
  public static ValidRiotIDStatus gameName(string gameName)
  {
    if (invalidIDCharacters().IsMatch(gameName))
    {
      return ValidRiotIDStatus.invalidCharacters;
    }

    switch (gameName.Length)
    {
      case < MIN_GAME_NAME_LENGTH:
        return ValidRiotIDStatus.tooShort;
      case > MAX_GAME_NAME_LENGTH:
        return ValidRiotIDStatus.gameNameTooLong;
    }

    return ValidRiotIDStatus.valid;
  }

  /// <summary>
  /// Whether a given TagLine for a Riot ID is valid.
  /// Checks for length and known-invalid characters.
  /// </summary>
  /// <param name="tagLine">The given TagLine</param>
  /// <returns>Riot ID Validity Status enum</returns>
  public static ValidRiotIDStatus tagLine(string tagLine)
  {
    if (invalidIDCharacters().IsMatch(tagLine))
    {
      return ValidRiotIDStatus.invalidCharacters;
    }

    switch (tagLine.Length)
    {
      case < MIN_TAG_LINE_LENGTH:
        return ValidRiotIDStatus.tooShort;
      case > MAX_TAG_LINE_LENGTH:
        return ValidRiotIDStatus.tagLineTooLong;
    }

    return ValidRiotIDStatus.valid;
  }

  /// <summary>
  /// Whether a given Riot ID is valid.
  /// </summary>
  /// <param name="gameName">The given GameName</param>
  /// <param name="tagLine">The given TagLine</param>
  /// <returns>Whether it is a valid Riot ID</returns>
  public static bool wholeID(string gameName, string tagLine)
  {
    return ValidateRiotID.gameName(gameName) == ValidRiotIDStatus.valid
           && ValidateRiotID.tagLine(tagLine) == ValidRiotIDStatus.valid;
  }
}
