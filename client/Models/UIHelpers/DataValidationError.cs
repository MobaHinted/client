// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

namespace client.Models.UIHelpers;

public class DataValidationError : Exception
{
    /// <summary>
    ///     Build a Data Validation Error
    /// </summary>
    /// <param name="message">The error to display</param>
    public DataValidationError(string message)
        : base(message) { }

    /// <summary>
    ///     Only give the exact error message given
    /// </summary>
    /// <returns>The message first passed into the exception, and nothing else</returns>
    public override string ToString()
    {
        return this.Message;
    }
}
