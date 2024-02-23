// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using Avalonia.ReactiveUI;
using ReactiveUI;

namespace client.Views;

public partial class
    MatchHistoryLoadingView : ReactiveUserControl<ViewModels.MatchHistory>, View
{
    public MatchHistoryLoadingView()
    {
        this.WhenActivated(disposables => { });
        InitializeComponent();
    }
}
