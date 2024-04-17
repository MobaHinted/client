// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using System.Text.Json;

#endregion

namespace client.Models.Data.DataDragon;

public static class DataDragonCall
{
    /// <summary>
    ///     Contacts the Data Dragon API and deserializes it into the given response
    ///     type.
    /// </summary>
    /// <param name="url">DataDragon URL</param>
    /// <typeparam name="T">
    ///     Response Class from <see cref="client.Models.Data.DataDragon" />
    /// </typeparam>
    /// <returns>The URL response, formatted into the specified Response</returns>
    /// <exception cref="ArgumentException">
    ///     Any error from deserializing the API response
    /// </exception>
    /// <exception cref="HttpRequestException">
    ///     Any error from calling the API
    /// </exception>
    public static T getAs<T>(string url)
    {
        // Ensure the type is from the DataDragon namespace
        if (!typeof(T).Namespace!.Contains("DataDragon"))
        {
            var error = new ArgumentException(
                    "Type must be from the DataDragon namespace"
                );
            Program.log(
                    source: nameof(ProgramAssets),
                    method: "getDataDragon()",
                    message: "Type must be from the DataDragon namespace\n" + error,
                    debugSymbols: [typeof(T).Name],
                    url: url,
                    logLevel: LogLevel.fatal,
                    logLocation: LogLocation.warningsPlus
                );
            throw error;
        }

        try
        {
            // Call the API
            var client = new HttpClient();
            var response = client.GetAsync(url);

            // If the first request fails, retry once
            if (!response.Result.IsSuccessStatusCode)
                response = client.GetAsync(url);

            // Read back the response
            var result = response.Result.Content.ReadAsStringAsync();

            // Return the response, deserialized into the given type, if not Simple
            if (!typeof(Simple).IsAssignableFrom(typeof(T)))
            {
                // Verify the Type matches the response
                validateTypeAgainstResponse<T>(result.Result);

                Program.log(
                        source: nameof(ProgramAssets),
                        method: "getDataDragon()",
                        doing: "Downloading",
                        message: typeof(T).Name + " (complex)",
                        url: url,
                        logLevel: LogLevel.debug,
                        logLocation: LogLocation.download
                    );
                return JsonSerializer.Deserialize<T>(result.Result)!;
            }

            Program.log(
                    source: nameof(ProgramAssets),
                    method: "getDataDragon()",
                    doing: "Downloading",
                    message: typeof(T).Name + " (simple)",
                    url: url,
                    logLevel: LogLevel.debug,
                    logLocation: LogLocation.download
                );

            // Get the type of the first variable in T, and save the variable
            // name
            Type type = typeof(T).GetProperties()[0].PropertyType;
            string variable = typeof(T).GetProperties()[0].Name;

            // Deserialize the response into the type of the first variable in T
            object deserialized = JsonSerializer.Deserialize(
                    result.Result,
                    type
                )!;

            // Create a new instance of T
            var newT = (T)Activator.CreateInstance(typeof(T))!;

            // Set the first variable in T to the deserialized response
            newT.GetType().GetProperty(variable)!.SetValue(
                    newT,
                    deserialized
                );

            // Return the new instance of T
            return newT;
        }
        // Handle double timeouts
        catch (HttpRequestException)
        {
            throw new HttpRequestException("The request timed out: " + url);
        }
        catch (ArgumentException e)
        {
            throw new ArgumentException(
                    "The response used in the DataDragon namespace does not match "
                    + "the API response: \n"
                    + url
                    + " -> "
                    + typeof(T)
                    + "\n"
                    + e.Message
                );
        }
        // Handle unexpected errors
        catch (Exception e)
        {
            throw new ArgumentException(
                    "An unexpected error was encountered while parsing the "
                    + "DataDragon API response: \n"
                    + url
                    + " -> "
                    + typeof(T)
                    + "\n"
                    + e
                    + "\n"
                );
        }
    }

    /// <summary>
    ///     Validate that the DataDragon API response matches the given
    ///     <see cref="DataDragon">DataDragon Type</see> in
    ///     <see cref="getAs{T}">Call.getAs()</see>.
    /// </summary>
    /// <param name="json">The API response</param>
    /// <typeparam name="T">The given DataDragon type</typeparam>
    /// <exception cref="ArgumentException">
    ///     The results of data mismatch to repair the DataDragon type with
    /// </exception>
    private static void validateTypeAgainstResponse<T>(string json)
    {
        JsonDocument doc = JsonDocument.Parse(json);

        // Check if the root element is a JSON object
        if (doc.RootElement.ValueKind != JsonValueKind.Object)
            throw new ArgumentException("The JSON does not represent an object.");

        // Get the JsonObject representing the root object in the JSON
        JsonElement.ObjectEnumerator rootObject = doc.RootElement.EnumerateObject();

        // Get the PropertyInfo objects for the properties of the given Type
        var properties = typeof(T).GetProperties();

        // Check if each property is present in the JsonObject
        var missingProperties = (from property in properties
            where rootObject.Current.Value.ValueKind == JsonValueKind.Object
                && rootObject.Current.Value.TryGetProperty(
                        property.Name,
                        out JsonElement _
                    )
            where !rootObject.Current.Value.TryGetProperty(
                    property.Name,
                    out _
                )
            select property.Name).ToList();

        // Check if each key in the JsonObject corresponds to a property
        var extraKeys = new List<string>();
        while (rootObject.MoveNext())
            if (properties.All(p => p.Name != rootObject.Current.Name))
                extraKeys.Add(rootObject.Current.Name);

        // TODO: Check the types of properties are correct as well

        // If there are no missing properties or extra keys, return
        if (missingProperties.Count == 0 && extraKeys.Count == 0)
            return;

        // If there are any missing properties or extra keys, throw an exception
        string message = "";
        if (missingProperties.Count != 0)
            message += "\nExtraneous properties in DataDragon type:\n- "
                + string.Join(
                        "\n- ",
                        missingProperties
                    );

        if (missingProperties.Count != 0 && extraKeys.Count != 0)
            message += "\n";

        if (extraKeys.Count != 0)
            message += "\nResponse keys missing from DataDragon Type:\n- "
                + string.Join(
                        "\n- ",
                        extraKeys
                    );

        throw new ArgumentException(message);
    }
}
