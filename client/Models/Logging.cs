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
