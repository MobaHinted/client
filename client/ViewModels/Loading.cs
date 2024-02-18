using client.Models.Data;
using System.Reactive;
using ReactiveUI;

namespace client.ViewModels;

public class Loading : ReactiveObject, IScreen
{
    public static string Greeting
    {
        get => "Loading...";
    }

    public RoutingState Router { get; } = new RoutingState();

    public Loading()
    {
      if (Program.Settings.activeAccount == null)
      {
        this.Router.Navigate.Execute(new Login(this));
        return;
      }
    }
}
