using System;
using System.Data;
using Avalonia.Controls;
using Avalonia.Controls.Templates;
using client.ViewModels;
using ReactiveUI;

namespace client;

public class ViewLocator : IDataTemplate, IViewLocator
{
    public Control? Build(object? data)
    {
        if (data is null)
            return null;

        var name = data.GetType().FullName!
              .Replace("ViewModel", "View", StringComparison.Ordinal)
            + "View";
        var type = Type.GetType(name);

        if (type == null)
            throw new EvaluateException("View not found: " + name);

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
