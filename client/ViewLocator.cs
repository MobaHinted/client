// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using System.Data;
using Avalonia.Controls;
using Avalonia.Controls.Templates;
using client.Models;
using ReactiveUI;

namespace client;

public class ViewLocator : IDataTemplate, IViewLocator
{
    public Control? Build(object? data)
    {
        // Early bail when nothing was passed
        if (data is null)
            return null;

        // Try to find the view by taking `client.ViewModels.Loading` and turning it
        // into `client.Views.LoadingView`
        string name = data.GetType().FullName!.Replace(
                    "ViewModel",
                    "View",
                    StringComparison.Ordinal
                )
            + "View";
        var type = Type.GetType(name);

        // If no such view was found, try for a Container in a subfolder
        if (type == null)
        {
            name = "client.Views." + data.GetType().Name + ".Container";
            Program.log(
                    source: nameof(ViewLocator),
                    method: "Build()",
                    doing: "Found no view",
                    message: "Checking client.Views.*",
                    debugSymbols: [$"searching for: {name}"],
                    logLevel: LogLevel.debug
                );

            type = Type.GetType(name);
        }

        // If no such view was found, even with checking the subfolders
        if (type == null)
        {
            var error = new EvaluateException("View not found: " + name);

            Program.log(
                    source: nameof(ViewLocator),
                    method: "Build()",
                    message: "Building View" + error.Message,
                    debugSymbols:
                    [$"from: {data.GetType().FullName!}", $"to: {name}"],
                    logLevel: LogLevel.fatal
                );

            throw error;
        }

        // Success
        Program.log(
                source: nameof(ViewLocator),
                method: "Build()",
                message: "Building View",
                debugSymbols: [$"name: {name}"],
                logLevel: LogLevel.debug
            );

        // Set the data context and load the view
        var control = (Control)Activator.CreateInstance(type)!;
        control.DataContext = data;
        return control;
    }

    public bool Match(object? data)
    {
        return data is ReactiveObject;
    }

    public IViewFor? ResolveView<T>(T? viewModel, string? contract = null)
    {
        return (IViewFor?)Build(viewModel);
    }
}
