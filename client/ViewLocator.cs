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
        if (data is null)
            return null;

        string name = data.GetType().FullName!.Replace(
                    "ViewModel",
                    "View",
                    StringComparison.Ordinal
                )
            + "View";
        var type = Type.GetType(name);

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

        Program.log(
                source: nameof(ViewLocator),
                method: "Build()",
                message: "Building View",
                debugSymbols: [$"name: {name}"],
                logLevel: LogLevel.debug
            );

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
