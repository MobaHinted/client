// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using Avalonia.ReactiveUI;
using client.ViewModels;
using ReactiveUI;

#endregion

namespace client.Views;

public partial class LoginView : ReactiveUserControl<Login>, Iview
{
    public LoginView()
    {
        this.WhenActivated(disposables => { });
        InitializeComponent();
    }
}
