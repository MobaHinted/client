// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using Avalonia.ReactiveUI;
using ReactiveUI;

namespace client.Views.MatchHistory;

public partial class FriendsElement : ReactiveUserControl<ViewModels.MatchHistory>,
    Ielement
{
    public FriendsElement()
    {
        this.WhenActivated(disposables => { });
        InitializeComponent();
    }
}
