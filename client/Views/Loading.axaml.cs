using Avalonia;
using Avalonia.Controls;

namespace client.Views;

public partial class LoadingView : Window
{
    public LoadingView()
    {
        Program.Window = this;
        InitializeComponent();
    }
}
