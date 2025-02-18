// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using Avalonia.ReactiveUI;
using ReactiveUI;

#endregion

namespace client.Views.MatchHistory;

public partial class PlayerElement : ReactiveUserControl<ViewModels.MatchHistory>
{
    public PlayerElement()
    {
        this.WhenActivated(disposables => { });
        InitializeComponent();
    }
}
