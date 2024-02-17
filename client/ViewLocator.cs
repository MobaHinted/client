using System;
using Avalonia.Controls;
using Avalonia.Controls.Templates;
using client.ViewModels;

namespace client;

public class ViewLocator : IDataTemplate
{
    public Control? Build(object? data)
    {
        if (data is null)
            return null;
        
        var name = data.GetType().FullName!.Replace("ViewModel", "View", StringComparison.Ordinal);
        var type = Type.GetType(name);

        Console.WriteLine(name);

        if (type != null)
        {
          Console.WriteLine("here");
            var control = (Control)Activator.CreateInstance(type)!;
            control.DataContext = data;
            return control;
        }
        else
        {
          Console.WriteLine("not here");
        }
        
        return new TextBlock { Text = "Not Found: " + name };
    }

    public bool Match(object? data)
    {
        return data is ViewModelBase;
    }
}
