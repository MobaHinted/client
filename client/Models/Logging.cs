// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using client.Models.Data;

namespace client.Models;

[Flags]
public enum LogTo
{
    file = 0,
    console = 1,
    retryPopup = 2,
    errorScreen = 4,
}

[Flags]
public enum LogLocation
{
    /// <summary>
    ///     The main log file.
    /// </summary>
    /// <seealso cref="Constants.mainLogFile" />
    main = 0,
    /// <summary>
    ///     The download-flow log file.
    /// </summary>
    /// <remarks>
    ///     Primarily this pertains to updating at launch, and downloading games for
    ///     match history and similar pages.
    /// </remarks>
    /// <seealso cref="Constants.downloadLogFile" />
    download = 1,
    /// <summary>
    ///     The game flow log file, as in pre-game, in-game, and post-game.
    /// </summary>
    /// <seealso cref="Constants.gameFlowLogFile" />
    gameFlow = 2,
    /// <summary>
    ///     The automation log file, for all operations running continuously in the
    ///     background.
    /// </summary>
    /// <seealso cref="Constants.automationLogFile" />
    automation = 4,
    /// <summary>
    ///     The overlay log file, for overlay-specific operations.
    /// </summary>
    /// <seealso cref="Constants.overlayLogFile" />
    overlays = 8,
    /// <summary>
    ///     The verbose log file, for all logs. An auto-targeted log.
    /// </summary>
    /// <seealso cref="Constants.fullLogFile" />
    verbose = 16,
    /// <summary>
    ///     The warningsPlus log file, for all logs of warning level or higher. An
    ///     auto-targeted log.
    /// </summary>
    /// <seealso cref="Constants.warningsPlusLogFile" />
    warningsPlus = 32,
    /// <summary>
    ///     All log locations.
    /// </summary>
    /// <remarks>
    ///     For Announcement logs.
    /// </remarks>
    /// <seealso cref="App.OnExit" />
    all = main
        | download
        | gameFlow
        | automation
        | overlays
        | verbose
        | warningsPlus,
}

public enum LogLevel
{
    debug,
    info,
    warning,
    error,
    fatal,
}

public class Logging
{
    /// <summary>
    ///     A lock object for the console to prevent color bleeding.
    /// </summary>
    private readonly static object consoleLock = new object();
    /// <summary>
    ///     A dictionary of log locations and their respective log files.
    /// </summary>
    private Dictionary<LogLocation, string> _logLocations =
        new Dictionary<LogLocation, string>
        {
            { LogLocation.main, Constants.mainLogFile },
            { LogLocation.download, Constants.downloadLogFile },
            { LogLocation.gameFlow, Constants.gameFlowLogFile },
            { LogLocation.automation, Constants.automationLogFile },
            { LogLocation.overlays, Constants.overlayLogFile },
            { LogLocation.verbose, Constants.fullLogFile },
            { LogLocation.warningsPlus, Constants.warningsPlusLogFile },
        };

    /// <summary>
    ///     A lock for each log location to prevent file access conflicts.
    /// </summary>
    private Dictionary<LogLocation, object> _logLocks =
        new Dictionary<LogLocation, object>
        {
            { LogLocation.main, new object() },
            { LogLocation.download, new object() },
            { LogLocation.gameFlow, new object() },
            { LogLocation.automation, new object() },
            { LogLocation.overlays, new object() },
            { LogLocation.verbose, new object() },
            { LogLocation.warningsPlus, new object() },
        };

