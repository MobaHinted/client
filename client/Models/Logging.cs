// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

namespace client.Models;

[Flags]
public enum LogTo
{
    file = 0,
    console = 1,
    retryPopup = 2,
    errorScreen = 4,
}

public enum LogLocation
{
    main,
    download,
    gameFlow,
    automation,
    overlays,
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
    private readonly static object consoleLock = new object();

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
        if (logTo.HasFlag(LogTo.console))
        {
            string preface = $"[{source}"
                + (method == "" ? "" : $"::{method}")
                + "] ";
            string log = preface;

            if (doing != "")
                log += $"{doing}> ";

            log += message + "\n";

            if (debugSymbols.Length > 0)
            {
                log += "".PadRight(preface.Length)
                    + $"({string.Join(", ", debugSymbols)})\n";
            }

            if (url != "")
                log += "".PadRight(preface.Length) + url + "\n";

            lock (consoleLock)
            {
                color(logLevel);
                Console.Write(log);
                Console.ResetColor();
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
