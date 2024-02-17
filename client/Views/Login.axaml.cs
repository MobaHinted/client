using Avalonia.ReactiveUI;
using client.ViewModels;
using ReactiveUI;

namespace client.Views;

public partial class LoginView : ReactiveUserControl<Login>
{
    public LoginView()
    {
        this.WhenActivated(disposables => { });
        InitializeComponent();
    }
}
