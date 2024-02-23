// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using Avalonia.ReactiveUI;
using client.ViewModels;
using ReactiveUI;

namespace client.Views;

public partial class LoadingView : ReactiveUserControl<Loading>, View
{
    public LoadingView()
    {
        this.WhenActivated(disposables => { });
        InitializeComponent();
    }
}
