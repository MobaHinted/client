﻿// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using Avalonia.ReactiveUI;
using ReactiveUI;

namespace client.Views.Match;

public partial class GameStatsElement : ReactiveUserControl<ViewModels.MatchHistory>,
    Ielement
{
    public GameStatsElement()
    {
        this.WhenActivated(disposables => { });
        InitializeComponent();
    }
}