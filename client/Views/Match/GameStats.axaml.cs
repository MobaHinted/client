// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using Avalonia.ReactiveUI;
using ReactiveUI;

namespace client.Views.Match;

public partial class GameStats : ReactiveUserControl<ViewModels.MatchHistory>,
    Ielement
{
    public GameStats()
    {
        this.WhenActivated(disposables => { });
        InitializeComponent();
    }
}
