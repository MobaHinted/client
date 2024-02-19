// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using System.Data;
using Avalonia.Controls;
using Avalonia.Controls.Templates;
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
            throw new EvaluateException("View not found: " + name);

        Console.WriteLine("Building view: " + name);

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
