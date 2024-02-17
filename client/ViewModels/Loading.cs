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

    // The command that navigates a user to first view model.
    public ReactiveCommand<Unit, IRoutableViewModel> Go { get; }

    public Loading()
    {
        this.Go = ReactiveCommand.CreateFromObservable(
            () => this.Router.Navigate.Execute(new Login(this))
        );
    }
}
