// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using Avalonia.ReactiveUI;
using ReactiveUI;

#endregion

namespace client.Views.Match;

public partial class GameStatsElement : ReactiveUserControl<ViewModels.MatchHistory>,
    IElement
{
    public GameStatsElement()
    {
        this.WhenActivated(disposables => { });
        InitializeComponent();
    }
}