    /// <summary>
    ///     The code behind the global logging functionality for the application.
    /// </summary>
    /// <remarks>
    ///     This method should not be used directly.
    ///     Use Program.Log instead.
    ///     See the example for usage.
    /// </remarks>
    /// <example>
    ///     <code>
    ///     Program.log(
    ///         source: nameof(MatchHistory),
    ///         method: "ctor()",
    ///         doing: "Loading",
    ///         message: "Match History View",
    ///         logLevel: LogLevel.info
    ///     );
    ///     </code>
    /// </example>
    /// <seealso cref="Program.log" />
    /// <param name="logTo">
    ///     How the log should be given, see: <see cref="LogTo" />
    /// </param>
    /// <param name="source">
    ///     The class giving the log <code>nameof( [this class] )</code>
    /// </param>
    /// <param name="method">The method giving the log</param>
    /// <param name="doing">What is being done - used to group logs together</param>
    /// <param name="message">The message to display</param>
    /// <param name="debugSymbols">Any debug symbols to include</param>
    /// <param name="url">Any URL the reader can open to test directly with</param>
    /// <param name="logLevel">
    ///     <see cref="LogLevel" /> for this log. Also decides coloration in console.
    /// </param>
    /// <param name="logLocation">
    ///     The log file this log should appear in, see: <see cref="LogLocation" />
    /// </param>
    public void log(
        LogTo logTo,
        string source,
        string method,
        string doing,
        string message,
        string[] debugSymbols,
        string url,
        LogLevel logLevel,
        LogLocation logLocation
    )
    {
        // Turn on all console logs for debug
        if (Program.Settings.debug)
            logTo |= LogTo.console;

        // Format and save the log
        string log = format(
                source,
                method,
                doing,
                message,
                debugSymbols,
                url,
                logLocation
            );

        // Write the log to the console if it's enabled
        if (logTo.HasFlag(LogTo.console))
        {
            // Lock the console so color doesn't bleed
            lock (consoleLock)
            {
                color(logLevel);
                Console.Write(log);
                Console.ResetColor();
            }
        }

        if (logTo.HasFlag(LogTo.file))
        {
            // Always log to the verbose log
            logLocation |= LogLocation.verbose;

            // Include the log in the main log if it's an info or higher
            if (logLevel >= LogLevel.info)
                logLocation |= LogLocation.main;

            // Include the log in the warningsPlus log if it's a warning or worse
            if (logLevel >= LogLevel.warning)
                logLocation |= LogLocation.warningsPlus;

            // For each log location option
            foreach (LogLocation location in Enum.GetValues(typeof(LogLocation)))
                // If the location was selected
            {
                if (logLocation.HasFlag(location))
                    // Lock the log file
                {
                    lock (this._logLocks[location])
                    {
                        // Recreate the log file if it was cleared
                        if (!FileManagement.fileExists(this._logLocations[location]))
                            FileManagement.createFile(this._logLocations[location]);

                        // Append the log to the file
                        FileManagement.appendToFile(
                                this._logLocations[location],
                                log
                            );
                    }
                }
            }
        }
    }

    private static string format(
        string source,
        string method,
        string doing,
        string message,
        string[] debugSymbols,
        string url,
        LogLocation logLocation,
        bool forFile = false
    )
    {
        string log = "";

        // Form the header
        string preface = $"[{source}" + (method == "" ? "" : $"::{method}") + "] ";
        log += preface;

        // Continue the header if an operation is specified
        if (doing != "")
            log += $"{doing}> ";

        // Finish the header with the message
        log += message + "\n";

        // Add debug symbols if they exist
        if (debugSymbols.Length > 0)
        {
            log += "".PadRight(preface.Length);
            log += $"({string.Join(", ", debugSymbols)})\n";
        }

        // Add a URL if it exists
        if (url != "")
        {
            log += "".PadRight(preface.Length);
            log += url + "\n";
        }

        // Format announcement logs
        if (logLocation == LogLocation.all)
        {
            log += "===============================================";
            log += "==============================================";
            log += $" [{DateTime.Now:O}]\n";
        }

        return log;
    }

    private static void color(LogLevel logLevel)
    {
        Console.ForegroundColor = logLevel switch
        {
            LogLevel.debug => ConsoleColor.DarkGray,
            LogLevel.info => ConsoleColor.White,
            LogLevel.warning => ConsoleColor.DarkMagenta,
            LogLevel.error => ConsoleColor.DarkYellow,
            LogLevel.fatal => ConsoleColor.DarkRed,
            _ => throw new ArgumentOutOfRangeException(
                    nameof(logLevel),
                    logLevel,
                    null
                ),
        };
    }
}
