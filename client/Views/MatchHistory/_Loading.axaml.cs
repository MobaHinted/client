﻿// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using Avalonia.ReactiveUI;
using ReactiveUI;

namespace client.Views.MatchHistory;

public partial class LoadingSubView : ReactiveUserControl<ViewModels.MatchHistory>,
    IsubView
{
    public LoadingSubView()
    {
        this.WhenActivated(disposables => { });
        InitializeComponent();
    }
}